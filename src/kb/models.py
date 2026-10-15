from __future__ import annotations

from functools import lru_cache

from langchain_ollama import ChatOllama, OllamaEmbeddings

from kb.config import get_settings


@lru_cache(maxsize=1)
def get_embeddings() -> OllamaEmbeddings:
    """文本 -> 1024 维向量。bge-m3 是中文效果较好的本地 embedding 模型。"""
    s = get_settings()
    return OllamaEmbeddings(base_url=s.ollama_base_url, model=s.embedding_model)


@lru_cache(maxsize=1)
def get_chat_model() -> ChatOllama:
    """生成层模型。检索问答场景下 temperature 要低，避免复述时改写事实。"""
    s = get_settings()
    return ChatOllama(base_url=s.ollama_base_url, model=s.chat_model, temperature=0)
