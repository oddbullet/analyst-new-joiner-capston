import pytest

from src.meridian.ticket_classifier import classify_severity

VALID_SEVERITIES = {"low", "medium", "high"}


# --- Happy path tests ---

def test_high_severity_example():
    assert classify_severity("Our website is down for all customers") == "high"


def test_medium_severity_example():
    assert classify_severity("I cannot login to the website") == "medium"


def test_low_severity_example():
    assert classify_severity("The logo looks blurry when I open the website") == "low"


# --- Edge cases ---

def test_empty_string_returns_low():
    assert classify_severity("") == "low"


def test_empty_string_logs_warning(capsys):
    classify_severity("")
    captured = capsys.readouterr()
    assert captured.out != "" or captured.err != ""


def test_none_returns_low():
    assert classify_severity(None) == "low"


def test_none_does_not_raise():
    try:
        classify_severity(None)
    except Exception as e:
        pytest.fail(f"classify_severity(None) raised an exception: {e}")


# --- Deterministic behavior ---

def test_deterministic_same_input_same_output():
    text = "I cannot login to the website"
    first = classify_severity(text)
    second = classify_severity(text)
    third = classify_severity(text)
    assert first == second == third


# --- Unknown/random input ---

def test_random_text_returns_valid_severity():
    result = classify_severity("ajdsfl;jdsf")
    assert result in VALID_SEVERITIES


def test_unrelated_text_returns_valid_severity():
    result = classify_severity("What is the weather?")
    assert result in VALID_SEVERITIES
