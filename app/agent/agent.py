from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes import (
    check_relevance,
    convert_nl_to_sql,
    execute_sql,
    generate_human_readable_answer,
    regenerate_query,
    generate_funny_response,
    end_max_iterations,
    relevance_router,
    execute_sql_router,
    check_attempts_router,
)

def build_agent():
    workflow = StateGraph(AgentState)
    workflow.set_entry_point("check_relevance")

    workflow.add_node("check_relevance", check_relevance)
    workflow.add_node("convert_to_sql", convert_nl_to_sql)
    workflow.add_node("execute_sql", execute_sql)
    workflow.add_node("generate_human_readable_answer", generate_human_readable_answer)
    workflow.add_node("regenerate_query", regenerate_query)
    workflow.add_node("generate_funny_response", generate_funny_response)
    workflow.add_node("end_max_iterations", end_max_iterations)

    workflow.add_conditional_edges("check_relevance", relevance_router, {
        "convert_to_sql": "convert_to_sql",
        "generate_funny_response": "generate_funny_response",
    })
    workflow.add_edge("convert_to_sql", "execute_sql")
    workflow.add_conditional_edges("execute_sql", execute_sql_router, {
        "generate_human_readable_answer": "generate_human_readable_answer",
        "regenerate_query": "regenerate_query",
    })
    workflow.add_conditional_edges("regenerate_query", check_attempts_router, {
        "convert_to_sql": "convert_to_sql",
        "end_max_iterations": "end_max_iterations",
    })

    workflow.add_edge("generate_human_readable_answer", END)
    workflow.add_edge("generate_funny_response", END)
    workflow.add_edge("end_max_iterations", END)

    return workflow.compile()
