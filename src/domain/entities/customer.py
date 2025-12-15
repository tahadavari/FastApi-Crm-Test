"""Customer entity containing business rules and state transitions."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from domain.errors import CustomerHasActiveDeals, ValidationError


VALID_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class CustomerStatus:
    """Supported customer lifecycle statuses."""

    NEW = "NEW"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

    ALL = {NEW, ACTIVE, INACTIVE}


@dataclass
class Customer:
    """Represents a CRM customer with validation and lifecycle helpers."""

    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company_name: Optional[str] = None
    status: str = CustomerStatus.NEW
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        self._validate_status(self.status)
        if self.email:
            self._validate_email(self.email)

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)

    @staticmethod
    def _validate_email(email: str) -> None:
        if not VALID_EMAIL_REGEX.match(email):
            raise ValidationError("Invalid email format")

    @staticmethod
    def _validate_status(status: str) -> None:
        if status not in CustomerStatus.ALL:
            raise ValidationError("Invalid customer status")

    def update_details(
        self,
        *,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company_name: Optional[str] = None,
        status: Optional[str] = None,
    ) -> None:
        """Update mutable fields with validation."""

        if name is not None:
            self.name = name
        if email is not None:
            self._validate_email(email)
            self.email = email
        if phone is not None:
            self.phone = phone
        if company_name is not None:
            self.company_name = company_name
        if status is not None:
            self._validate_status(status)
            self.status = status
        self._touch()

    def activate(self) -> None:
        self.status = CustomerStatus.ACTIVE
        self._touch()

    def deactivate(self) -> None:
        self.status = CustomerStatus.INACTIVE
        self._touch()

    def ensure_can_be_archived(self, active_deals: int) -> None:
        """Raise if archiving is forbidden due to active deals."""

        if active_deals > 0:
            raise CustomerHasActiveDeals(
                "Customer has active deals and cannot be archived until they are closed."
            )
        self.deactivate()
