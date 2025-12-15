"""Task service for reminders lifecycle."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable
from uuid import UUID

from domain.entities.task import Task
from domain.errors import TaskNotFound
from domain.unit_of_work import UnitOfWork


class TaskService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_task(
        self,
        *,
        title: str,
        due_date: datetime,
        customer_id: UUID | None,
        deal_id: UUID | None,
    ) -> Task:
        task = Task(title=title, due_date=due_date, customer_id=customer_id, deal_id=deal_id)
        async with self.uow:
            await self.uow.tasks.add(task)
            await self.uow.commit()
            return task

    async def list_tasks(self, *, status: str | None = None, due_before: datetime | None = None) -> Iterable[Task]:
        async with self.uow:
            return await self.uow.tasks.list(status=status, due_before=due_before)

    async def complete_task(self, task_id: UUID) -> Task:
        async with self.uow:
            task = await self.uow.tasks.get(task_id)
            if not task:
                raise TaskNotFound("Task not found")
            task.complete()
            await self.uow.tasks.update(task)
            await self.uow.commit()
            return task
