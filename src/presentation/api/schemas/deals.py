"""Pydantic schemas for deals."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DealCreate(BaseModel):
    customer_id: UUID
    title: str
    amount: float
    stage: str = Field("NEW")
    expected_close_date: Optional[date] = None


class DealUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    expected_close_date: Optional[date] = None


class MoveStage(BaseModel):
    new_stage: str


class DealResponse(BaseModel):
    id: UUID
    customer_id: UUID
    title: str
    amount: float
    stage: str
    expected_close_date: Optional[date]
    created_at: datetime

    class Config:
        orm_mode = True
