from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "bot-over-signals",
    }


def test_api_v1_health_check() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "bot-over-signals",
    }
