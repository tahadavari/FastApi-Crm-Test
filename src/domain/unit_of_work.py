"""Unit of Work abstraction for coordinating repositories and transactions."""

from __future__ import annotations

from typing import Protocol

from domain.repositories.activity import ActivityRepository
from domain.repositories.customer import CustomerRepository
from domain.repositories.deal import DealRepository
from domain.repositories.task import TaskRepository


class UnitOfWork(Protocol):
    customers: CustomerRepository
    activities: ActivityRepository
    deals: DealRepository
    tasks: TaskRepository

    async def __aenter__(self) -> "UnitOfWork":
        ...

    async def __aexit__(self, exc_type, exc, tb) -> None:
        ...

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...
