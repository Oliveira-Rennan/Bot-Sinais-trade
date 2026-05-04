from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.enums import MarketType, MethodStatus, PeriodType
from app.models.method import Method


class MethodRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, method: Method) -> Method:
        self.db.add(method)
        self.db.commit()
        self.db.refresh(method)
        return method

    def get(self, method_id: int) -> Method | None:
        return self.db.get(Method, method_id)

    def list(
        self,
        *,
        status: MethodStatus | None = None,
        market: MarketType | None = None,
        period: PeriodType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Method]:
        statement = select(Method).order_by(Method.id).limit(limit).offset(offset)

        if status is None:
            statement = statement.where(Method.status != MethodStatus.ARCHIVED.value)
        else:
            statement = statement.where(Method.status == status.value)

        if market is not None:
            statement = statement.where(Method.market == market.value)

        if period is not None:
            statement = statement.where(Method.period == period.value)

        return self.db.scalars(statement).all()

    def save(self, method: Method) -> Method:
        self.db.add(method)
        self.db.commit()
        self.db.refresh(method)
        return method
