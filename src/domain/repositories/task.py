"""Task repository abstraction."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Protocol
from uuid import UUID

from domain.entities.task import Task


class TaskRepository(Protocol):
    async def add(self, task: Task) -> None:
        ...

    async def get(self, task_id: UUID) -> Task | None:
        ...

    async def list(self, *, status: str | None = None, due_before: datetime | None = None) -> Iterable[Task]:
        ...

    async def update(self, task: Task) -> None:
        ...
