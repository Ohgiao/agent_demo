from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """所有可调参数集中在这里，环境变量前缀 KB_（见 .env.example）。"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    postgres_dsn: str = Field(default="postgresql://postgres:postgres@127.0.0.1:5432/kb_demo")
    collection_name: str = Field(default="kb_documents")

    ollama_base_url: str = Field(default="http://127.0.0.1:11434")
    chat_model: str = Field(default="qwen3.5:9b")
    embedding_model: str = Field(default="bge-m3")
    embedding_dim: int = Field(default=1024)

    chunk_size: int = Field(default=800)
    chunk_overlap: int = Field(default=120)
    top_k: int = Field(default=6)

    upload_dir: str = Field(default="data/uploads")

    @property
    def postgres_dsn_async(self) -> str:
        """SQLAlchemy 走异步驱动；LangChain 的 PostgresStore 同时需要同步串。"""
        return self.postgres_dsn.replace("postgresql://", "postgresql+asyncpg://", 1)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
