import uuid

import pytest

from src.meridian.ticket_store import TicketNotFoundError, get_ticket, save_ticket


# --- Save and retrieve ---

def test_save_and_get_ticket_returns_same_ticket():
    ticket = {"title": "Cannot log in", "description": "Login page returns 500", "severity": "high"}

    ticket_id = save_ticket(ticket)
    retrieved = get_ticket(ticket_id)

    assert retrieved == ticket


def test_save_ticket_returns_a_string_id():
    ticket = {"title": "Blurry logo", "description": "Logo looks pixelated", "severity": "low"}

    ticket_id = save_ticket(ticket)

    assert isinstance(ticket_id, str)
    assert ticket_id != ""


# --- Unique IDs ---

def test_two_different_tickets_get_different_ids():
    ticket_a = {"title": "Billing issue", "description": "Overcharged", "severity": "medium"}
    ticket_b = {"title": "Site down", "description": "500 error on homepage", "severity": "high"}

    id_a = save_ticket(ticket_a)
    id_b = save_ticket(ticket_b)

    assert id_a != id_b


# --- Unknown ID ---

def test_get_ticket_with_unknown_id_raises_ticket_not_found_error():
    unknown_id = str(uuid.uuid4())

    with pytest.raises(TicketNotFoundError):
        get_ticket(unknown_id)


# --- Contents match exactly ---

def test_retrieved_ticket_matches_original_contents_exactly():
    ticket = {
        "title": "Password reset email not arriving",
        "description": "User requested a reset link three times, none arrived",
        "severity": "medium",
        "category": "account",
    }

    ticket_id = save_ticket(ticket)
    retrieved = get_ticket(ticket_id)

    assert retrieved == ticket
    assert set(retrieved.keys()) == set(ticket.keys())
    for key, value in ticket.items():
        assert retrieved[key] == value
