from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from domain.entities.task import Task, TaskStatus
from domain.errors import TaskAlreadyCompleted, ValidationError


def test_complete_task_transitions_from_pending():
    due = datetime.now(timezone.utc) + timedelta(days=1)
    task = Task(title="Call", due_date=due)
    task.complete()
    assert task.status == TaskStatus.DONE


def test_complete_task_from_non_pending_fails():
    due = datetime.now(timezone.utc) + timedelta(days=1)
    task = Task(title="Call", due_date=due, status=TaskStatus.DONE)
    with pytest.raises(TaskAlreadyCompleted):
        task.complete()


def test_due_date_far_past_rejected():
    past_due = datetime.now(timezone.utc) - timedelta(days=10)
    with pytest.raises(ValidationError):
        Task(title="Old", due_date=past_due)
