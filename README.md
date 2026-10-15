# 企业知识库骨架

技术选型（全部本地，不依赖任何云 API）：

| 层 | 选型 | 说明 |
|---|---|---|
| 接口 | FastAPI + uvicorn | `main.py` 一键起 |
| 编排 | LangChain 1.x | 只用 loader/splitter/retriever/chain 抽象，不套 agent 框架 |
| 存储 | PostgreSQL 18 + pgvector | 向量与元数据同库，能做 SQL 级权限过滤 |
| 模型 | Ollama：`bge-m3`（1024 维 embedding）+ `qwen3.5:9b`（生成） | 已本地就绪 |

## 跑起来

```bash
cp .env.example .env           # 改 KB_POSTGRES_DSN 里的密码
createdb kb_demo               # 或用 psql 建库（见 R0）
.venv/Scripts/python.exe -m pip install -e ".[dev]"
.venv/Scripts/python.exe main.py
```

打开 http://127.0.0.1:8000 —— 顶部横幅会实时显示 Ollama / PostgreSQL 的自检结果。
调用未实现的功能会返回 **501 + 题面**，页面里直接能看到这道题要做什么。

## 目录

```
src/kb/
  config.py   参数（env 驱动）          ← 已完成
  health.py   真实探活                  ← 已完成
  models.py   ChatOllama / OllamaEmbeddings ← 已完成
  store.py    PGEngine + 建表 + store 单例   ← 已完成
  api/        路由与 app 装配            ← 已完成
  web/        极简验收页                ← 已完成
  loaders.py  R1  文件 -> Document      ← 你写
  chunking.py R2  Document -> 片段      ← 你写
  ingest.py   R3  幂等入库管道           ← 你写
  search.py   R4  向量召回               ← 你写
  rag.py      R5  检索增强生成 + 拒答     ← 你写
```

## 需求阶梯

一次只做一道，做完我用验收标准卡你，过了再领下一道。
R6 之后（ACL、混合检索、增量同步、评测集、可观测）等前面通了再给。

| 编号 | 目标 | 验收 |
|---|---|---|
| **R0** | 建库 + 填 `.env` + `/healthz` 变绿 | 横幅显示 `status: ok` |
| **R1** | `loaders.load()` 支持 .md/.txt/.pdf | 单测：三种文件都产出带 source/dept/page 的 Document |
| **R2** | `chunking.split()` | 元数据不丢；overlap 越界报错；空白片被滤掉 |
| **R3** | `ingest.ingest_file()` 幂等重灌 | 同一文件传两次，第二次 `created=False`，库中片段数不变 |
| **R4** | `search.search()` | 问"年假顺延"时 HR 文档排第一，财务文档不进前 3 |
| **R5** | `rag.answer()` | 答案带 [n] 引用；空库时 `refused=True` 而不是编造 |

## 术语对照（给刚接触 RAG 的你）

| 术语 | 人话 |
|---|---|
| embedding | 把一句话变成 1024 个数字，语义越近数字越接近 |
| chunk / 切片 | 文档太长不能整篇比对，切成 500-1000 字的片段再分别向量化 |
| 召回 (retrieval) | 拿问题的向量在库里找最近的 K 个片段，只负责"找"不负责"答" |
| RAG | 先把召回片段贴进 prompt，再让模型基于它回答，减少瞎编 |
| 拒答 | 召回内容不够相关时明确说"不知道"，这是企业库的底线而非缺陷 |
