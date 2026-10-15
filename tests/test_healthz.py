from __future__ import annotations

from fastapi.testclient import TestClient

from kb.api.app import create_app


def test_healthz_reports_both_backends() -> None:
    with TestClient(create_app()) as client:
        resp = client.get("/healthz")
        assert resp.status_code == 200
        body = resp.json()
        assert {"status", "ollama", "postgres", "collection"} <= set(body)
        assert body["ollama"]["ok"] is True, f"Ollama 不可用: {body['ollama']['detail']}"


def test_unimplemented_stub_returns_501_with_the_assignment() -> None:
    with TestClient(create_app()) as client:
        resp = client.post("/api/search", json={"query": "年假可以顺延吗"})
        assert resp.status_code == 501
        assert "R4" in resp.json()["detail"]
