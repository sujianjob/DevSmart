# DevSmart Backend

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

3. 访问接口：

- 文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/health`
