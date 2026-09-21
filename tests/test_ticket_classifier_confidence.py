import pytest

from src.meridian.ticket_classifier import classify_severity

VALID_SEVERITIES = {"low", "medium", "high"}


# --- Story 4: confidence scoring ---

def test_high_severity_confidence():
    label, confidence = classify_severity("production database is down, 500 users affected")
    assert label == "high"
    assert confidence >= 0.8


def test_medium_severity_classification():
    label, confidence = classify_severity("I cannot login to the website")
    assert label == "medium"
    assert 0.0 <= confidence <= 1.0


def test_low_severity_classification():
    label, confidence = classify_severity("The logo looks blurry when I open the website")
    assert label == "low"
    assert 0.0 <= confidence <= 1.0


def test_ambiguous_ticket_confidence():
    _, confidence = classify_severity("Something seems off")
    assert confidence < 0.6


# --- Confidence range validation ---

@pytest.mark.parametrize(
    "text",
    [
        "production database is down, 500 users affected",
        "I cannot login to the website",
        "The logo looks blurry when I open the website",
        "Something seems off",
        "",
        None,
        "ajdsfl;jdsf",
        "down, failed, slowed",
    ],
)
def test_confidence_always_between_zero_and_one(text):
    _, confidence = classify_severity(text)
    assert isinstance(confidence, float)
    assert 0.0 <= confidence <= 1.0


# --- Edge cases ---

def test_empty_string_handling():
    label, confidence = classify_severity("")
    assert label == "low"
    assert 0.0 <= confidence <= 1.0


def test_none_handling():
    label, confidence = classify_severity(None)
    assert label == "low"
    assert 0.0 <= confidence <= 1.0


def test_none_does_not_raise():
    try:
        classify_severity(None)
    except Exception as e:
        pytest.fail(f"classify_severity(None) raised an exception: {e}")


# --- Deterministic behavior ---

def test_deterministic_same_input_same_output():
    text = "production database is down, 500 users affected"
    first = classify_severity(text)
    second = classify_severity(text)
    third = classify_severity(text)
    assert first == second == third


def test_deterministic_ambiguous_input():
    text = "Something seems off"
    first = classify_severity(text)
    second = classify_severity(text)
    assert first == second