from __future__ import annotations

from pathlib import Path

from kb.schemas import IngestResult


async def ingest_file(path: Path, *, dept: str) -> IngestResult:
    """R3：串起 load -> split -> 算 doc_id/content_hash -> 写入向量库。

    要求
    ----
    - doc_id = 文件内容 sha256 前 16 位（不要用文件名，同名覆盖是事故源）。
    - content_hash 同 doc_id 即可；写入前先查库：已存在同 doc_id 则删除旧片段再写，
      返回 IngestResult(created=False)。这一步叫"幂等重灌"，没有它每次重跑
      知识库就会同时存在新旧两份矛盾内容，检索时一起召回。
    - 用 store.get_vectorstore() 拿 PGVectorStore，
      调 await vs.aadd_documents(chunks, ids=[...])。
      ⚠ ids 必须每片唯一且稳定，推荐 f"{doc_id}:{chunk_index}" 的 sha1。
    - 切片文本放进 Document.page_content，元数据放进 metadata。

    提示
    ----
    embedding 调用是这里唯一的慢操作，本地 bge-m3 约 0.1-0.3s/片。
    先打日志看耗时，别急着优化。
    """
    raise NotImplementedError("R3 未实现：入库管道")
