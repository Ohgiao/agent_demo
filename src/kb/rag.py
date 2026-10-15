from __future__ import annotations

from kb.schemas import AskResponse


async def answer(question: str, *, top_k: int, dept: str | None = None) -> AskResponse:
    """R5：检索增强生成。

    要求
    ----
    - 先调 search.search() 拿片段；召回为空或最高分低于阈值时直接返回
      AskResponse(text="知识库中没有相关内容", citations=[], refused=True)。
      这条分支叫"拒答"，是企业知识库最重要的一道护栏。
    - 拼 prompt：System 里给规则，Human 里按 [1] [2] 编号注入片段正文和 source。
      推荐 langchain_core.prompts.ChatPromptTemplate.from_messages。
    - 调 models.get_chat_model()，用 `prompt | llm` 组成链，await chain.ainvoke(...)。
    - 要求模型在答案里用 [n] 标注引用；citations 只回传真正被引用的片段。
    - 上下文总长控制在模型 num_ctx 内：按 score 从高到低累加，超预算就截断，
      不要无脑把 top_k 全部塞进去。

    注意 qwen3.5 是思考型模型：回答会带 reasoning 内容，
    取 `res.content` 时若发现混入思考过程，考虑关 thinking 或做后处理（可选加分项）。
    """
    raise NotImplementedError("R5 未实现：问答链")
