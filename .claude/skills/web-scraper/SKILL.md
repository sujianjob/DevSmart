---
name: web-scraper
description: 基于 agent-browser 的智能网站爬取工具。完整抓取开放平台、API 文档网站，自动发现导航结构，遍历所有页面，输出多文件目录结构。
---

# Web Scraper - 智能网站爬取工具

基于 `agent-browser` 的智能爬取工具，专门针对开放平台、API 文档网站。

---

## 快速开始

```bash
# 1. 打开目标网站
agent-browser open https://open.example.com/docs

# 2. 获取快照，分析导航结构
agent-browser snapshot -i

# 3. 按工作流执行爬取
```

### 完整示例

```bash
agent-browser open https://open.example.com/docs
agent-browser wait --load networkidle
agent-browser snapshot -i
# 展开所有菜单 -> 遍历所有页面 -> 保存内容
agent-browser close
```

---

## 网站类型识别

在开始爬��前，**必须先识别网站类型**：

```bash
agent-browser open <目标URL>
agent-browser wait 3000
agent-browser click "某个菜单项"
agent-browser wait 2000
# 观察：页面是否白屏刷新？
```

### 类型判断表

| 类型 | 特征 | 爬取策略 |
|-----|------|---------|
| **传统多页网站** | 点击链接后整页刷新（白屏）| 可直接 `open` URL |
| **SPA 单页应用** | 点击链接无刷新，内容局部更新 | **必须通过 `click` 导航** |
| **混合类型** | 部分链接刷新，部分不刷新 | 分情况处理 |

### SPA 识别要点

如果出现以下情况，则为 **SPA 网站**：
1. 点击菜单后，URL 变了但页面没有白屏刷新
2. 页面切换有淡入淡出或滑动动画
3. 直接访问子页面 URL 显示的是首页内容
4. 使用了 React/Vue/Angular 等框架

**SPA 核心规则**：
```
🚫 不要用 agent-browser open <子页面URL>
✅ 必须用 agent-browser click "菜单项" 来导航
```

**SPA 爬取策略**：
1. 只在开始时 `open` 一次首页 URL
2. 之后所有页面切换都通过 `click` 导航链接
3. 每次 `click` 后必须 `wait 2000+` ms
4. 通过 `get url` 确认 URL 已变化
5. 如需返���上级，用 `click` 返回导航，不用 `back`

---

## 核心工作流（5 阶段）

### 阶段一：初始化与站点探测

```bash
agent-browser open <目标URL>
agent-browser wait --load networkidle
agent-browser wait 2000
agent-browser screenshot homepage.png --full
agent-browser get title
```

**输出**：创建目录 `{网站名称}_scraped/`

### 阶段二：导航结构分析（关键）

**⚠️ 必须确保所有嵌套菜单都完全展开！**

```bash
agent-browser snapshot -i
# 识别 nav, sidebar, menu 元素
# 识别折叠按钮（▸ ▾ + - 箭头图标）
```

#### 递归展开算法

```
1. 截图并获取 snapshot -i
2. 识别所有"折叠状态"的菜单项：
   - 带有 ▸ ▶ + 箭头的项
   - aria-expanded="false" 的项
3. 如果找到折叠项：
   a. 点击第一个折叠项的展开按钮
   b. 等待 500-1000ms
   c. 重新获取 snapshot -i
   d. 回到步骤 2（递归）
4. 如果没有更多折叠项，进入下一阶段
```

**具体命令**：

```bash
# === 展开一级菜单 ===
agent-browser snapshot -i
agent-browser click "建站管理"
agent-browser wait 800
agent-browser snapshot -i

# === 展开二级菜单 ===
agent-browser click "橙子建站落地页管理"
agent-browser wait 800
agent-browser snapshot -i

# === 继续直到所有叶子节点 ===
```

**判断菜单是否需要展开**：

| 特征 | 说明 |
|-----|------|
| 箭头图标 ▸ ▶ + | 表示折叠 |
| 箭头图标 ▾ ▼ - | 表示已展开 |
| aria-expanded="false" | 折叠状态 |

**常见陷阱**：
- 有些菜单点击文字是导航，点击箭头才是展开
- 部分菜单需要 `hover` 而不是 `click`
- 子菜单可能异步加载，需足够等待时间

### 阶段三：深度遍历爬取

```bash
# 对队列中每个页面执行：
agent-browser click "目标链接"   # SPA 用 click
agent-browser wait 2000
agent-browser get title
agent-browser snapshot           # 获取内容
# 保存为 Markdown 文件
```

**遍历规则**：广度优先、同域优先、自动去重

### 阶段四：内容结构化

```
{网站名称}_scraped/
├── README.md                    # 总目录 + 爬取报告
├── .scraper-state.json          # 状态文件（断点续爬）
├── 00_快速入门/
│   ├── 01_介绍.md
│   └── 02_注册流程.md
├── 01_认证授权/
│   └── 01_OAuth2.0.md
├── 02_API参考/
│   ├── 账号服务/
│   │   └── 客户信息.md
│   └── 投放管理/
└── _assets/
    └── images.md
```

### 阶段五：完整性校验

