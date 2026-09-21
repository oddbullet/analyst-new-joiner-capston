HIGH_SEVERITY_KEYWORDS = ["down", "outage", "critical", "all customers", "production"]
MEDIUM_SEVERITY_KEYWORDS = ["login", "cannot", "error", "failed", "slow"]


def classify_severity(text: str) -> str:
    """
    Classify the severity of a support ticket.
    Returns: "low", "medium", or "high"
    Raises: nothing — returns "low" for empty/None input
    """
    if not text:
        print("Warning: classify_severity received empty/None input, defaulting to 'low'")
        return "low"

    normalized_text = text.lower()

    if any(keyword in normalized_text for keyword in HIGH_SEVERITY_KEYWORDS):
        return "high"
    if any(keyword in normalized_text for keyword in MEDIUM_SEVERITY_KEYWORDS):
        return "medium"
    return "low"


def classify_severity_node(state: dict) -> dict:
    """
    LangGraph node that classifies ticket severity.
    Reads "text" from state, classifies it, and stores the result under "severity".
    """
    state["severity"] = classify_severity(state.get("text"))
    return state


def classify_category(text: str) -> str:
    """
    Classify the category of a support ticket.
    Returns: "bug", "feature_request", "billing", "access_request", or "other"
    """
    raise NotImplementedError
