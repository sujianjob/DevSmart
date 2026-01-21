# Web Scraper - 输出模板

本文档包含所有输出文件的标准模板。

---

## README.md 总目录模板

```markdown
# {网站名称} - 文档爬取结果

> 爬取时间：{YYYY-MM-DD HH:mm:ss}
> 来源网站：{原始URL}
> 总页面数：{N} 页

## 目录

- [00_快速入门](./00_快速入门/)
  - [介绍](./00_快速入门/01_介绍.md)
  - [注册流程](./00_快速入门/02_注册流程.md)
- [01_认证授权](./01_认证授权/)
  - [OAuth2.0](./01_认证授权/01_OAuth2.0.md)
  ...

## 爬取报告

### 统计信息

| 指标 | 数值 |
|-----|------|
| 总页面数 | {N} |
| 成功爬取 | {M} |
| 跳过页面 | {K} |
| 失败页面 | {F} |
| 爬取耗时 | {T} |

### 覆盖板块

- [x] 快速入门
- [x] 认证授权
- [x] API 参考
- [x] SDK
- [x] 错误码
- [ ] 更新日志（未找到）

### 遗漏页面

（如有无法访问的页面列在此处）

| URL | 错误原因 | 重试次数 |
|-----|---------|---------|
| /api/deprecated | 404 | 3 |
```

---

## 单页 Markdown 模板

```markdown
# {页面标题}

> 原始链接：{原始URL}
> 所属分类：{导航路径}

---

{页面正文内容}

---

## 相关链接

- [上一篇：xxx](./xxx.md)
- [下一篇：xxx](./xxx.md)
```

---

## API 文档结构化模板

```markdown
## {接口名称}

### 基本信息

- **接口地址**：`POST /api/v1/endpoint`
- **请求方式**：POST
- **Content-Type**：application/json

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| param1 | string | 是 | 参数说明 |
| param2 | int | 否 | 参数说明 |

### 响应参数

| 参数名 | 类型 | 说明 |
|-------|------|------|
| code | int | 状态码 |
| data | object | 返回数据 |

### 请求示例

\`\`\`json
{
  "param1": "value1"
}
\`\`\`

### 响应示例

\`\`\`json
{
  "code": 0,
  "data": {}
}
\`\`\`
```

---

## 爬取状态文件模板

`.scraper-state.json`

```json
{
  "version": "1.0",
  "site": {
    "entry_url": "https://open.example.com/doc",
    "site_type": "spa",
    "preset": "generic-docs"
  },
  "progress": {
    "phase": "crawl",
    "started_at": "2024-01-15T10:30:00Z",
    "last_updated": "2024-01-15T11:45:00Z",
    "total_discovered": 45,
    "completed": 23,
    "failed": 2,
    "pending": 20
  },
  "navigation_tree": {
    "快速入门": {
      "expanded": true,
      "children": ["介绍", "注册流程"]
    },
    "API参考": {
      "expanded": true,
      "children": {
        "账号服务": {
          "expanded": true,
          "children": ["客户信息", "资质管理"]
        }
      }
    }
  },
  "url_queue": [
    {
      "url": "/api/user",
      "status": "completed",
      "file": "01_API/user.md",
      "completed_at": "2024-01-15T10:35:00Z"
    },
    {
      "url": "/api/order",
      "status": "pending"
    },
    {
      "url": "/api/pay",
      "status": "failed",
      "error": "timeout",
      "retries": 2
    }
  ]
}
```

---

## 目录命名规则

```
{序号}_{目录名}/
├── {序号}_{文件名}.md
```

- 序号：两位数字，从 00 开始
- 目录名/文件名：使用原网站导航名称
- 特殊字符替换为下划线

### 示例目录结构

```
{网站名称}_scraped/
├── README.md                    # 总目录索引 + 爬取报告
├── .scraper-state.json          # 状态文件（断点续爬）
├── 00_快速入门/
│   ├── 01_介绍.md
│   ├── 02_注册流程.md
│   └── 03_第一个请求.md
├── 01_认证授权/
│   ├── 01_OAuth2.0.md
│   ├── 02_获取AccessToken.md
│   └── 03_权限范围.md
├── 02_API参考/
│   ├── README.md                # 分类索引
│   ├── 账号服务/
│   │   ├── 客户信息.md
│   │   └── 资质管理.md
│   └── 投放管理/
│       ├── 计划管理.md
│       └── 创意管理.md
├── 03_SDK/
│   ├── Java_SDK.md
│   ├── Python_SDK.md
│   └── 下载链接.md
├── 04_错误码/
│   └── 错误码列表.md
├── 05_更新日志/
│   └── 版本历史.md
└── _assets/
    └── images.md                # 引用的图片链接记录
```

---

## 进度显示格式

### 实时进度

```
📊 爬取进度: [████████░░░░░░░░] 23/45 (51%)
   ├─ 当前: 账号服务 > 客户信息管理 > 获取客户信息
   ├─ 耗时: 12分钟
   └─ 状态: ✓ 23 | ✗ 2 | ○ 20
```

### 板块完成提示

```
✅ 完成板块: 账号服务 (8/8 页)
⏳ 下一板块: 投放管理
```

### 错误提示

```
⚠️ 爬取失败: /api/deprecated
   原因: 404 Not Found
   操作: 已跳过，记录到失败列表
```

### 最终报告

```
🎉 爬取完成！

📁 输出目录: ./oceanengine_scraped/
📊 统计:
   - 总页面: 45
   - 成功: 43
   - 失败: 2
   - 耗时: 25分钟

📝 查看详情: ./oceanengine_scraped/README.md
```
