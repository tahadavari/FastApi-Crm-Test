"""Customer endpoints."""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from application.services.customer_service import CustomerService
from domain.errors import CustomerHasActiveDeals, CustomerNotFound, ValidationError
from presentation.api.schemas.customers import CustomerCreate, CustomerResponse, CustomerUpdate
from presentation.dependencies import get_uow


router = APIRouter(prefix="/v1/customers", tags=["customers"])


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(payload: CustomerCreate, uow=Depends(get_uow)) -> CustomerResponse:
    service = CustomerService(uow)
    try:
        customer = await service.create_customer(
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            company_name=payload.company_name,
            status=payload.status,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    return CustomerResponse(**customer.__dict__)


@router.get("", response_model=List[CustomerResponse])
async def list_customers(status_filter: str | None = None, uow=Depends(get_uow)) -> List[CustomerResponse]:
    service = CustomerService(uow)
    customers = await service.list_customers(status=status_filter)
    return [CustomerResponse(**c.__dict__) for c in customers]


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: UUID, uow=Depends(get_uow)) -> CustomerResponse:
    service = CustomerService(uow)
    try:
        customer = await service.get_customer(customer_id)
    except CustomerNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return CustomerResponse(**customer.__dict__)


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(customer_id: UUID, payload: CustomerUpdate, uow=Depends(get_uow)) -> CustomerResponse:
    service = CustomerService(uow)
    try:
        customer = await service.update_customer(
            customer_id,
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            company_name=payload.company_name,
            status=payload.status,
        )
    except CustomerNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    return CustomerResponse(**customer.__dict__)


@router.post("/{customer_id}/archive", response_model=CustomerResponse)
async def archive_customer(customer_id: UUID, uow=Depends(get_uow)) -> CustomerResponse:
    service = CustomerService(uow)
    try:
        customer = await service.archive_customer(customer_id)
    except CustomerNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except CustomerHasActiveDeals as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return CustomerResponse(**customer.__dict__)
