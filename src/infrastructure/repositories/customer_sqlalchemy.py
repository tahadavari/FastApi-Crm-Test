"""SQLAlchemy implementation of customer repository."""

from __future__ import annotations

from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.customer import Customer
from domain.repositories.customer import CustomerRepository
from infrastructure.db.models.customer import CustomerModel
from infrastructure.db.models.deal import DealModel


class SQLAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, customer: Customer) -> None:
        model = CustomerModel(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            company_name=customer.company_name,
            status=customer.status,
            created_at=customer.created_at,
            updated_at=customer.updated_at,
        )
        self.session.add(model)

    async def get(self, customer_id: UUID) -> Customer | None:
        result = await self.session.execute(select(CustomerModel).where(CustomerModel.id == customer_id))
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            phone=model.phone,
            company_name=model.company_name,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    async def list(self, *, status: str | None = None) -> Iterable[Customer]:
        query = select(CustomerModel)
        if status:
            query = query.where(CustomerModel.status == status)
        result = await self.session.execute(query.order_by(CustomerModel.created_at.desc()))
        models = result.scalars().all()
        return [
            Customer(
                id=m.id,
                name=m.name,
                email=m.email,
                phone=m.phone,
                company_name=m.company_name,
                status=m.status,
                created_at=m.created_at,
                updated_at=m.updated_at,
            )
            for m in models
        ]

    async def count_active_deals(self, customer_id: UUID) -> int:
        result = await self.session.execute(
            select(DealModel).where(DealModel.customer_id == customer_id, DealModel.stage.notin_(["WON", "LOST"]))
        )
        return len(result.scalars().all())

    async def update(self, customer: Customer) -> None:
        await self.session.merge(
            CustomerModel(
                id=customer.id,
                name=customer.name,
                email=customer.email,
                phone=customer.phone,
                company_name=customer.company_name,
                status=customer.status,
                created_at=customer.created_at,
                updated_at=customer.updated_at,
            )
        )
