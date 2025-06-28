from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .state import AgentState
from .utils import get_database_schema, SessionLocal
from pydantic import BaseModel, Field
from langchain_core.runnables.config import RunnableConfig
from sqlalchemy import text

# Relevance check
class CheckRelevance(BaseModel):
    relevance: str = Field(...)


def check_relevance(state: AgentState, config: RunnableConfig):
    print("🔎 Checking relevance of the question...")
    question = state["question"]
    schema = get_database_schema()
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are an assistant that checks if a user question is related to this database schema:\n{schema}\nRespond only with 'relevant' or 'not_relevant'."),
        ("user", f"Question: {question}")
    ])
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    checker = prompt | llm.with_structured_output(CheckRelevance)
    state["relevance"] = checker.invoke({}).relevance
    print(f"✅ Relevance check result: {state['relevance']}")
    return state


class ConvertToSQL(BaseModel):
    sql_query: str = Field(
        description="The SQL query corresponding to the user's natural language question."
    )

def convert_nl_to_sql(state: AgentState, config: RunnableConfig):
    print("📝 Converting natural language to SQL...")
    question = state["question"]
    schema = get_database_schema()
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"Convert natural language question to SQL based on this schema:\n{schema}\nOnly return SQL."),
        ("human", f"Question: {{question}}")
    ])
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    generator = prompt | llm.with_structured_output(ConvertToSQL)
    state["sql_query"] = generator.invoke({"question": question}).sql_query
    print(f"✅ SQL generated: {state['sql_query']}")
    return state

def execute_sql(state: AgentState):
    print("🚀 Executing SQL query...")
    session = SessionLocal()
    sql_query = state["sql_query"]
    try:
        result = session.execute(text(sql_query))
        if sql_query.strip().lower().startswith("select"):
            rows = result.fetchall()
            columns = result.keys()
            state["query_rows"] = [dict(zip(columns, row)) for row in rows]
            formatted = "\n".join([str(r) for r in state["query_rows"]])
            state["query_result"] = formatted or "No results found."
            print(f"📊 Query returned {len(state['query_rows'])} rows.")
        else:
            session.commit()
            state["query_result"] = "Query executed successfully."
            print("✅ Non-select query executed successfully.")
        state["sql_error"] = False
    except Exception as e:
        state["query_result"] = str(e)
        state["sql_error"] = True
        print(f"❌ SQL execution error: {e}")
    finally:
        session.close()
    return state

def generate_human_readable_answer(state: AgentState):
    print("💬 Generating human-readable answer...")
    #If you want to use variables in the prompt, you should use {variable} and pass them as parameters to .invoke().
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Convert SQL query result to natural language explanation."),
        ("human", f"Query: {{sql_query}}\nResult: {{query_result}}")
    ])
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    parser = prompt | llm | StrOutputParser()
    state["query_result"] = parser.invoke({
        "sql_query": state["sql_query"],
        "query_result": state["query_result"]
    })
    print("✅ Human-readable answer generated.")
    return state


class RewrittenQuestion(BaseModel):
    question: str = Field(description="The rewritten question.")

def regenerate_query(state: AgentState):
    print("🔄 Retrying to generate SQL query...")
    print("Retrying to generate SQL query")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Rewrite the question for better SQL generation."),
        ("human", f"Original Question: {state['question']}")
    ])
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    rewriter = prompt | llm.with_structured_output(RewrittenQuestion)
    rewritten = rewriter.invoke({})
    state["question"] = rewritten.question
    state["attempts"] += 1
    print(f"✏️ Rewritten question: {state['question']} (Attempt {state['attempts']})")
    return state

def generate_funny_response(state: AgentState):
    print("😅 Generating a funny response for irrelevant question...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Be a witty assistant."),
        ("human", "That question isn't about a database, but maybe you're hungry?")
    ])
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
    joke = prompt | llm | StrOutputParser()
    state["query_result"] = joke.invoke({})
    print("🎉 Funny response generated.")
    return state

def end_max_iterations(state: AgentState):
    print("🛑 Maximum attempts reached.")
    state["query_result"] = "Tried too many times. Please rephrase your question."
    return state

def relevance_router(state: AgentState):
    return "convert_to_sql" if state["relevance"].lower() == "relevant" else "generate_funny_response"

def execute_sql_router(state: AgentState):
    return "generate_human_readable_answer" if not state["sql_error"] else "regenerate_query"

def check_attempts_router(state: AgentState):
    return "convert_to_sql" if state["attempts"] < 3 else "end_max_iterations"



# Similarly include:
# - convert_nl_to_sql
# - execute_sql
# - generate_human_readable_answer
# - regenerate_query
# - generate_funny_response
# - end_max_iterations
# - router functions
