from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class RetentionAssessment:
    expires_on: date
    days_remaining: int
    state: str
    reason: str


def calculate_expiry(collected_on: date, retention_days: int) -> date:
    if retention_days <= 0:
        raise ValueError("Saklama süresi sıfırdan büyük olmalıdır.")
    return collected_on + timedelta(days=retention_days)


def assess_retention(collected_on: date, retention_days: int, as_of: date) -> RetentionAssessment:
    expires_on = calculate_expiry(collected_on, retention_days)
    remaining = (expires_on - as_of).days
    if remaining < 0:
        return RetentionAssessment(
            expires_on,
            remaining,
            "overdue",
            f"Saklama süresi {-remaining} gün önce doldu; insan kararı gerekiyor.",
        )
    if remaining <= 7:
        return RetentionAssessment(
            expires_on,
            remaining,
            "review_due",
            f"Saklama süresinin dolmasına {remaining} gün kaldı.",
        )
    return RetentionAssessment(
        expires_on,
        remaining,
        "active",
        f"Kayıt {remaining} gün daha saklanabilir.",
    )
