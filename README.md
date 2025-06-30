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


## ⚠️ Limitations

### Semantic Mismatch Example

A common failure in SQL-based LLM agents is when the generated SQL is **syntactically valid but semantically wrong**—the query "works" but doesn't match the user's intent.

**Example:**
```
[User]: List all users with more than two products in their cart

[SQL generated]:
SELECT T1.name, T1.email 
FROM User AS T1 
JOIN Orders AS T2 ON T1.id = T2.user_id 
JOIN OrderItem AS T3 ON T2.id = T3.order_id 
GROUP BY T1.id, T1.name, T1.email 
HAVING COUNT(DISTINCT T3.product_id) > 2
```
❌ **Mismatch with User Intent:**  
The user asked about the "cart" (implying a temporary, not-yet-ordered selection), but the schema has no cart table. The LLM mapped "cart" to "orders + order_items", which is not what the user meant.

**Why This Didn’t Trigger a Retry:**  
- The SQL is valid and returns results.
- The LLM "guessed" the intent, but the answer is semantically different.

### Approaches to Reduce Semantic Hallucinations

1. **LLM-Judge Node**  
   After generating SQL, an LLM validates if the query makes semantic sense given the schema. `(convert_to_sql → validate_sql_semantics → execute_sql)`
   - **Pros:** Catches invalid joins/misuse, can prevent bad execution.
   - **Cons:** LLM still hallucinates first (late catch), extra LLM call per query, needs schema context again.

2. **Retrieval-Augmented Schema Semantics**  
   Retrieve natural-language explanations of schema/relationships before SQL generation. `user query → retrieve explanations → convert_to_sql → execute_sql`
   - **Pros:** Helps LLM avoid hallucinations up front, smarter/cheaper prompt, generalizes to new schemas.
   - **Cons:** Requires maintaining/updating explanation docs, needs vector DB or retriever infra.

**Note:**  
This project currently does not implement these advanced mitigation strategies, so semantic mismatches may occur in complex or ambiguous queries.


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