"""Service for creating and listing activities."""

from __future__ import annotations

from typing import Iterable
from uuid import UUID

from domain.entities.activity import Activity
from domain.errors import CustomerNotFound
from domain.unit_of_work import UnitOfWork


class ActivityService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def add_activity(
        self, *, customer_id: UUID, type: str, subject: str, description: str | None, created_by_user_id: UUID | None
    ) -> Activity:
        async with self.uow:
            customer = await self.uow.customers.get(customer_id)
            if not customer:
                raise CustomerNotFound("Customer not found")
            activity = Activity(
                customer_id=customer_id,
                type=type,
                subject=subject,
                description=description,
                created_by_user_id=created_by_user_id,
            )
            await self.uow.activities.add(activity)
            await self.uow.commit()
            return activity

    async def list_activities(self, customer_id: UUID) -> Iterable[Activity]:
        async with self.uow:
            customer = await self.uow.customers.get(customer_id)
            if not customer:
                raise CustomerNotFound("Customer not found")
            return await self.uow.activities.list_for_customer(customer_id)
