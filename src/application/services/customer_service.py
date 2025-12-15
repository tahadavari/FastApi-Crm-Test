"""Customer service orchestrating UoW operations and domain rules."""

from __future__ import annotations

from typing import Iterable
from uuid import UUID

from domain.entities.customer import Customer
from domain.errors import CustomerNotFound
from domain.unit_of_work import UnitOfWork


class CustomerService:
    """Use cases for managing customers."""

    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def create_customer(
        self, *, name: str, email: str | None, phone: str | None, company_name: str | None, status: str
    ) -> Customer:
        new_customer = Customer(name=name, email=email, phone=phone, company_name=company_name, status=status)
        async with self.uow:
            await self.uow.customers.add(new_customer)
            await self.uow.commit()
        return new_customer

    async def list_customers(self, *, status: str | None = None) -> Iterable[Customer]:
        async with self.uow:
            customers = await self.uow.customers.list(status=status)
        return customers

    async def get_customer(self, customer_id: UUID) -> Customer:
        async with self.uow:
            customer = await self.uow.customers.get(customer_id)
        if not customer:
            raise CustomerNotFound("Customer not found")
        return customer

    async def update_customer(
        self,
        customer_id: UUID,
        *,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        company_name: str | None = None,
        status: str | None = None,
    ) -> Customer:
        async with self.uow:
            customer = await self.uow.customers.get(customer_id)
            if not customer:
                raise CustomerNotFound("Customer not found")
            customer.update_details(
                name=name, email=email, phone=phone, company_name=company_name, status=status
            )
            await self.uow.customers.update(customer)
            await self.uow.commit()
            return customer

    async def archive_customer(self, customer_id: UUID) -> Customer:
        async with self.uow:
            customer = await self.uow.customers.get(customer_id)
            if not customer:
                raise CustomerNotFound("Customer not found")
            active_deals = await self.uow.customers.count_active_deals(customer_id)
            customer.ensure_can_be_archived(active_deals)
            await self.uow.customers.update(customer)
            await self.uow.commit()
            return customer
