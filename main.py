# 运行入口：PyCharm 里直接点右键运行即可，等价于 uvicorn kb.api.app:app --reload。

import uvicorn

if __name__ == "__main__":
    uvicorn.run("kb.api.app:app", host="127.0.0.1", port=8000, reload=True)
