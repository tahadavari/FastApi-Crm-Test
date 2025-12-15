"""Pydantic schemas for customer endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = None
    company_name: Optional[str] = None
    status: str = Field("NEW")


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    status: Optional[str] = None


class CustomerResponse(BaseModel):
    id: UUID
    name: str
    email: Optional[str]
    phone: Optional[str]
    company_name: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
