"""Customer repository abstraction."""

from __future__ import annotations

from typing import Iterable, Protocol
from uuid import UUID

from domain.entities.customer import Customer


class CustomerRepository(Protocol):
    """Persistence port for customers."""

    async def add(self, customer: Customer) -> None:
        ...

    async def get(self, customer_id: UUID) -> Customer | None:
        ...

    async def list(self, *, status: str | None = None) -> Iterable[Customer]:
        ...

    async def count_active_deals(self, customer_id: UUID) -> int:
        ...

    async def update(self, customer: Customer) -> None:
        ...
