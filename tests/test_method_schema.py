from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.domain.enums import MarketType, MethodStatus, PeriodType
from app.schemas.method import MethodCreate


def valid_method_payload() -> dict:
    return {
        "name": "Over 0.5 HT Pressao Forte",
        "description": "Metodo validado externamente no Zeus.",
        "market": MarketType.OVER_0_5_HT,
        "period": PeriodType.FIRST_HALF,
        "status": MethodStatus.ACTIVE,
        "minute_start": 15,
        "minute_end": 32,
        "score_filter": "0x0",
        "min_dangerous_attacks": 35,
        "min_total_shots": 5,
        "min_shots_on_target": 2,
        "min_corners": 3,
        "min_odd": Decimal("1.55"),
        "max_odd": Decimal("2.30"),
        "historical_hit_rate": Decimal("0.68"),
        "sample_size": 842,
        "min_edge": Decimal("0.08"),
        "stake_units": Decimal("0.5"),
    }


def test_method_create_accepts_valid_payload() -> None:
    method = MethodCreate(**valid_method_payload())

    assert method.name == "Over 0.5 HT Pressao Forte"
    assert method.market == MarketType.OVER_0_5_HT
    assert method.period == PeriodType.FIRST_HALF
    assert method.status == MethodStatus.ACTIVE
    assert method.source == "zeus"


def test_method_create_calculates_fair_odd_when_missing() -> None:
    method = MethodCreate(**valid_method_payload())

    assert method.fair_odd == Decimal("1") / Decimal("0.68")


def test_method_create_keeps_informed_fair_odd() -> None:
    payload = valid_method_payload()
    payload["fair_odd"] = Decimal("1.4705")

    method = MethodCreate(**payload)

    assert method.fair_odd == Decimal("1.4705")


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("minute_start", -1),
        ("historical_hit_rate", Decimal("0")),
        ("historical_hit_rate", Decimal("1.01")),
        ("sample_size", 0),
        ("min_odd", Decimal("1")),
        ("max_odd", Decimal("1")),
        ("min_edge", Decimal("-0.01")),
        ("stake_units", Decimal("0")),
    ],
)
def test_method_create_rejects_invalid_scalar_values(field: str, value: object) -> None:
    payload = valid_method_payload()
    payload[field] = value

    with pytest.raises(ValidationError):
        MethodCreate(**payload)


def test_method_create_rejects_minute_end_before_start() -> None:
    payload = valid_method_payload()
    payload["minute_end"] = payload["minute_start"]

    with pytest.raises(ValidationError, match="minute_end"):
        MethodCreate(**payload)


def test_method_create_rejects_max_odd_lower_than_min_odd() -> None:
    payload = valid_method_payload()
    payload["max_odd"] = Decimal("1.50")

    with pytest.raises(ValidationError, match="max_odd"):
        MethodCreate(**payload)
