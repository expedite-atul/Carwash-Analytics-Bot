# Carwash Analytics Bot - Implementation Plan & Roadmap

## 🎯 Goal
Build a **Production-Grade Business Intelligence Bot** for Carwash Owners that allows natural language querying of business data using **Recall-Augmented Text-to-SQL**.

## 🏗 Architecture
*   **Infrastructure**: Docker Compose (Postgres 16 + pgvector)
*   **Backend**: FastAPI (Python 3.10+)
*   **AI Engine**: Google Gemini 2.5 Flash + LangChain
*   **Frontend**: Svelte 5 + TailwindCSS
*   **Database**: PostgreSQL with `pgvector` for RAG capabilities.

---

## ✅ MVP Features (Completed)
### 1. Robust Text-to-SQL Engine
*   [x] **Schema Pruning**: Dynamically exposes relevant tables (currently `customer`) to the LLM.
*   [x] **Read-Only Safety**: Uses a specific `bot_reader` database user with strictly limited permissions.
*   [x] **Human-in-the-Loop**: Generates an SQL "Plan" for user review before execution.

### 2. Business Dashboard UI
*   [x] **Suggestion Chips**: One-click access to common queries (Revenue, Churn, Active Users).
*   [x] **Smart Rendering**:
    *   **KPI Cards**: Automatically detects single-value metrics and displays them as big stat cards.
    *   **Data Tables**: Renders row data in clean, striped HTML tables.
    *   **Collapsible SQL**: Maintains trust by allowing users to inspect the generated SQL if desired.

### 3. Infrastructure
*   [x] Dockerized PostgreSQL with `pgvector` pre-configured.
*   [x] Automated `init.sql` for user permission management.

---

## 🚀 Roadmap & TODOs
### Phase 2: RAG & Memory (In Progress)
The `pgvector` infrastructure is ready. The next step is to enable "Memory" so the bot learns from correct queries.
- [ ] **Golden Query Seeder**: Populate `golden_queries` table with vetted Q&A pairs.
- [ ] **Vector Search**: Implement cosine similarity search to inject "Similar Past Queries" into the prompt.
    - *Note: Base logic is implemented in `agent.py`, pending API Rate Limit resolution for seeding.*

### Phase 3: Advanced Analytics
- [ ] **Multi-Table Joins**: Expand schema pruning to include `transactions`, `wash_packages`, and `employees`.
- [ ] **Chart Generation**: Return data suitable for Chart.js/Recharts (Line/Bar charts for revenue over time).

### Phase 4: Production Hardening
- [ ] **Auth**: Implement simple JWT Authentication for the Dashboard.
- [ ] **CI/CD**: GitHub Actions workflow for linting and testing.
