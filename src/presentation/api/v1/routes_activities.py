"""Activity endpoints."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.services.activity_service import ActivityService
from domain.errors import CustomerNotFound, ValidationError
from presentation.api.schemas.activities import ActivityCreate, ActivityResponse
from presentation.dependencies import get_uow


router = APIRouter(prefix="/v1/customers/{customer_id}/activities", tags=["activities"])


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def add_activity(customer_id: UUID, payload: ActivityCreate, uow=Depends(get_uow)) -> ActivityResponse:
    service = ActivityService(uow)
    try:
        activity = await service.add_activity(
            customer_id=customer_id,
            type=payload.type,
            subject=payload.subject,
            description=payload.description,
            created_by_user_id=payload.created_by_user_id,
        )
    except CustomerNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    return ActivityResponse(**activity.__dict__)


@router.get("", response_model=List[ActivityResponse])
async def list_activities(customer_id: UUID, uow=Depends(get_uow)) -> List[ActivityResponse]:
    service = ActivityService(uow)
    try:
        activities = await service.list_activities(customer_id)
    except CustomerNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return [ActivityResponse(**a.__dict__) for a in activities]
