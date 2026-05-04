from decimal import Decimal
from types import SimpleNamespace

import pytest

from app.domain.enums import MarketType, MethodStatus, PeriodType
from app.schemas.method import MethodCreate, MethodUpdate
from app.services.method_service import MethodNotFoundError, MethodService, MethodValidationError


class FakeMethodRepository:
    def __init__(self) -> None:
        self.methods = {}
        self.next_id = 1

    def create(self, method):
        method.id = self.next_id
        self.next_id += 1
        self.methods[method.id] = method
        return method

    def get(self, method_id: int):
        return self.methods.get(method_id)

    def list(self, **kwargs):
        return list(self.methods.values())

    def save(self, method):
        self.methods[method.id] = method
        return method


def method_payload() -> dict:
    return {
        "name": "Over 0.5 HT Pressao Forte",
        "market": MarketType.OVER_0_5_HT,
        "period": PeriodType.FIRST_HALF,
        "minute_start": 15,
        "minute_end": 32,
        "historical_hit_rate": Decimal("0.68"),
        "sample_size": 842,
        "min_odd": Decimal("1.55"),
        "max_odd": Decimal("2.30"),
        "zeus_query": "m15-m32: placar 0x0",
        "scanner_condition": "Jogo 0x0 entre 15 e 32 minutos",
        "entry_rule": "Entrar se todas as condicoes forem atendidas",
        "validation_notes": "Validacao manual no Zeus",
    }


def create_existing_method(**overrides):
    data = method_payload()
    data.update(overrides)
    data["fair_odd"] = Decimal("1") / data["historical_hit_rate"]
    return SimpleNamespace(id=1, status=MethodStatus.ACTIVE, **data)


def test_service_creates_method_with_calculated_fair_odd() -> None:
    repository = FakeMethodRepository()
    service = MethodService(repository)

    method = service.create(MethodCreate(**method_payload()))

    assert method.id == 1
    assert method.fair_odd == Decimal("1") / Decimal("0.68")
    assert method.zeus_query == "m15-m32: placar 0x0"


def test_service_update_recalculates_fair_odd_when_hit_rate_changes() -> None:
    repository = FakeMethodRepository()
    repository.methods[1] = create_existing_method()
    service = MethodService(repository)

    method = service.update(1, MethodUpdate(historical_hit_rate=Decimal("0.70")))

    assert method.historical_hit_rate == Decimal("0.70")
    assert method.fair_odd == Decimal("1") / Decimal("0.70")


def test_service_update_preserves_explicit_fair_odd() -> None:
    repository = FakeMethodRepository()
    repository.methods[1] = create_existing_method()
    service = MethodService(repository)

    method = service.update(
        1,
        MethodUpdate(historical_hit_rate=Decimal("0.70"), fair_odd=Decimal("1.40")),
    )

    assert method.fair_odd == Decimal("1.40")


def test_service_update_validates_merged_minutes() -> None:
    repository = FakeMethodRepository()
    repository.methods[1] = create_existing_method()
    service = MethodService(repository)

    with pytest.raises(MethodValidationError):
        service.update(1, MethodUpdate(minute_start=40))


def test_service_archive_sets_archived_status() -> None:
    repository = FakeMethodRepository()
    repository.methods[1] = create_existing_method()
    service = MethodService(repository)

    method = service.archive(1)

    assert method.status == MethodStatus.ARCHIVED


def test_service_get_raises_when_method_does_not_exist() -> None:
    service = MethodService(FakeMethodRepository())

    with pytest.raises(MethodNotFoundError):
        service.get(999)
