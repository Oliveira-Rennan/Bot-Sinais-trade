from collections.abc import Sequence
from datetime import UTC, datetime
from decimal import Decimal

from app.domain.enums import MarketType, MethodStatus, PeriodType
from app.models.method import Method
from app.repositories.method_repository import MethodRepository
from app.schemas.method import MethodCreate, MethodUpdate


class MethodNotFoundError(Exception):
    pass


class MethodValidationError(Exception):
    pass


class MethodService:
    def __init__(self, repository: MethodRepository) -> None:
        self.repository = repository

    def create(self, payload: MethodCreate) -> Method:
        method = Method(**payload.model_dump())
        return self.repository.create(method)

    def list(
        self,
        *,
        status: MethodStatus | None = None,
        market: MarketType | None = None,
        period: PeriodType | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Method]:
        return self.repository.list(
            status=status,
            market=market,
            period=period,
            limit=limit,
            offset=offset,
        )

    def get(self, method_id: int) -> Method:
        method = self.repository.get(method_id)
        if method is None:
            raise MethodNotFoundError
        return method

    def update(self, method_id: int, payload: MethodUpdate) -> Method:
        method = self.get(method_id)
        update_data = payload.model_dump(exclude_unset=True)

        if not update_data:
            return method

        merged_data = self._merged_data(method, update_data)
        self._validate_merged_data(merged_data)

        if "historical_hit_rate" in update_data and "fair_odd" not in update_data:
            update_data["fair_odd"] = Decimal("1") / update_data["historical_hit_rate"]

        for field, value in update_data.items():
            setattr(method, field, value)

        method.updated_at = datetime.now(UTC)
        return self.repository.save(method)

    def archive(self, method_id: int) -> Method:
        method = self.get(method_id)
        method.status = MethodStatus.ARCHIVED
        method.updated_at = datetime.now(UTC)
        return self.repository.save(method)

    @staticmethod
    def _merged_data(method: Method, update_data: dict) -> dict:
        fields = [
            "minute_start",
            "minute_end",
            "min_odd",
            "max_odd",
            "name",
        ]
        merged = {field: getattr(method, field) for field in fields}
        merged.update(update_data)
        return merged

    @staticmethod
    def _validate_merged_data(data: dict) -> None:
        if data["name"] is not None and not str(data["name"]).strip():
            raise MethodValidationError("name must not be empty")

        if data["minute_end"] <= data["minute_start"]:
            raise MethodValidationError("minute_end must be greater than minute_start")

        min_odd = data.get("min_odd")
        max_odd = data.get("max_odd")
        if min_odd is not None and max_odd is not None and max_odd <= min_odd:
            raise MethodValidationError("max_odd must be greater than min_odd")
