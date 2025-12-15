"""SQLAlchemy deal repository."""

from __future__ import annotations

from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.deal import Deal
from domain.repositories.deal import DealRepository
from infrastructure.db.models.deal import DealModel


class SQLAlchemyDealRepository(DealRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, deal: Deal) -> None:
        model = DealModel(
            id=deal.id,
            customer_id=deal.customer_id,
            title=deal.title,
            amount=deal.amount,
            stage=deal.stage,
            expected_close_date=deal.expected_close_date,
            created_at=deal.created_at,
        )
        self.session.add(model)

    async def get(self, deal_id: UUID) -> Deal | None:
        result = await self.session.execute(select(DealModel).where(DealModel.id == deal_id))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Deal(
            id=model.id,
            customer_id=model.customer_id,
            title=model.title,
            amount=float(model.amount),
            stage=model.stage,
            expected_close_date=model.expected_close_date,
            created_at=model.created_at,
        )

    async def list(self, *, stage: str | None = None) -> Iterable[Deal]:
        query = select(DealModel)
        if stage:
            query = query.where(DealModel.stage == stage)
        result = await self.session.execute(query.order_by(DealModel.created_at.desc()))
        models = result.scalars().all()
        return [
            Deal(
                id=m.id,
                customer_id=m.customer_id,
                title=m.title,
                amount=float(m.amount),
                stage=m.stage,
                expected_close_date=m.expected_close_date,
                created_at=m.created_at,
            )
            for m in models
        ]

    async def update(self, deal: Deal) -> None:
        await self.session.merge(
            DealModel(
                id=deal.id,
                customer_id=deal.customer_id,
                title=deal.title,
                amount=deal.amount,
                stage=deal.stage,
                expected_close_date=deal.expected_close_date,
                created_at=deal.created_at,
            )
        )
