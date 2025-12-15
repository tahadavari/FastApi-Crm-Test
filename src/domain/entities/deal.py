"""Deal entity with pipeline stage enforcement."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from domain.errors import InvalidStageTransition, ValidationError


class DealStage:
    """Supported deal pipeline stages."""

    NEW = "NEW"
    CONTACTED = "CONTACTED"
    PROPOSAL = "PROPOSAL"
    WON = "WON"
    LOST = "LOST"

    ALL = {NEW, CONTACTED, PROPOSAL, WON, LOST}


@dataclass
class Deal:
    """Sales opportunity tied to a customer."""

    customer_id: UUID
    title: str
    amount: float
    stage: str = DealStage.NEW
    expected_close_date: Optional[date] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        self._validate_stage(self.stage)

    @staticmethod
    def _validate_stage(stage: str) -> None:
        if stage not in DealStage.ALL:
            raise ValidationError("Invalid deal stage")

    def move_to_stage(self, new_stage: str) -> None:
        """Move to a new stage enforcing terminal restrictions."""

        self._validate_stage(new_stage)
        if self.stage in {DealStage.WON, DealStage.LOST}:
            raise InvalidStageTransition("Cannot move a closed deal to another stage")
        self.stage = new_stage

    def mark_as_won(self) -> None:
        self.stage = DealStage.WON

    def mark_as_lost(self) -> None:
        self.stage = DealStage.LOST

    def update_details(
        self, *, title: Optional[str] = None, amount: Optional[float] = None, expected_close_date: Optional[date] = None
    ) -> None:
        if title is not None:
            self.title = title
        if amount is not None:
            self.amount = amount
        if expected_close_date is not None:
            self.expected_close_date = expected_close_date
