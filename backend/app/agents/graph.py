from langgraph.graph import StateGraph, END
from app.agents.nodes import (
    ComplaintState,
    extract_fields_node,
    completeness_check_node,
    duplicate_check_node,
    risk_classification_node,
    root_cause_capa_node,
    summary_node,
)


def build_graph():
    workflow = StateGraph(ComplaintState)

    workflow.add_node("extract_fields", extract_fields_node)
    workflow.add_node("completeness_check", completeness_check_node)
    workflow.add_node("duplicate_check", duplicate_check_node)
    workflow.add_node("risk_classification", risk_classification_node)
    workflow.add_node("root_cause_capa", root_cause_capa_node)
    workflow.add_node("summary", summary_node)

    workflow.set_entry_point("extract_fields")
    workflow.add_edge("extract_fields", "completeness_check")
    workflow.add_edge("completeness_check", "duplicate_check")
    workflow.add_edge("duplicate_check", "risk_classification")
    workflow.add_edge("risk_classification", "root_cause_capa")
    workflow.add_edge("root_cause_capa", "summary")
    workflow.add_edge("summary", END)

    return workflow.compile()


complaint_graph = build_graph()