# Carwash Analytics Bot - Implementation Plan

## Goal
Transform the MVP into a scalable, secure, and modern Business Intelligence application with Role-Based Access Control (RBAC), high-performance caching (Redis), and comprehensive administration capabilities.

## Architecture (Phase 2)
*   **Frontend**: Svelte 5 + TailwindCSS + Vite (Single Page App with Routing)
*   **Backend**: FastAPI (Python 3.10+)

## Roadmap & TODOs
### Phase 2: RAG & Memory (Completed)
The `pgvector` infrastructure is mature and fully integrated.
- [x] **Golden Query Seeder**: Populates `golden_queries` table ensuring vectors are ready on startup.
- [x] **Vector Search**: RAG implementation active in `agent.py` using `sqlmodel`.
- [x] **Context Awareness**: Multi-turn conversation support via history injection.

### Phase 2.5: Stability & Performance (Completed)
- [x] **Frontend Resilience**: Unique UUIDs for messages and robust Chart fallback logic.
- [x] **Backend Optimization**: Database Indexes + Limit 50 on History Fetch.
- [x] **Performance Logging**: Granular timing logs for per-request latency analysis.

### Phase 3: Advanced Analytics
- [ ] **Multi-Table Joins**: Expand schema pruning to include `transactions`, `wash_packages`, and `employees`.
- [ ] **Chart Generation**: Return data suitable for Chart.js/Recharts (Line/Bar charts for revenue over time).

### Phase 4: Production Hardening
- [ ] **Auth**: Implement simple JWT Authentication for the Dashboard.
- [ ] **CI/CD**: GitHub Actions workflow for linting and testing.
