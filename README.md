# Text-to-SQL Agentic RAG System

## 📝 Project Overview

This project is an **Agentic Retrieval-Augmented Generation (RAG) system** that converts natural language questions into SQL queries, executes them on a database, and returns human-friendly answers. If the generated SQL fails, the system automatically rewrites the question and tries again—an application of the **Self-Healing Agentic Workflow** design pattern.

## 🚀 Simple Use Case

- **Ask a question** about your data in plain English (e.g., "What did Bob order last week?").
- The agent checks if your question is relevant to the database.
- If relevant, it generates an SQL query using a GenAI model, executes it, and explains the result in natural language.
- If the SQL fails, the agent rewrites your question and tries again (up to 3 times).
- If your question is not about the database, you get a witty, funny response!

## ⚙️ How It Works

1. **Relevance Check:**  
   The agent uses a GenAI model to determine if your question is about the database.
2. **SQL Generation:**  
   If relevant, the agent generates an SQL query using the schema and your question.
3. **SQL Execution:**  
   The query is run on a local SQLite database.
4. **Self-Healing:**  
   If the query fails, the agent rewrites your question and tries again (up to 3 attempts).
5. **Human-Readable Answer:**  
   The agent explains the result in plain English.
6. **Funny Response:**  
   If your question is irrelevant, you get a playful reply.

## 🧠 Agentic Flow

Below is the flow diagram of the agentic process:

![Agentic Flow](./flow.png)

- The flow starts with a relevance check.
- If relevant, it proceeds to SQL generation and execution.
- On SQL errors, it attempts to regenerate the query.
- After 3 failed attempts, it ends with a helpful message.
- Irrelevant questions get a funny response.

## 🛠️ Tech Stack

- **Python 3**
- **LangChain** (agentic workflow, prompt chaining)
- **Google Gemini GenAI** (for LLM-powered reasoning and generation)
- **Pydantic** (data validation)
- **SQLAlchemy** (ORM and DB access)
- **SQLite** (local database)
- **Debian GNU/Linux 12 (bookworm)** (dev container)
- **VS Code Dev Containers** (for reproducible development)

## ⚡ Getting Started

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd text-to-sql
```

### 2. Configure the Project

- The project uses a `.env` file for API keys.  
  Make sure your `GOOGLE_API_KEY` is set in `app/agent/.env`.

### 3. Initialize the Database

Before running the agent, **populate the SQLite database with dummy data**:

```sh
cd app
python3 agent/utils.py
```

You should see output confirming the tables and data are created.

### 4. Run the Agent

```sh
python3 run.py
```

Type your questions at the prompt!

---

## 📚 Notes

- The agent is designed for demonstration and educational purposes.
- You can extend the schema and prompts for your own use cases.
- The agentic flow is modular and easy to customize.

---

Enjoy your conversational SQL agent!