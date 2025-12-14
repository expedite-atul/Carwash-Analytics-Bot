# Carwash Analytics Bot - Implementation Plan

## Goal
Transform the MVP into a scalable, secure, and modern Business Intelligence application with Role-Based Access Control (RBAC), high-performance caching (Redis), and comprehensive administration capabilities.

## Architecture (Phase 2)
*   **Frontend**: Svelte 5 + TailwindCSS + Vite (Single Page App with Routing)
*   **Backend**: FastAPI (Python 3.10+)

## Roadmap & TODOs
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
