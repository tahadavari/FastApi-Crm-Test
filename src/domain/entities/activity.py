"""Activity entity describing customer interactions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from domain.errors import ValidationError


class ActivityType:
    """Supported activity types."""

    CALL = "CALL"
    EMAIL = "EMAIL"
    MEETING = "MEETING"
    NOTE = "NOTE"

    ALL = {CALL, EMAIL, MEETING, NOTE}


@dataclass
class Activity:
    """Represents a recorded interaction with a customer."""

    customer_id: UUID
    type: str
    subject: str
    description: Optional[str] = None
    created_by_user_id: Optional[UUID] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if self.type not in ActivityType.ALL:
            raise ValidationError("Invalid activity type")
