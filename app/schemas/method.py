from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.domain.enums import MarketType, MethodStatus, PeriodType


class MethodBase(BaseModel):
    name: str
    description: str | None = None
    market: MarketType
    period: PeriodType
    status: MethodStatus = MethodStatus.ACTIVE
    minute_start: int = Field(ge=0)
    minute_end: int
    score_filter: str | None = None
    min_dangerous_attacks: int | None = None
    min_total_shots: int | None = None
    min_shots_on_target: int | None = None
    min_corners: int | None = None
    max_red_cards: int = Field(default=0, ge=0)
    min_odd: Decimal | None = Field(default=None, gt=Decimal("1"))
    max_odd: Decimal | None = Field(default=None, gt=Decimal("1"))
    historical_hit_rate: Decimal = Field(gt=Decimal("0"), le=Decimal("1"))
    sample_size: int = Field(gt=0)
    fair_odd: Decimal | None = None
    min_edge: Decimal = Field(default=Decimal("0.08"), ge=Decimal("0"))
    stake_units: Decimal = Field(default=Decimal("0.5"), gt=Decimal("0"))
    source: str = "zeus"
    zeus_query: str | None = None
    scanner_condition: str | None = None
    entry_rule: str | None = None
    validation_notes: str | None = None
    notes: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name must not be empty")
        return value

    @model_validator(mode="after")
    def validate_method_ranges(self) -> "MethodBase":
        if self.minute_end <= self.minute_start:
            raise ValueError("minute_end must be greater than minute_start")

        if self.min_odd is not None and self.max_odd is not None:
            if self.max_odd <= self.min_odd:
                raise ValueError("max_odd must be greater than min_odd")

        return self


class MethodCreate(MethodBase):
    @model_validator(mode="after")
    def calculate_fair_odd(self) -> "MethodCreate":
        if self.fair_odd is None:
            self.fair_odd = Decimal("1") / self.historical_hit_rate

        return self


class MethodUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    market: MarketType | None = None
    period: PeriodType | None = None
    status: MethodStatus | None = None
    minute_start: int | None = Field(default=None, ge=0)
    minute_end: int | None = None
    score_filter: str | None = None
    min_dangerous_attacks: int | None = None
    min_total_shots: int | None = None
    min_shots_on_target: int | None = None
    min_corners: int | None = None
    max_red_cards: int | None = Field(default=None, ge=0)
    min_odd: Decimal | None = Field(default=None, gt=Decimal("1"))
    max_odd: Decimal | None = Field(default=None, gt=Decimal("1"))
    historical_hit_rate: Decimal | None = Field(default=None, gt=Decimal("0"), le=Decimal("1"))
    sample_size: int | None = Field(default=None, gt=0)
    fair_odd: Decimal | None = None
    min_edge: Decimal | None = Field(default=None, ge=Decimal("0"))
    stake_units: Decimal | None = Field(default=None, gt=Decimal("0"))
    source: str | None = None
    zeus_query: str | None = None
    scanner_condition: str | None = None
    entry_rule: str | None = None
    validation_notes: str | None = None
    notes: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("name must not be empty")
        return value

    @model_validator(mode="after")
    def validate_method_ranges(self) -> "MethodUpdate":
        non_nullable_fields = {
            "name",
            "market",
            "period",
            "status",
            "minute_start",
            "minute_end",
            "max_red_cards",
            "historical_hit_rate",
            "sample_size",
            "fair_odd",
            "min_edge",
            "stake_units",
            "source",
        }
        for field_name in non_nullable_fields:
            if field_name in self.model_fields_set and getattr(self, field_name) is None:
                raise ValueError(f"{field_name} must not be null")

        if (
            self.minute_start is not None
            and self.minute_end is not None
            and self.minute_end <= self.minute_start
        ):
            raise ValueError("minute_end must be greater than minute_start")

        if self.min_odd is not None and self.max_odd is not None:
            if self.max_odd <= self.min_odd:
                raise ValueError("max_odd must be greater than min_odd")

        return self


class MethodRead(MethodBase):
    id: int
    fair_odd: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
