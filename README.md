# Carwash Analytics Chatbot 🚗💧

A RAG-enhanced Business Intelligence bot that allows carwash owners to query their data using natural language. Built with **FastAPI**, **Svelte**, **PostgreSQL (pgvector)**, and **Google Gemini**.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Svelte](https://img.shields.io/badge/svelte-5.0-orange.svg)

## ✨ Features
*   **Natural Language to SQL**: Ask "How many active customers do we have?" and get real data.
*   **Human-in-the-Loop**: The bot proposes a plan (SQL), and you approve it.
*   **Smart Dashboard**: 
    *   **KPI Cards**: Big stats for important numbers.
    *   **Data Tables**: Clean formatting for lists.
    *   **Suggestion Chips**: Quick shortcuts for common business questions.
*   **Secure**: Runs with a Read-Only database user.

## 🛠 Tech Stack
*   **Backend**: FastAPI, LangChain, Google Gemini 2.5 Flash
*   **Frontend**: Svelte 5, TailwindCSS
*   **Database**: PostgreSQL 16 + `pgvector`
*   **Infrastructure**: Docker Compose

## 🚀 Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Node.js 18+
*   Python 3.10+
*   Google Gemini API Key

### 1. Database Setup
Start the local PostgreSQL instance with pgvector:
```bash
docker-compose up -d
```
*Port mapping: Host `5433` -> Container `5432` (to avoid conflicts).*

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Secrets
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173` to access the dashboard.

## 🧠 Architecture
1.  **User asks question** -> FastAPI Endpoint
2.  **Agent Logic (`agent.py`)**:
    *   (Optional) Searches `pgvector` for similar past queries (RAG).
    *   Prompts Gemini with Schema + Examples.
    *   Returns a **Plan** (SQL + Explanation).
3.  **User approves logic**.
4.  **Agent executes SQL** on Postgres (Read-Only).
5.  **Smart Formatting**: Results are returned as KPI, Table, or Text.

## 📝 License
MIT
