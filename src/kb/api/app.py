from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

from kb import store
from kb.api.routes import router

log = logging.getLogger("kb")

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """建表失败不阻止启动：让 /healthz 明确告诉你缺什么，而不是进程直接退出。"""
    try:
        await store.ensure_schema()
        log.info("向量表就绪")
    except Exception as exc:  # noqa: BLE001
        log.warning("跳过建表（%s: %s）—— 请检查 .env 里的 KB_POSTGRES_DSN", type(exc).__name__, exc)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="企业知识库骨架", lifespan=lifespan)
    app.include_router(router)

    # 未实现的需求桩一律返回 501 + 题面，页面里能直接看到"这道题还没做"。
    @app.exception_handler(NotImplementedError)
    async def _501(request: Request, exc: NotImplementedError) -> JSONResponse:
        return JSONResponse(status_code=501, content={"detail": str(exc)})

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    return app


app = create_app()
