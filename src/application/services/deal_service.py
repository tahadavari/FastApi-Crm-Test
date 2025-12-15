"""Deal service implementing creation and stage transitions."""

from __future__ import annotations

from typing import Iterable
from uuid import UUID

from domain.entities.activity import Activity, ActivityType
from domain.entities.deal import Deal
from domain.errors import CustomerNotFound, DealNotFound
from domain.unit_of_work import UnitOfWork


class DealService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_deal(
        self,
        *,
        customer_id: UUID,
        title: str,
        amount: float,
        stage: str,
        expected_close_date,
    ) -> Deal:
        async with self.uow:
            customer = await self.uow.customers.get(customer_id)
            if not customer:
                raise CustomerNotFound("Customer not found")
            deal = Deal(
                customer_id=customer_id,
                title=title,
                amount=amount,
                stage=stage,
                expected_close_date=expected_close_date,
            )
            await self.uow.deals.add(deal)
            await self.uow.commit()
            return deal

    async def list_deals(self, *, stage: str | None = None) -> Iterable[Deal]:
        async with self.uow:
            return await self.uow.deals.list(stage=stage)

    async def get_deal(self, deal_id: UUID) -> Deal:
        async with self.uow:
            deal = await self.uow.deals.get(deal_id)
        if not deal:
            raise DealNotFound("Deal not found")
        return deal

    async def update_deal(
        self,
        deal_id: UUID,
        *,
        title: str | None = None,
        amount: float | None = None,
        expected_close_date=None,
    ) -> Deal:
        async with self.uow:
            deal = await self.uow.deals.get(deal_id)
            if not deal:
                raise DealNotFound("Deal not found")
            deal.update_details(title=title, amount=amount, expected_close_date=expected_close_date)
            await self.uow.deals.update(deal)
            await self.uow.commit()
            return deal

    async def move_stage(self, deal_id: UUID, new_stage: str) -> Deal:
        async with self.uow:
            deal = await self.uow.deals.get(deal_id)
            if not deal:
                raise DealNotFound("Deal not found")
            previous_stage = deal.stage
            deal.move_to_stage(new_stage)
            await self.uow.deals.update(deal)
            if new_stage in {"WON", "LOST"}:
                note = Activity(
                    customer_id=deal.customer_id,
                    type=ActivityType.NOTE,
                    subject=f"Deal {new_stage.lower()}",
                    description=f"Deal moved from {previous_stage} to {new_stage}",
                )
                await self.uow.activities.add(note)
            await self.uow.commit()
            return deal
