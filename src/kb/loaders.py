from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document


def load(path: Path, *, dept: str) -> list[Document]:
    """R1：把磁盘文件读成 LangChain Document 列表（一个文件一个 Document）。

    要求
    ----
    - 支持 .md / .txt / .pdf，其余后缀抛 ValueError。
    - .txt/.md 用 utf-8 读，遇到 GBK 中文文件不能崩（提示：errors 或 chardet 思路）。
    - .pdf 用已装好的 pypdf，逐页一个 Document。
    - 每个 Document 的 metadata 至少含：source(文件名)、dept、page(从 0 起)。
      不要把 doc_id / content_hash 放进来，那是 R3 的职责。

    参考
    ----
    - Document(page_content=str, metadata=dict)
    - pypdf.PdfReader(path).pages[i].extract_text()
    - 不必引入 langchain-community，自己 20 行写完更清楚。
    """
    raise NotImplementedError("R1 未实现：文件 -> Document 列表")
