import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from sqlalchemy import text
from .db import engine

load_dotenv()

# --- Configuration ---
# Use the high-performance Flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0, 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

db = SQLDatabase(engine, include_tables=['customer'])

# --- RAG: Golden Queries ---
# Simple In-Memory "Vector Store" logic for MVP using pgvector directly is robust.
# But for speed, we will use a raw SQL approach with pgvector extension we just enabled.

INITIAL_GOLDEN_QUERIES = [
    ("How many customers do we have?", "SELECT count(*) FROM customer;"),
    ("Who are the active customers?", "SELECT first_name, last_name, email FROM customer WHERE active = true LIMIT 10;"),
    ("Show me customers from store 1.", "SELECT * FROM customer WHERE store_id = 1 LIMIT 5;")
]

def seed_golden_queries():
    """Hashes and seeds queries if table is empty."""
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS golden_queries (id SERIAL PRIMARY KEY, question TEXT, sql_query TEXT, embedding vector(768));"))
        # Check if empty
        result = conn.execute(text("SELECT count(*) FROM golden_queries")).scalar()
        if result == 0:
            print("Seeding Golden Queries...")
            for q, sql in INITIAL_GOLDEN_QUERIES:
                # Generate embedding
                vector = embeddings.embed_query(q)
                conn.execute(
                    text("INSERT INTO golden_queries (question, sql_query, embedding) VALUES (:q, :sql, :vec)"),
                    {"q": q, "sql": sql, "vec": str(vector)}
                )
            conn.commit()

# Run seed on startup (safe to run multiple times due to check)
try:
    seed_golden_queries()
except Exception as e:
    print(f"Warning: Vector Store Seed Failed (pgvector might not be ready): {e}")

def get_similar_examples(question: str, k=2):
    """Finds similar SQL examples using pgvector cosine distance."""
    try:
        query_vec = embeddings.embed_query(question)
        with engine.connect() as conn:
            # <=> is cosine distance operator in pgvector
            stmt = text("SELECT question, sql_query FROM golden_queries ORDER BY embedding <=> :vec LIMIT :k")
            results = conn.execute(stmt, {"vec": str(query_vec), "k": k}).fetchall()
            
        examples_str = ""
        for q, sql in results:
            examples_str += f"- Question: {q}\n  SQL: {sql}\n"
        return examples_str
    except Exception as e:
        print(f"Vector Search Error: {e}")
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

def execute_approved_sql(sql_query: str):
    """
    Executes the SQL and attempts to Format it intelligently (KPI vs Table).
    """
    try:
        # We need raw results to format them
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = list(result.keys())
            
            # Smart Formatting Logic
            data = [dict(zip(columns, row)) for row in rows]
            
            # 1. KPI Mode: Single Row, Single Column (numeric)
            if len(rows) == 1 and len(columns) == 1:
                val = rows[0][0]
                if isinstance(val, (int, float)):
                    return {
                        "status": "success",
                        "type": "kpi",
                        "data": {
                            "value": val,
                            "label": columns[0],
                            "sql": sql_query
                        }
                    }

            # 2. Table Mode: Everything else
            return {
                "status": "success",
                "type": "table",
                "data": {
                    "columns": list(columns),
                    "rows": data, # List of dicts
                    "sql": sql_query
                }
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
