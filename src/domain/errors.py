"""Domain-specific exception classes for business rules and validations."""

from __future__ import annotations


class DomainError(Exception):
    """Base class for domain-level errors."""


class CustomerNotFound(DomainError):
    """Raised when a customer cannot be located."""


class DealNotFound(DomainError):
    """Raised when a deal cannot be located."""


class ActivityNotFound(DomainError):
    """Raised when an activity cannot be located."""


class TaskNotFound(DomainError):
    """Raised when a task cannot be located."""


class InvalidStageTransition(DomainError):
    """Raised when a deal tries to move to an invalid stage."""


class TaskAlreadyCompleted(DomainError):
    """Raised when attempting to complete an already finished task."""


class CustomerHasActiveDeals(DomainError):
    """Raised when business rules prevent deleting/archiving a customer with active deals."""


class ValidationError(DomainError):
    """Raised when entity-level validation fails."""
