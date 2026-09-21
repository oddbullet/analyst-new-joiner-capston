def route_ticket(severity: str, category: str) -> str:
    """
    Route a ticket to the appropriate support team.
    Returns: team name string
    Routing rules:
      - severity "high": always "tier-2-escalation"
      - category "billing": "billing-team"
      - all others: "tier-1-support"
    """
    if severity == "high":
        return "tier-2-escalation"
    if category == "billing":
        return "billing-team"
    return "tier-1-support"


def route_ticket_node(state: dict) -> dict:
    """
    LangGraph node that routes a ticket to a support team.
    Reads "severity" and "category" from state, and stores the result under "team".
    """
    state["team"] = route_ticket(state.get("severity"), state.get("category"))
    return state
