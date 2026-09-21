import pytest

from src.meridian.ticket_router import route_ticket

VALID_TEAMS = {"tier-2-escalation", "billing-team", "tier-1-support"}


# --- Happy path tests ---

def test_high_severity_billing_returns_tier_2_escalation():
    assert route_ticket("high", "billing") == "tier-2-escalation"


def test_high_severity_technical_returns_tier_2_escalation():
    assert route_ticket("high", "technical") == "tier-2-escalation"


def test_medium_severity_billing_returns_billing_team():
    assert route_ticket("medium", "billing") == "billing-team"


def test_low_severity_billing_returns_billing_team():
    assert route_ticket("low", "billing") == "billing-team"


def test_low_severity_technical_returns_tier_1_support():
    assert route_ticket("low", "technical") == "tier-1-support"


# --- Unknown/edge case values ---

def test_unknown_severity_and_category_returns_tier_1_support():
    assert route_ticket("unknown", "unknown") == "tier-1-support"


def test_unknown_severity_with_billing_returns_billing_team():
    assert route_ticket("unknown", "billing") == "billing-team"


def test_medium_severity_with_unknown_category_returns_tier_1_support():
    assert route_ticket("medium", "unknown") == "tier-1-support"


# --- Does not raise exceptions ---

def test_does_not_raise_on_unknown_values():
    try:
        route_ticket("unknown", "unknown")
    except Exception as e:
        pytest.fail(f"route_ticket raised an exception: {e}")


def test_does_not_raise_on_none_values():
    try:
        route_ticket(None, None)
    except Exception as e:
        pytest.fail(f"route_ticket raised an exception: {e}")


# --- Return type/value contract ---

def test_returns_valid_team_name():
    result = route_ticket("high", "billing")
    assert result in VALID_TEAMS


def test_deterministic_same_input_same_output():
    first = route_ticket("high", "technical")
    second = route_ticket("high", "technical")
    third = route_ticket("high", "technical")
    assert first == second == third
