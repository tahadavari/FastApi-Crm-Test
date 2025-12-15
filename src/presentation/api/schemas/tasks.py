"""Pydantic schemas for tasks."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    due_date: datetime
    customer_id: Optional[UUID] = None
    deal_id: Optional[UUID] = None


class TaskResponse(BaseModel):
    id: UUID
    customer_id: Optional[UUID]
    deal_id: Optional[UUID]
    title: str
    due_date: datetime
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
