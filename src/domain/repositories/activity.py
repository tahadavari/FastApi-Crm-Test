"""Activity repository abstraction."""

from __future__ import annotations

from typing import Iterable, Protocol
from uuid import UUID

from domain.entities.activity import Activity


class ActivityRepository(Protocol):
    async def add(self, activity: Activity) -> None:
        ...

    async def list_for_customer(self, customer_id: UUID) -> Iterable[Activity]:
        ...
