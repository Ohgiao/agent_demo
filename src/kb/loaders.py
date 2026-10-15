from __future__ import annotations

from pathlib import Path
from pypdf import PdfReader
import chardet
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
    docs: list[Document] = []

    suffix = path.suffix.lower()
    if suffix in (".txt", ".md"):
        # 二进制读取，用chardet自动判断编码，解决GBK/utf8中文乱码
        raw = path.read_bytes()
        enc_info = chardet.detect(raw)
        encoding = enc_info["encoding"] or "utf-8"
        text = raw.decode(encoding, errors="replace")
        # txt/md：整个文件作为1个Document，page固定0
        docs.append(Document(
            page_content=text,
            metadata={
                "source": path.name,
                "dept": dept,
                "page": 0
            }
        ))

    elif suffix == ".pdf":
        reader = PdfReader(path)
        for page_idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            docs.append(Document(
                page_content=page_text,
                metadata={
                    "source": path.name,
                    "dept": dept,
                    "page": page_idx
                }
            ))
    else:
        raise ValueError(f"不支持的文件类型：{suffix}，仅支持 .txt .md .pdf")

    return docs
