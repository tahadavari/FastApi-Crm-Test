"""SQLAlchemy-backed Unit of Work."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from domain.unit_of_work import UnitOfWork
from infrastructure.repositories.activity_sqlalchemy import SQLAlchemyActivityRepository
from infrastructure.repositories.customer_sqlalchemy import SQLAlchemyCustomerRepository
from infrastructure.repositories.deal_sqlalchemy import SQLAlchemyDealRepository
from infrastructure.repositories.task_sqlalchemy import SQLAlchemyTaskRepository


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.customers = SQLAlchemyCustomerRepository(session)
        self.activities = SQLAlchemyActivityRepository(session)
        self.deals = SQLAlchemyDealRepository(session)
        self.tasks = SQLAlchemyTaskRepository(session)

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
