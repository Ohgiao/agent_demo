from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from kb.config import get_settings

if TYPE_CHECKING:
    from langchain_postgres import PGEngine, PGVectorStore

# 由 ensure_schema() 建表的"一等公民"元数据列。
# 为什么不把它们塞进一个 JSON 列：独立列才能建索引、才能在 SQL 里做权限过滤（见 R6）。
METADATA_COLUMNS = ["doc_id", "source", "dept", "content_hash"]

_store: PGVectorStore | None = None


@lru_cache(maxsize=1)
def get_engine() -> PGEngine:
    from langchain_postgres import PGEngine

    # PGEngine 内部跑一个事件循环线程来桥接 async/sync，所以连接串必须是 asyncpg 驱动。
    return PGEngine.from_connection_string(get_settings().postgres_dsn_async)


async def ensure_schema() -> None:
    """幂等地准备 pgvector 扩展和向量表。扩展需超级用户，这一步走 psycopg 而非 SQLAlchemy。"""
    import psycopg
    from langchain_postgres import Column

    s = get_settings()
    with psycopg.connect(s.postgres_dsn, autocommit=True, connect_timeout=5) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

    await get_engine().ainit_vectorstore_table(
        table_name=s.collection_name,
        vector_size=s.embedding_dim,
        metadata_columns=[Column(name=c, data_type="TEXT", nullable=True) for c in METADATA_COLUMNS],
    )


async def get_vectorstore() -> PGVectorStore:
    """进程内单例：每请求重建 store 会反复建连接池。"""
    global _store
    from langchain_postgres import PGVectorStore

    from kb.models import get_embeddings

    if _store is None:
        _store = await PGVectorStore.create(
            engine=get_engine(),
            embedding_service=get_embeddings(),
            table_name=get_settings().collection_name,
            metadata_columns=list(METADATA_COLUMNS),
        )
    return _store
