from datetime import date

import pytest

from app.rules import assess_retention, calculate_expiry


def test_expiry_uses_calendar_days() -> None:
    assert calculate_expiry(date(2024, 2, 28), 2) == date(2024, 3, 1)


def test_overdue_record_requires_human_decision() -> None:
    result = assess_retention(date(2026, 1, 1), 30, date(2026, 2, 5))
    assert result.state == "overdue"
    assert result.days_remaining == -5
    assert "insan kararı" in result.reason


def test_seven_day_boundary_is_review_due() -> None:
    result = assess_retention(date(2026, 1, 1), 30, date(2026, 1, 24))
    assert result.state == "review_due"
    assert result.days_remaining == 7


def test_non_positive_retention_is_rejected() -> None:
    with pytest.raises(ValueError):
        calculate_expiry(date.today(), 0)
