from __future__ import annotations

from kb.schemas import SearchHit


async def search(query: str, *, top_k: int, dept: str | None = None) -> list[SearchHit]:
    """R4：向量召回。R6 会在此基础上加权限过滤。

    要求
    ----
    - vs = await store.get_vectorstore()
    - 用 await vs.asimilarity_search_with_score(query, k=top_k) 拿到 (Document, score)。
      注意 pgvector 的 cosine distance 越小越像，而 SearchHit.score 约定越大越像，
      你要自己换算并保证落在 0-1。
    - 组装 SearchHit：chunk_id 用 Document 的 id，doc_id/source/dept 从 metadata 取。
      取不到就填 None，别让一次检索因为一个坏元数据整段失败。
    - 先不加阈值过滤（R4 只要召回正确），但把 top_k 传对。

    验收方式
    --------
    问一个只出现在 hr-leave.md 里的词，它必须排第一；
    问一个财务词，HR 文档不能进前 3。做不到就先看切片，再看 embedding。
    """
    raise NotImplementedError("R4 未实现：向量检索")
