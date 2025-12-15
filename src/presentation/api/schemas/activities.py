"""Pydantic schemas for activities."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ActivityCreate(BaseModel):
    type: str
    subject: str
    description: Optional[str] = None
    created_by_user_id: Optional[UUID] = None


class ActivityResponse(BaseModel):
    id: UUID
    customer_id: UUID
    type: str
    subject: str
    description: Optional[str]
    created_by_user_id: Optional[UUID]
    created_at: datetime

    class Config:
        orm_mode = True