```bash
# 统计爬取结果
# 检查关键内容（认证、API、SDK、错误码）
# 生成爬取报告
agent-browser close
```

---

## 状态管理（断点续爬）

### 状态文件

爬取过程会自动生成 `.scraper-state.json`：

```json
{
  "version": "1.0",
  "site": {
    "entry_url": "https://open.example.com/doc",
    "site_type": "spa",
    "preset": "oceanengine"
  },
  "progress": {
    "phase": "crawl",
    "started_at": "2024-01-15T10:30:00Z",
    "total_discovered": 45,
    "completed": 23,
    "failed": 2,
    "pending": 20
  },
  "url_queue": [
    {"url": "/api/user", "status": "completed", "file": "01_API/user.md"},
    {"url": "/api/order", "status": "pending"},
    {"url": "/api/pay", "status": "failed", "error": "timeout", "retries": 2}
  ]
}
```

### 恢复逻辑

1. 检测输出目录是否存在 `.scraper-state.json`
2. 提示用户是否继续上次任务
3. 从 `url_queue` 中找到第一个 `pending` 项继续

### 进度显示

```
📊 爬取进度: [████████░░░░░░░░] 23/45 (51%)
   ├─ 当前: 账号服务 > 客户信息管理 > 获取客户信息
   ├─ 耗时: 12分钟
   └─ 状态: ✓ 23 | ✗ 2 | ○ 20

✅ 完成板块: 账号服务 (8/8 页)
⏳ 下一板块: 投放管理
```

### 错误恢复策略

| 错误类型 | 处理策略 |
|---------|---------|
| 网络超时 | 重试 3 次，指数退避 (1s, 3s, 10s) |
| 元素未找到 | 重试 2 次，截图记录 |
| 404/500 | 记录到失败列表，跳过继续 |
| 登录过期 | 暂停，提示用户处理 |

---

## 预设配置

预设是针对特定网站优化的配置模板。

### 可用预设

| 预设 | 适用网站 |
|-----|---------|
| `oceanengine` | 巨量引擎开放平台 |
| `wechat-open` | 微信开放平台 |
| `generic-docs` | 通用文档站点 |

### 使用方式

```bash
# 自动检测
agent-browser open https://open.oceanengine.com/doc
# -> "检测到预设 'oceanengine'，是否使用？"

# 手动指定
# 用户指令: "使用 oceanengine 预设爬取"
```

### 自动检测逻辑

1. 获取当前 URL 的域名
2. 匹配 `presets/*.yaml` 中的 `url_pattern`
3. 找到匹配则提示使用

详见 [presets/README.md](./presets/README.md)

---

## 输出格式

### 目录命名规则

```
{序号}_{目录名}/
├── {序号}_{文件名}.md
```

- 序号：两位数字，从 00 开始
- 目录名/文件名：使用原网站导航名称
- 特殊字符替换为下划线

### README.md 总目录

```markdown
# {网站名称} - 文档爬取结果

> 爬取时间：{YYYY-MM-DD HH:mm:ss}
> 来源网站：{原始URL}
> 总页面数：{N} 页

## 目录
...

## 爬取报告
### 统计信息
| 指标 | 数值 |
|-----|------|
| 总页面数 | {N} |
| 成功爬取 | {M} |
```

详细模板见 [TEMPLATES.md](./TEMPLATES.md)

---

## 命令速查

### 导航

| 命令 | 说明 |
|-----|------|
| `open <url>` | 打开页面 |
| `back` / `forward` | 前��/后退 |
| `close` | 关闭浏览器 |

### 快照

| 命令 | 说明 |
|-----|------|
| `snapshot` | 完整 DOM 树 |
| `snapshot -i` | 仅交互元素（带 @ref） |
| `snapshot -c` | 紧凑输出 |

### 交互

| 命令 | 说明 |
|-----|------|
| `click @e1` | 点击元素 |
| `click "文字"` | 点击文字 |
| `hover @e1` | 悬停元素 |
| `scroll down 500` | 向下滚动 |

### 获取信息

| 命令 | 说明 |
|-----|------|
| `get text @e1` | 获取元素文本 |
| `get title` | 获取页面标题 |
| `get url` | 获取当前 URL |

### 等待

| 命令 | 说明 |
|-----|------|
| `wait @e1` | 等待元素出现 |
| `wait 2000` | 等待 2 秒 |
| `wait --load networkidle` | 等待网络空闲 |

### 截图

| 命令 | 说明 |
|-----|------|
| `screenshot path.png` | 保存截图 |
| `screenshot --full` | 完整页面截图 |

---

## 更多资源

- **高级功能**：[ADVANCED.md](./ADVANCED.md)
  - 6 种链接发现策略
  - 动态内容处理
  - URL 过滤规则
  - 可视化模式
  - 模型选择建议
  - 常见问题 Q&A

- **输出模板**：[TEMPLATES.md](./TEMPLATES.md)
  - README 总目录模板
  - 单页 Markdown 模板
  - API 文档结构化模板
  - 状态文件格式

- **预设配置**：[presets/](./presets/)
  - 预设使用说明
  - 巨量引擎预设
  - 微信开放平台预设
  - 通用文档站点预设
