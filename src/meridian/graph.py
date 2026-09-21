from typing import TypedDict

from langgraph.graph import StateGraph, END

from meridian.ticket_classifier import classify_severity_node, classify_category_node
from meridian.ticket_router import route_ticket_node
from meridian.ticket_store import persist_ticket_node


class TicketState(TypedDict, total=False):
    text: str
    severity: str
    category: str
    team: str
    ticket_id: str


def build_graph():
    """Build the ticket-processing LangGraph."""
    graph = StateGraph(TicketState)
    graph.add_node("classify_severity", classify_severity_node)
    graph.add_node("classify_category", classify_category_node)
    graph.add_node("route_ticket", route_ticket_node)
    graph.add_node("persist_ticket", persist_ticket_node)
    graph.set_entry_point("classify_severity")
    graph.add_edge("classify_severity", "classify_category")
    graph.add_edge("classify_category", "route_ticket")
    graph.add_edge("route_ticket", "persist_ticket")
    graph.add_edge("persist_ticket", END)
    return graph.compile()


def run_graph(text: str) -> TicketState:
    """Run the ticket-processing graph on a single ticket's text."""
    app = build_graph()
    return app.invoke({"text": text})
