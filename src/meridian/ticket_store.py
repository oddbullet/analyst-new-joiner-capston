import json
import sqlite3
import uuid
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "tickets.db"


class TicketNotFoundError(Exception):
    pass


@contextmanager
def _connect():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("CREATE TABLE IF NOT EXISTS tickets (id TEXT PRIMARY KEY, data TEXT NOT NULL)")
        with conn:
            yield conn
    finally:
        conn.close()


def save_ticket(ticket: dict) -> str:
    """Save a ticket dict and return its generated ID."""
    ticket_id = str(uuid.uuid4())
    with _connect() as conn:
        conn.execute(
            "INSERT INTO tickets (id, data) VALUES (?, ?)",
            (ticket_id, json.dumps(ticket)),
        )
    return ticket_id


def get_ticket(ticket_id: str) -> dict:
    """Retrieve a ticket by ID. Raises TicketNotFoundError if not found."""
    with _connect() as conn:
        row = conn.execute("SELECT data FROM tickets WHERE id = ?", (ticket_id,)).fetchone()

    if row is None:
        raise TicketNotFoundError(f"Ticket not found: {ticket_id}")
    return json.loads(row[0])


def persist_ticket_node(state: dict) -> dict:
    """
    LangGraph node that saves the ticket and stores the generated ID.
    Saves the current state as the ticket, and stores the result under "ticket_id".
    """
    state["ticket_id"] = save_ticket(dict(state))
    return state
