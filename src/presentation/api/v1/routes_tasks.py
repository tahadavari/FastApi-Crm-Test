"""Task endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.services.task_service import TaskService
from domain.errors import TaskAlreadyCompleted, TaskNotFound, ValidationError
from presentation.api.schemas.tasks import TaskCreate, TaskResponse
from presentation.dependencies import get_uow


router = APIRouter(prefix="/v1/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, uow=Depends(get_uow)) -> TaskResponse:
    service = TaskService(uow)
    try:
        task = await service.create_task(
            title=payload.title,
            due_date=payload.due_date,
            customer_id=payload.customer_id,
            deal_id=payload.deal_id,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    return TaskResponse(**task.__dict__)


@router.get("", response_model=List[TaskResponse])
async def list_tasks(status_filter: str | None = None, due_before: str | None = None, uow=Depends(get_uow)) -> List[TaskResponse]:
    service = TaskService(uow)
    parsed_due = None
    if due_before:
        try:
            parsed_due = datetime.fromisoformat(due_before)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    tasks = await service.list_tasks(status=status_filter, due_before=parsed_due)
    return [TaskResponse(**t.__dict__) for t in tasks]


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: UUID, uow=Depends(get_uow)) -> TaskResponse:
    service = TaskService(uow)
    try:
        task = await service.complete_task(task_id)
    except TaskNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except TaskAlreadyCompleted as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return TaskResponse(**task.__dict__)
