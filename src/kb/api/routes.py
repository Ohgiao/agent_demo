from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from kb import health, ingest, rag, search
from kb.config import get_settings
from kb.schemas import AskRequest, AskResponse, IngestResult, SearchRequest, SearchResponse

router = APIRouter()

ALLOWED_SUFFIXES = {".md", ".txt", ".pdf"}


@router.get("/healthz")
def healthz() -> dict:
    """自检：Ollama 与两个模型、PostgreSQL 与 pgvector 扩展，全部真实探活。"""
    ollama = health.check_ollama()
    postgres = health.check_postgres()
    return {
        "status": "ok" if ollama["ok"] and postgres["ok"] else "degraded",
        "ollama": ollama,
        "postgres": postgres,
        "collection": get_settings().collection_name,
    }


@router.post("/api/documents", response_model=IngestResult)
async def upload_document(file: UploadFile = File(...), dept: str = Form(...)) -> IngestResult:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(415, f"只支持 {sorted(ALLOWED_SUFFIXES)}，收到 {suffix or '(无后缀)'}")

    target_dir = Path(get_settings().upload_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    # 落盘用随机名，避免上传文件名里的路径穿越（../../etc/passwd）直接变成磁盘路径。
    path = target_dir / f"{uuid.uuid4().hex}{suffix}"
    path.write_bytes(await file.read())

    return await ingest.ingest_file(path, dept=dept)


@router.post("/api/search", response_model=SearchResponse)
async def search_endpoint(req: SearchRequest) -> SearchResponse:
    hits = await search.search(req.query, top_k=req.top_k or get_settings().top_k, dept=req.dept)
    return SearchResponse(hits=hits)


@router.post("/api/ask", response_model=AskResponse)
async def ask_endpoint(req: AskRequest) -> AskResponse:
    return await rag.answer(
        req.question, top_k=req.top_k or get_settings().top_k, dept=req.dept
    )
