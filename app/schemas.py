from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AssetCreate(BaseModel):
    record_name: str = Field(min_length=3, max_length=100)
    data_category: str = Field(min_length=2, max_length=80)
    purpose: str = Field(min_length=3, max_length=240)
    legal_basis: str = Field(min_length=3, max_length=160)
    storage_location: str = Field(min_length=2, max_length=160)
    owner_role: str = Field(min_length=2, max_length=80)
    subject_reference: str = Field(min_length=2, max_length=80)
    retention_days: int = Field(gt=0, le=3650)
    collected_on: date

    @field_validator(
        "record_name",
        "data_category",
        "purpose",
        "legal_basis",
        "storage_location",
        "owner_role",
        "subject_reference",
    )
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class RetentionDecision(BaseModel):
    action: Literal["keep", "anonymize", "delete"]
    actor: str = Field(min_length=2, max_length=80)
    reason: str = Field(min_length=8, max_length=500)


class AssetView(BaseModel):
    id: str
    record_name: str
    data_category: str
    purpose: str
    legal_basis: str
    storage_location: str
    owner_role: str
    subject_reference: str
    retention_days: int
    collected_on: str
    expires_on: str
    status: str
    created_at: str
