"""Task entity encapsulating reminders and completion rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from domain.errors import TaskAlreadyCompleted, ValidationError


class TaskStatus:
    """Possible task statuses."""

    PENDING = "PENDING"
    DONE = "DONE"
    CANCELED = "CANCELED"

    ALL = {PENDING, DONE, CANCELED}


@dataclass
class Task:
    """Reminder or todo item linked to a customer or deal."""

    title: str
    due_date: datetime
    customer_id: Optional[UUID] = None
    deal_id: Optional[UUID] = None
    status: str = TaskStatus.PENDING
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        self._validate_status(self.status)
        self._validate_due_date(self.due_date)

    @staticmethod
    def _validate_status(status: str) -> None:
        if status not in TaskStatus.ALL:
            raise ValidationError("Invalid task status")

    @staticmethod
    def _validate_due_date(due_date: datetime) -> None:
        now = datetime.now(timezone.utc)
        if due_date < now.replace(tzinfo=timezone.utc) and (now - due_date).days > 7:
            raise ValidationError("Due date is too far in the past")

    def complete(self) -> None:
        if self.status != TaskStatus.PENDING:
            raise TaskAlreadyCompleted("Task cannot be completed from its current status")
        self.status = TaskStatus.DONE

    def cancel(self) -> None:
        self.status = TaskStatus.CANCELED
