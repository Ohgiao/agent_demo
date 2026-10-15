from __future__ import annotations

from langchain_core.documents import Document


def split(docs: list[Document], *, chunk_size: int, chunk_overlap: int) -> list[Document]:
    """R2：把整篇文档切成待入库的片段。

    要求
    ----
    - 优先用 langchain_text_splitters.MarkdownHeaderTextSplitter 或
      RecursiveCharacterTextSplitter；想手写也可以，但要能解释你的边界选择。
    - 切片后每个 Document 的 metadata 必须保留父文档的 source / dept，
      并新增 chunk_index(从 0 起的 int)。
      ⚠ metadata 在切片时最容易丢，丢了 R6 的权限过滤就没法做。
    - chunk_overlap 必须有上限保护，overlap >= chunk_size 时抛 ValueError。
    - 空白片段（strip 后为空）要过滤掉。

    验收标准见 R2：同一份 samples/hr-leave.md，chunk_size=800 与 200 的
    召回质量差异要能用人话解释。
    """
    raise NotImplementedError("R2 未实现：Document 列表 -> 片段列表")
