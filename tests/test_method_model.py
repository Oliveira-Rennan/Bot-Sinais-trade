from decimal import Decimal

from app.domain.enums import MarketType, MethodStatus, PeriodType
from app.models.method import Method


def test_method_model_can_be_created() -> None:
    method = Method(
        name="Over 0.5 HT Pressao Forte",
        description="Metodo validado externamente no Zeus.",
        market=MarketType.OVER_0_5_HT,
        period=PeriodType.FIRST_HALF,
        status=MethodStatus.ACTIVE,
        minute_start=15,
        minute_end=32,
        score_filter="0x0",
        min_dangerous_attacks=35,
        min_total_shots=5,
        min_shots_on_target=2,
        min_corners=3,
        max_red_cards=0,
        min_odd=Decimal("1.55"),
        max_odd=Decimal("2.30"),
        historical_hit_rate=Decimal("0.68"),
        sample_size=842,
        fair_odd=Decimal("1.4705"),
        min_edge=Decimal("0.08"),
        stake_units=Decimal("0.5"),
        source="zeus",
    )

    assert method.name == "Over 0.5 HT Pressao Forte"
    assert method.market == MarketType.OVER_0_5_HT
    assert method.period == PeriodType.FIRST_HALF
    assert method.status == MethodStatus.ACTIVE
    assert method.fair_odd == Decimal("1.4705")
