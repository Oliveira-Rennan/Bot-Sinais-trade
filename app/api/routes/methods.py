from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.enums import MarketType, MethodStatus, PeriodType
from app.repositories.method_repository import MethodRepository
from app.schemas.method import MethodCreate, MethodRead, MethodUpdate
from app.services.method_service import (
    MethodNotFoundError,
    MethodService,
    MethodValidationError,
)

router = APIRouter(prefix="/methods", tags=["methods"])


def get_method_service(db: Session = Depends(get_db)) -> MethodService:
    return MethodService(MethodRepository(db))


@router.post("", response_model=MethodRead, status_code=status.HTTP_201_CREATED)
def create_method(
    payload: MethodCreate,
    service: Annotated[MethodService, Depends(get_method_service)],
):
    return service.create(payload)


@router.get("", response_model=list[MethodRead])
def list_methods(
    service: Annotated[MethodService, Depends(get_method_service)],
    status: MethodStatus | None = None,
    market: MarketType | None = None,
    period: PeriodType | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return service.list(
        status=status,
        market=market,
        period=period,
        limit=limit,
        offset=offset,
    )


@router.get("/{method_id}", response_model=MethodRead)
def get_method(
    method_id: int,
    service: Annotated[MethodService, Depends(get_method_service)],
):
    try:
        return service.get(method_id)
    except MethodNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Method not found") from exc


@router.patch("/{method_id}", response_model=MethodRead)
def update_method(
    method_id: int,
    payload: MethodUpdate,
    service: Annotated[MethodService, Depends(get_method_service)],
):
    try:
        return service.update(method_id, payload)
    except MethodNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Method not found") from exc
    except MethodValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


@router.delete("/{method_id}", response_model=MethodRead)
def archive_method(
    method_id: int,
    service: Annotated[MethodService, Depends(get_method_service)],
):
    try:
        return service.archive(method_id)
    except MethodNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Method not found") from exc
