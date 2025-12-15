"""Deal endpoints."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.services.deal_service import DealService
from domain.errors import CustomerNotFound, DealNotFound, InvalidStageTransition, ValidationError
from presentation.api.schemas.deals import DealCreate, DealResponse, DealUpdate, MoveStage
from presentation.dependencies import get_uow


router = APIRouter(prefix="/v1/deals", tags=["deals"])


@router.post("", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(payload: DealCreate, uow=Depends(get_uow)) -> DealResponse:
    service = DealService(uow)
    try:
        deal = await service.create_deal(
            customer_id=payload.customer_id,
            title=payload.title,
            amount=payload.amount,
            stage=payload.stage,
            expected_close_date=payload.expected_close_date,
        )
    except (CustomerNotFound, ValidationError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    return DealResponse(**deal.__dict__)


@router.get("", response_model=List[DealResponse])
async def list_deals(stage: str | None = None, uow=Depends(get_uow)) -> List[DealResponse]:
    service = DealService(uow)
    deals = await service.list_deals(stage=stage)
    return [DealResponse(**d.__dict__) for d in deals]


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(deal_id: UUID, uow=Depends(get_uow)) -> DealResponse:
    service = DealService(uow)
    try:
        deal = await service.get_deal(deal_id)
    except DealNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return DealResponse(**deal.__dict__)


@router.patch("/{deal_id}", response_model=DealResponse)
async def update_deal(deal_id: UUID, payload: DealUpdate, uow=Depends(get_uow)) -> DealResponse:
    service = DealService(uow)
    try:
        deal = await service.update_deal(
            deal_id,
            title=payload.title,
            amount=payload.amount,
            expected_close_date=payload.expected_close_date,
        )
    except DealNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return DealResponse(**deal.__dict__)


@router.post("/{deal_id}/move-stage", response_model=DealResponse)
async def move_stage(deal_id: UUID, payload: MoveStage, uow=Depends(get_uow)) -> DealResponse:
    service = DealService(uow)
    try:
        deal = await service.move_stage(deal_id, payload.new_stage)
    except DealNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except (InvalidStageTransition, ValidationError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return DealResponse(**deal.__dict__)
