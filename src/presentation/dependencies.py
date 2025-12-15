"""Dependency providers for FastAPI routes."""

from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.session import get_session
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


async def get_uow(session: AsyncSession = Depends(get_session)) -> SQLAlchemyUnitOfWork:
    """Provide a Unit of Work bound to the request-scoped session."""

    return SQLAlchemyUnitOfWork(session)
