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


BILLING_CATEGORY_KEYWORDS = ["invoice", "charge", "billing", "payment", "refund", "subscription"]
ACCESS_REQUEST_CATEGORY_KEYWORDS = ["access", "permission", "locked out", "password reset"]
BUG_CATEGORY_KEYWORDS = ["bug", "crash", "broken", "not working", "fails", "error"]
FEATURE_REQUEST_CATEGORY_KEYWORDS = ["feature request", "would like", "enhancement", "please add"]


def classify_category(text: str) -> str:
    """
    Classify the category of a support ticket.
    Returns: "bug", "feature_request", "billing", "access_request", or "other"
    Raises: nothing — returns "other" for empty/None input
    """
    if not text:
        print("Warning: classify_category received empty/None input, defaulting to 'other'")
        return "other"

    normalized_text = text.lower()

    if any(keyword in normalized_text for keyword in BILLING_CATEGORY_KEYWORDS):
        return "billing"
    if any(keyword in normalized_text for keyword in ACCESS_REQUEST_CATEGORY_KEYWORDS):
        return "access_request"
    if any(keyword in normalized_text for keyword in BUG_CATEGORY_KEYWORDS):
        return "bug"
    if any(keyword in normalized_text for keyword in FEATURE_REQUEST_CATEGORY_KEYWORDS):
        return "feature_request"
    return "other"


def classify_category_node(state: dict) -> dict:
    """
    LangGraph node that classifies ticket category.
    Reads "text" from state, classifies it, and stores the result under "category".
    """
    state["category"] = classify_category(state.get("text"))
    return state
