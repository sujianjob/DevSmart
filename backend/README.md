# DevSmart Backend

后端用于支撑 DevSmart POC 的需求包保存、状态流转、PRD/AC 生成结果记录和评审记录。

## 本地启动

1. 安装依赖：

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 启动服务：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

3. 访问本地文档：

- 接口文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/health`

## 产品边界

后端只服务于需求澄清、PRD、AC、待确认项和评审记录，不承载代码生成、技术方案设计或研发执行流程。
