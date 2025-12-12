import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
# To support OpenAI/Claude in future, import their classes here e.g.:
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_anthropic import ChatAnthropic

from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from sqlalchemy import text
from .db import engine

load_dotenv()

# --- Configuration & Factory ---

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini") # Options: gemini, openai, anthropic
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local") # Options: local, google, openai

print(f"🔹 Config: LLM={LLM_PROVIDER}, Embeddings={EMBEDDING_PROVIDER}")

# 1. LLM Factory
def get_llm():
    if LLM_PROVIDER == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0, 
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    # Future Scalability Stubs:
    # elif LLM_PROVIDER == "openai":
    #     return ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
    # elif LLM_PROVIDER == "anthropic":
    #     return ChatAnthropic(model="claude-3-opus", api_key=os.getenv("ANTHROPIC_API_KEY"))
    else:
        raise ValueError(f"Unknown LLM Provider: {LLM_PROVIDER}")

# 2. Embedding Factory
def get_embeddings():
    if EMBEDDING_PROVIDER == "local":
        print("⚡️ Loading Local Embeddings (HuggingFace)...")
        # standard lightweight model, no API cost
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    elif EMBEDDING_PROVIDER == "google":
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # elif EMBEDDING_PROVIDER == "openai":
    #     return OpenAIEmbeddings()
    else:
        raise ValueError(f"Unknown Embedding Provider: {EMBEDDING_PROVIDER}")

llm = get_llm()
embeddings = get_embeddings()

db = SQLDatabase(engine, include_tables=['customer'])

# --- RAG: Golden Queries ---
# Simple In-Memory "Vector Store" logic for MVP using pgvector directly is robust.

INITIAL_GOLDEN_QUERIES = [
    ("How many customers do we have?", "SELECT count(*) FROM customer;"),
    ("Who are the active customers?", "SELECT first_name, last_name, email FROM customer WHERE active = true LIMIT 10;"),
    ("Show me customers from store 1.", "SELECT * FROM customer WHERE store_id = 1 LIMIT 5;")
]

def seed_golden_queries():
    """Hashes and seeds queries if table is empty."""
    with engine.connect() as conn:
        # Note: vector(384) for MiniLM, vector(768) for Gemini.
        # We need to handle this dimension change if switching providers dynamically on the same DB.
        # For now, we assume the user clears the table if switching providers, or we handle migration.
        
        # Detect dimensions
        sample_vec = embeddings.embed_query("test")
        dim = len(sample_vec)
        
        conn.execute(text(f"CREATE TABLE IF NOT EXISTS golden_queries (id SERIAL PRIMARY KEY, question TEXT, sql_query TEXT, embedding vector({dim}));"))
        
        # Check if empty
        result = conn.execute(text("SELECT count(*) FROM golden_queries")).scalar()
        if result == 0:
            print(f"🌱 Seeding Golden Queries using {EMBEDDING_PROVIDER} (dim={dim})...")
            for q, sql in INITIAL_GOLDEN_QUERIES:
                vector = embeddings.embed_query(q)
                conn.execute(
                    text("INSERT INTO golden_queries (question, sql_query, embedding) VALUES (:q, :sql, :vec)"),
                    {"q": q, "sql": sql, "vec": str(vector)}
                )
            conn.commit()
            print("✅ Seeding Complete.")

# Run seed on startup
try:
    seed_golden_queries()
except Exception as e:
    print(f"⚠️ Vector Store Seed Failed: {e}")
    if "vector" in str(e) and "does not exist" in str(e):
        print("   -> Hint: Please enable pgvector extension.")
    if "dimension" in str(e):
        print("   -> Hint: You switched embedding models but DB has old vector size. Drop table 'golden_queries'.")


def get_similar_examples(question: str, k=2):
    """Finds similar SQL examples using pgvector cosine distance."""
    try:
        query_vec = embeddings.embed_query(question)
        with engine.connect() as conn:
            stmt = text("SELECT question, sql_query FROM golden_queries ORDER BY embedding <=> :vec LIMIT :k")
            results = conn.execute(stmt, {"vec": str(query_vec), "k": k}).fetchall()
            
        examples_str = ""
        for q, sql in results:
            examples_str += f"- Question: {q}\n  SQL: {sql}\n"
        return examples_str
    except Exception as e:
        print(f"❌ Vector Search Error: {e}")
        return ""

# --- Agent Logic ---

template = """You are a Postgres expert. Given an input question, create a syntactically correct PostgreSQL query to run.
Use the schema and the "Similar Examples" below to guide your answer.

Unless the user specifies a specific number of examples, always limit your query to at most 5 results using the LIMIT clause.
Never query for all columns from a table. You must query only the columns that are needed to answer the question.
Pay attention to use only the column names you can see in the schema description. Be careful to not query for columns that do not exist.
Also, ensure the query is Read-Only.

Only use the following tables:
{table_info}

Similar Examples (Golden Queries):
{examples}

Question: {input}
SQLQuery:"""

prompt_template = PromptTemplate.from_template(template)

def get_sql_chain(question: str):
    # RAG Step: Get Context
    examples = get_similar_examples(question)
    
    # Manual chain: Get Schema -> Format Prompt -> Call LLM
    table_info = db.get_table_info()
    formatted_prompt = prompt_template.format(
        table_info=table_info,
        examples=examples,
        input=question
    )
    response = llm.invoke(formatted_prompt)
    return response.content

def process_user_question(question: str):
    """
    Returns a plan containing the generated SQL and an explanation.
    """
    try:
        generated_sql = get_sql_chain(question)
        clean_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        
        return {
            "status": "success",
            "type": "plan",
            "sql": clean_sql,
            "explanation": f"I found some similar past queries to help me. I will query the 'customer' table."
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Execute function remains unchanged...
def execute_approved_sql(sql_query: str):
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = list(result.keys())
            data = [dict(zip(columns, row)) for row in rows]
            
            if len(rows) == 1 and len(columns) == 1:
                val = rows[0][0]
                if isinstance(val, (int, float)):
                    return {"status": "success", "type": "kpi", "data": {"value": val, "label": columns[0], "sql": sql_query}}

            return {"status": "success", "type": "table", "data": {"columns": list(columns), "rows": data, "sql": sql_query}}

    except Exception as e:
        return {"status": "error", "message": str(e)}
