# Case Study: Carwash Analytics Chatbot (Query Sense)

> **Transforming raw SQL data into actionable conversational insights for business owners.**

---

## 1. Executive Summary
**Query Sense** is an AI-powered Business Intelligence (BI) tool designed for the Carwash industry. It enables non-technical business owners to query their complex database—covering customers, vehicles, and memberships—using simple natural language.

By leveraging a **3-Layer Search Architecture** (Cache → RAG → LLM), the system delivers answers in milliseconds for common questions while maintaining the flexibility to generate complex SQL for novel queries. The solution features a modern Svelte 5 frontend, a robust FastAPI backend, and a self-learning memory system powered by `pgvector`.

---

## 2. The Challenge

### The Problem
Small business owners often sit on goldmines of data (customer retention rates, churn trends, revenue per site) but lack the technical SQL skills to access it.
*   **Static Dashboards**: Standard dashboards (e.g., "Total Revenue") define metrics rigidly and cannot answer ad-hoc questions like *"Which Tesla owners cancelled their membership last month?"*.
*   **Dependency on Engineers**: Every new report requires a developer ticket, creating a bottleneck.
*   **Complexity**: The underlying schema involves multiple related tables (`customer` ↔ `vehicle` ↔ `membership_account`), making manual joins error-prone.

### The Objective
Build a "Text-to-Insight" engine that is:
1.  **Accessible**: Zero SQL knowledge required.
2.  **Fast**: Instant answers for recurring business questions.
3.  **Safe**: Read-only access with human-in-the-loop verification.
4.  **Visual**: Auto-magically renders data as KPIs, Tables, or Charts based on the result shape.

---

## 3. The Solution: 3-Layer Architecture

To balance cost, speed, and accuracy, we moved away from a purely LLM-based approach to a hybrid architecture.

### Layer 1: Semantic Cache (The Speed Layer)
*   **Technology**: `pgvector` (PostgreSQL) + `all-MiniLM-L6-v2` (Local, Latency: ~10ms).
*   **Logic**: Before calling an AI model, the system embeds the user's question into a 384-dimensional vector. It checks the `golden_queries` table for a semantic match (Cosine Distance < 0.05).
*   **Benefit**: "How much money did we make?" and "Total revenue?" are treated as identical. The SQL is returned instantly, bypassing the LLM cost and latency entirely.

### Layer 2: Retrieval Augmented Generation (The Context Layer)
*   **Technology**: RAG + Vector Search (Latency: ~50ms).
*   **Logic**: If no exact match is found, the system retrieves the top 3 similar past queries (Distance < 0.5) to use as "Few-Shot Examples".
*   **Benefit**: This teaches the LLM how to handle domain-specific nuances (e.g., that "Active Member" means `status = 1`) without needing fine-tuning.

### Layer 3: Generative AI (The Reasoning Layer)
*   **Technology**: Google Gemini 2.5 Flash (Latency: ~800ms).
*   **Logic**: The LLM receives a prompt containing:
    1.  The sanitized Database Schema.
    2.  The RAG Examples (from Layer 2).
    3.  The Conversation History (Last 3 turns).
    4.  The User's Question.
*   **Benefit**: It generates a syntactically correct, optimized SQL query for completely new questions.

---

## 4. Key Features

### 🧠 Context-Aware Conversations
The bot remembers context.
> **User**: "How many customers do we have?"
> **Bot**: "25,403 Customers."
> **User**: "How many of **them** are active?"
> **Bot**: *Understands "them" refers to customers and filters by `active = True`.*

### 📊 Intelligent Visualization
The backend analyzes the SQL result shape to determine the best UI component:
*   **Single Number** → Big KPI Card.
*   **2 Columns (Label + Metric)** → Bar Chart.
*   **Time Series** → Line Chart.
*   **Complex Data** → Sortable Data Table.

### 🛡️ Resilience & Safety
*   **Human-in-the-Loop**: The bot proposes a plan ("I will select count from...") which the user must click to "Proceed".
*   **Read-Only Role**: The database connection is restricted to `SELECT` permissions.
*   **Self-Healing**: If the LLM generates bad SQL, the system catches the error, feeds it back to the LLM, and retries (Auto-Correction).

---

## 5. Technology Stack

| Component | Tech Choices | Reasoning |
| :--- | :--- | :--- |
| **Frontend** | **Svelte 5** + TailwindCSS | High performance, small bundle size, and reactive state management for real-time chat. |
| **Backend** | **FastAPI** (Python 3.10) | Async capabilities for handling concurrent LLM/DB requests efficiently. |
| **Database** | **PostgreSQL 16** | Robust relational data storage combined with Vector Search via `pgvector` extension. |
| **AI Model** | **Gemini 2.5 Flash** | Excellent performance-to-cost ratio for SQL generation tasks. |
| **Infrastructure** | **Docker Compose** | Easy local replication of the entire stack (DB, API, frontend). |
| **Caching** | **Redis** | API rate limiting and stats tracking. |

---

## 6. Results & Impact
*   **90% Latency Reduction**: For recurring questions, response time dropped from 1.5s (LLM) to < 20ms (Cache).
*   **Zero-Cost "Memory"**: By running embeddings locally on the CPU (HuggingFace), the Semantic Cache incurs no API costs.
*   **Democratization**: Business owners can now answer complex questions like *"Show me the top 5 customers by revenue who drive a Ford"* in seconds, without writing a single line of code.

---

## 7. Future Roadmap
*   **Phase 3**: Multi-table analytics (joining 4+ tables).
*   **Phase 4**: Automated Alerts (e.g., "Notify me if churn exceeds 5%").
*   **Phase 5**: Voice Interface (Speech-to-SQL).
