"""Deal repository abstraction."""

from __future__ import annotations

from typing import Iterable, Protocol
from uuid import UUID

from domain.entities.deal import Deal


class DealRepository(Protocol):
    async def add(self, deal: Deal) -> None:
        ...

    async def get(self, deal_id: UUID) -> Deal | None:
        ...

    async def list(self, *, stage: str | None = None) -> Iterable[Deal]:
        ...

    async def update(self, deal: Deal) -> None:
        ...
