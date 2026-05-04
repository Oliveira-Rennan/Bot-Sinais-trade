from datetime import UTC, datetime
from decimal import Decimal
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from app.api.routes.methods import get_method_service
from app.domain.enums import MarketType, MethodStatus, PeriodType
from app.main import app
from app.services.method_service import MethodNotFoundError


client = TestClient(app)


def method_payload() -> dict:
    return {
        "name": "Over 0.5 HT Pressao Forte",
        "description": "Metodo validado no Zeus para pressao ofensiva no primeiro tempo",
        "market": "OVER_0_5_HT",
        "period": "FIRST_HALF",
        "minute_start": 15,
        "minute_end": 32,
        "score_filter": "0x0",
        "min_dangerous_attacks": 35,
        "min_total_shots": 5,
        "min_shots_on_target": 2,
        "min_corners": 3,
        "max_red_cards": 0,
        "min_odd": "1.55",
        "max_odd": "2.30",
        "historical_hit_rate": "0.68",
        "sample_size": 842,
        "min_edge": "0.08",
        "stake_units": "0.5",
        "source": "zeus",
        "zeus_query": "m15-m32: placar 0x0",
        "scanner_condition": "Jogo 0x0 entre 15 e 32 minutos",
        "entry_rule": "Entrar se todas as condicoes forem atendidas",
        "validation_notes": "Validacao manual no Zeus",
        "notes": "Primeiro metodo base para MVP",
    }


def method_object(**overrides):
    now = datetime.now(UTC)
    data = {
        "id": 1,
        "name": "Over 0.5 HT Pressao Forte",
        "description": "Metodo validado no Zeus para pressao ofensiva no primeiro tempo",
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
        "max_red_cards": 0,
        "min_odd": Decimal("1.55"),
        "max_odd": Decimal("2.30"),
        "historical_hit_rate": Decimal("0.68"),
        "sample_size": 842,
        "fair_odd": Decimal("1") / Decimal("0.68"),
        "min_edge": Decimal("0.08"),
        "stake_units": Decimal("0.5"),
        "source": "zeus",
        "zeus_query": "m15-m32: placar 0x0",
        "scanner_condition": "Jogo 0x0 entre 15 e 32 minutos",
        "entry_rule": "Entrar se todas as condicoes forem atendidas",
        "validation_notes": "Validacao manual no Zeus",
        "notes": "Primeiro metodo base para MVP",
        "created_at": now,
        "updated_at": now,
    }
    data.update(overrides)
    return SimpleNamespace(**data)


class FakeMethodService:
    def __init__(self) -> None:
        self.created_payload = None
        self.list_filters = None
        self.updated_payload = None
        self.methods = {1: method_object(), 2: method_object(id=2, status=MethodStatus.ARCHIVED)}

    def create(self, payload):
        self.created_payload = payload
        return method_object(fair_odd=payload.fair_odd)

    def list(self, **filters):
        self.list_filters = filters
        status = filters.get("status")
        if status is None:
            return [method for method in self.methods.values() if method.status != MethodStatus.ARCHIVED]
        return [method for method in self.methods.values() if method.status == status]

    def get(self, method_id: int):
        if method_id not in self.methods:
            raise MethodNotFoundError
        return self.methods[method_id]

    def update(self, method_id: int, payload):
        if method_id not in self.methods:
            raise MethodNotFoundError
        self.updated_payload = payload
        if payload.historical_hit_rate is not None and payload.fair_odd is None:
            return method_object(
                id=method_id,
                historical_hit_rate=payload.historical_hit_rate,
                fair_odd=Decimal("1") / payload.historical_hit_rate,
                zeus_query=payload.zeus_query,
            )
        return method_object(id=method_id, zeus_query=payload.zeus_query)

    def archive(self, method_id: int):
        if method_id not in self.methods:
            raise MethodNotFoundError
        return method_object(id=method_id, status=MethodStatus.ARCHIVED)


@pytest.fixture
def fake_service():
    service = FakeMethodService()
    app.dependency_overrides[get_method_service] = lambda: service
    yield service
    app.dependency_overrides.clear()


def test_post_methods_creates_method_and_returns_traceability_fields(fake_service) -> None:
    response = client.post("/api/v1/methods", json=method_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Over 0.5 HT Pressao Forte"
    assert Decimal(body["fair_odd"]) == Decimal("1") / Decimal("0.68")
    assert body["zeus_query"] == "m15-m32: placar 0x0"
    assert body["scanner_condition"] == "Jogo 0x0 entre 15 e 32 minutos"
    assert body["entry_rule"] == "Entrar se todas as condicoes forem atendidas"
    assert body["validation_notes"] == "Validacao manual no Zeus"


def test_get_methods_excludes_archived_by_default(fake_service) -> None:
    response = client.get("/api/v1/methods")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["status"] == "ACTIVE"


def test_get_methods_includes_archived_when_filtered(fake_service) -> None:
    response = client.get("/api/v1/methods?status=ARCHIVED")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["status"] == "ARCHIVED"


def test_get_methods_passes_simple_filters(fake_service) -> None:
    response = client.get("/api/v1/methods?market=OVER_0_5_HT&period=FIRST_HALF&limit=50&offset=0")

    assert response.status_code == 200
    assert fake_service.list_filters["market"] == MarketType.OVER_0_5_HT
    assert fake_service.list_filters["period"] == PeriodType.FIRST_HALF
    assert fake_service.list_filters["limit"] == 50
    assert fake_service.list_filters["offset"] == 0


def test_get_method_by_id_returns_existing_method(fake_service) -> None:
    response = client.get("/api/v1/methods/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_method_by_id_returns_404_when_missing(fake_service) -> None:
    response = client.get("/api/v1/methods/999")

    assert response.status_code == 404


def test_patch_method_updates_traceability_and_recalculates_fair_odd(fake_service) -> None:
    response = client.patch(
        "/api/v1/methods/1",
        json={"historical_hit_rate": "0.70", "zeus_query": "nova query zeus"},
    )

    assert response.status_code == 200
    body = response.json()
    assert Decimal(body["fair_odd"]) == Decimal("1") / Decimal("0.70")
    assert body["zeus_query"] == "nova query zeus"


def test_patch_method_returns_404_when_missing(fake_service) -> None:
    response = client.patch("/api/v1/methods/999", json={"name": "Novo nome"})

    assert response.status_code == 404


def test_delete_method_archives_method(fake_service) -> None:
    response = client.delete("/api/v1/methods/1")

    assert response.status_code == 200
    assert response.json()["status"] == "ARCHIVED"


def test_delete_method_returns_404_when_missing(fake_service) -> None:
    response = client.delete("/api/v1/methods/999")

    assert response.status_code == 404
