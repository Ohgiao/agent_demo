from __future__ import annotations

import httpx

from kb.config import get_settings


def check_ollama() -> dict:
    """探活 Ollama，并确认所需两个模型都已本地存在。"""
    s = get_settings()
    try:
        resp = httpx.get(f"{s.ollama_base_url}/api/tags", timeout=3.0)
        resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001 - 健康检查要把任何失败如实报告
        return {"ok": False, "detail": f"{type(exc).__name__}: {exc}"}

    installed = {m["name"] for m in resp.json().get("models", [])}
    missing = [m for m in (s.chat_model, s.embedding_model) if not _is_installed(m, installed)]
    return {
        "ok": not missing,
        "models": sorted(installed),
        "missing": missing,
        "detail": f"缺少模型: {missing}" if missing else "ok",
    }


def _is_installed(wanted: str, installed: set[str]) -> bool:
    """对齐 Ollama 自身的解析规则：裸名等价于 :latest。"""
    return wanted in installed or f"{wanted}:latest" in installed


def check_postgres() -> dict:
    s = get_settings()
    import psycopg

    try:
        with psycopg.connect(s.postgres_dsn, connect_timeout=3) as conn:
            pg_version = conn.execute("select version()").fetchone()[0]
            has_vector = conn.execute(
                "select 1 from pg_extension where extname='vector'"
            ).fetchone()
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "detail": f"{type(exc).__name__}: {exc}"}

    return {
        "ok": bool(has_vector),
        "version": pg_version.split(",")[0],
        "pgvector_installed": bool(has_vector),
        "detail": "ok" if has_vector else "需要 CREATE EXTENSION vector",
    }
