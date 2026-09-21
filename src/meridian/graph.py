from typing import TypedDict

from langgraph.graph import StateGraph, END

from meridian.ticket_classifier import classify_severity_node


class TicketState(TypedDict, total=False):
    text: str
    severity: str


def build_graph():
    """Build the ticket-processing LangGraph."""
    graph = StateGraph(TicketState)
    graph.add_node("classify_severity", classify_severity_node)
    graph.set_entry_point("classify_severity")
    graph.add_edge("classify_severity", END)
    return graph.compile()


def run_graph(text: str) -> TicketState:
    """Run the ticket-processing graph on a single ticket's text."""
    app = build_graph()
    return app.invoke({"text": text})
