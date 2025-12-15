"""SQLAlchemy task repository."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.task import Task
from domain.repositories.task import TaskRepository
from infrastructure.db.models.task import TaskModel


class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, task: Task) -> None:
        model = TaskModel(
            id=task.id,
            customer_id=task.customer_id,
            deal_id=task.deal_id,
            title=task.title,
            due_date=task.due_date,
            status=task.status,
            created_at=task.created_at,
        )
        self.session.add(model)

    async def get(self, task_id: UUID) -> Task | None:
        result = await self.session.execute(select(TaskModel).where(TaskModel.id == task_id))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Task(
            id=model.id,
            customer_id=model.customer_id,
            deal_id=model.deal_id,
            title=model.title,
            due_date=model.due_date,
            status=model.status,
            created_at=model.created_at,
        )

    async def list(self, *, status: str | None = None, due_before: datetime | None = None) -> Iterable[Task]:
        query = select(TaskModel)
        if status:
            query = query.where(TaskModel.status == status)
        if due_before:
            query = query.where(TaskModel.due_date <= due_before)
        result = await self.session.execute(query.order_by(TaskModel.due_date))
        models = result.scalars().all()
        return [
            Task(
                id=m.id,
                customer_id=m.customer_id,
                deal_id=m.deal_id,
                title=m.title,
                due_date=m.due_date,
                status=m.status,
                created_at=m.created_at,
            )
            for m in models
        ]

    async def update(self, task: Task) -> None:
        await self.session.merge(
            TaskModel(
                id=task.id,
                customer_id=task.customer_id,
                deal_id=task.deal_id,
                title=task.title,
                due_date=task.due_date,
                status=task.status,
                created_at=task.created_at,
            )
        )
