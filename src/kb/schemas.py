from __future__ import annotations

from pydantic import BaseModel, Field


class IngestResult(BaseModel):
    doc_id: str
    source: str
    chunks: int
    created: bool = Field(description="内容 hash 未变化时应返回 False（幂等，见 R3）")


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=50)
    dept: str | None = Field(default=None, description="调用者所属部门，R6 起用于权限过滤")


class SearchHit(BaseModel):
    chunk_id: str
    doc_id: str
    source: str
    dept: str | None
    text: str
    score: float = Field(description="相似度 0-1，越大越相关")


class SearchResponse(BaseModel):
    hits: list[SearchHit]


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=50)
    dept: str | None = None


class AskResponse(BaseModel):
    text: str
    citations: list[SearchHit]
    refused: bool = Field(description="召回不足时应为 True，而不是硬编一个答案")
