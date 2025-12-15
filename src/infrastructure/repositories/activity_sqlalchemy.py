"""SQLAlchemy activity repository."""

from __future__ import annotations

from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.activity import Activity
from domain.repositories.activity import ActivityRepository
from infrastructure.db.models.activity import ActivityModel


class SQLAlchemyActivityRepository(ActivityRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, activity: Activity) -> None:
        model = ActivityModel(
            id=activity.id,
            customer_id=activity.customer_id,
            type=activity.type,
            subject=activity.subject,
            description=activity.description,
            created_by_user_id=activity.created_by_user_id,
            created_at=activity.created_at,
        )
        self.session.add(model)

    async def list_for_customer(self, customer_id: UUID) -> Iterable[Activity]:
        result = await self.session.execute(
            select(ActivityModel)
            .where(ActivityModel.customer_id == customer_id)
            .order_by(ActivityModel.created_at.desc())
        )
        models = result.scalars().all()
        return [
            Activity(
                id=m.id,
                customer_id=m.customer_id,
                type=m.type,
                subject=m.subject,
                description=m.description,
                created_by_user_id=m.created_by_user_id,
                created_at=m.created_at,
            )
            for m in models
        ]
