import pytest

from src.meridian import ticket_store

TEMP_DB_PATH = ticket_store.DB_PATH.parent / "temp.db"


@pytest.fixture(autouse=True)
def use_temp_db(monkeypatch):
    """Point ticket_store at a throwaway SQLite db so tests never touch tickets.db."""
    monkeypatch.setattr(ticket_store, "DB_PATH", TEMP_DB_PATH)


@pytest.fixture(scope="session", autouse=True)
def clean_temp_db():
    TEMP_DB_PATH.unlink(missing_ok=True)
    yield
    TEMP_DB_PATH.unlink(missing_ok=True)
