---
name: web-scraper
description: 基于 agent-browser 的智能网站爬取工具。完整抓取开放平台、API 文档网站，自动发现导航结构，遍历所有页面，输出多文件目录结构。
---

# Web Scraper - 智能网站爬取工具

基于 `agent-browser` 能力的智能网站爬取 skill，专门针对开放平台、API 文档网站，自动发现导航结构，遍历所有页面，输出结构化的多文件 Markdown 文档。

---

## 🔍 第一步：识别网站类型

在开始爬取前，**必须先识别网站类型**，这决定了后续的爬取策略：

```bash
# 1. 打开网站，观察加载过程
agent-browser open <目标URL>
agent-browser wait 3000
agent-browser screenshot site_type_check.png

# 2. 点击任意导航链接，观察行为
agent-browser click "某个菜单项"
agent-browser wait 2000
```

### 网站类型判断表

| 类型 | 特征 | 爬取策略 |
|-----|------|---------|
| **传统多页网站** | 点击链接后整页刷新（白屏）| 可以直接 `open` URL |
| **SPA 单页应用** | 点击链接无刷新，内容局部更新 | **必须通过 `click` 导航** |
| **混合类型** | 部分链接刷新，部分不刷新 | 分情况处理 |
| **需要登录** | 出现登录弹窗或跳转登录页 | 先登录再爬取 |

### ⚠️ SPA 网站识别要点

如果出现以下情况，则为 **SPA 网站**：
1. ✅ 点击菜单后，URL 变了但页面没有白屏刷新
2. ✅ 页面切换有淡入淡出或滑动动画
3. ✅ 直接访问子页面 URL 显示的是首页内容
4. ✅ 查看源码有 React/Vue/Angular 标识

**SPA 网站的核心规则**：
```
🚫 不要用 agent-browser open <子页面URL>
✅ 必须用 agent-browser click "菜单项" 来导航
```

---

## 模型选择建议（Opus vs Sonnet）

执行此 skill 时，不同模型有不同的表现特点：

| 特性 | Claude Opus | Claude Sonnet |
|-----|-------------|---------------|
| **复杂导航分析** | ⭐⭐⭐ 最佳 | ⭐⭐ 良好 |
| **SPA 识别准确度** | ⭐⭐⭐ 高 | ⭐⭐ 中等 |
| **递归展开策略** | ⭐⭐⭐ 深度理解 | ⭐⭐ 基本正确 |
| **异常处理能力** | ⭐⭐⭐ 全面 | ⭐⭐ 常见场景 |
| **执行速度** | ⭐ 较慢 | ⭐⭐⭐ 快 |
| **Token 成本** | ⭐ 高 | ⭐⭐⭐ 低 |

### 推荐使用场景

| 场景 | 推荐模型 | 原因 |
|-----|---------|------|
| **复杂 SPA 网站**（如巨量引擎） | Opus | 需要准确识别多层嵌套菜单，处理复杂的导航逻辑 |
| **简单文档站点** | Sonnet | 结构清晰，Sonnet 足够处理，速度更快 |
| **首次探测新网站** | Opus | 更好地理解网站结构和类型 |
| **批量爬取同类网站** | Sonnet | 策略已确定，执行即可，节省成本 |
| **调试和测试** | Sonnet | 快速迭代，成本较低 |

### 切换模型方法

在 Claude Code 中可以通过以下方式指定模型：
```bash
# 使用 Opus（复杂任务）
claude --model opus

# 使用 Sonnet（快速任务）
claude --model sonnet
```

---

## 可视化模式配置

爬取过程默认在后台无界面运行（headless 模式）。如需可视化查看爬取过程，可开启可视化模式。

### 🎬 开启可视化模式

在爬取开始前声明使用可视化模式：

```
我要开启可视化模式爬取网站，请：
1. 使用 --headed 参数显示浏览器窗口
2. 每个关键步骤都截图保存
3. 截图命名格式：step_{序号}_{操作描述}.png
```

### 可视化模式命令变化

| 操作 | 普通模式 | 可视化模式 |
|-----|---------|-----------|
| 打开页面 | `agent-browser open <url>` | `agent-browser open <url> --headed` |
| 首页截图 | （跳过） | `agent-browser screenshot step_01_homepage.png --full` |
| 展开菜单 | `agent-browser click "菜单"` | `agent-browser click "菜单"` + `agent-browser screenshot step_02_expand_menu.png` |
| 页面切换 | `agent-browser click "链接"` | `agent-browser click "链接"` + `wait 2000` + `screenshot step_03_page_xxx.png` |

### 可视化模式工作流示例

```bash
# === 可视化模式：完整命令序列 ===

# 1. 打开浏览器（可视化）
agent-browser open https://open.example.com/docs --headed
agent-browser wait 3000
agent-browser screenshot step_01_homepage.png --full

# 2. 分析导航结构
agent-browser snapshot -i
agent-browser screenshot step_02_navigation.png

# 3. 展开菜单（每次展开都截图）
agent-browser click "账号服务"
agent-browser wait 1000
agent-browser screenshot step_03_expand_account.png

agent-browser click "客户信息管理"
agent-browser wait 1000
agent-browser screenshot step_04_expand_customer.png

# 4. 访问页面（每个页面都截图）
agent-browser click "获取客户信息"
agent-browser wait 2000
agent-browser screenshot step_05_page_get_customer.png
agent-browser snapshot

# ... 继续爬取，每步都截图 ...

# 5. 爬取完成
agent-browser screenshot step_final_complete.png
agent-browser close
```

### 截图文件命名规范

```
step_{序号}_{操作类型}_{描述}.png

示例：
step_01_init_homepage.png          # 初始化-首页
step_02_nav_sidebar.png            # 导航-侧边栏
step_03_expand_api_reference.png   # 展开-API参考
step_04_page_get_token.png         # 页面-获取Token
step_05_scroll_bottom.png          # 滚动-底部
step_final_complete.png            # 最终-完成
```

### 可视化模式的用途

1. **调试问题**：观察哪一步出错，元素是否正确定位
2. **验证结果**：确认爬取到的内容是否完整
3. **学习网站结构**：了解 SPA 的导航行为
4. **生成演示**：截图可用于文档或报告

---

## 快速开始（3 步启动）

```bash
# 1. 打开目标网站
agent-browser open https://open.example.com/docs

# 2. 获取快照，分析导航结构
agent-browser snapshot -i

# 3. 开始爬取（按下方工作流执行）
```

---

## 完整爬取工作流（5 个阶段）

### 阶段一：初始化与站点探测

```bash
# 1. 打开入口 URL
agent-browser open <目标URL>

# 2. 等待页面完全加载
agent-browser wait --load networkidle
agent-browser wait 2000  # 额外等待 SPA 渲染

# 3. 截图保存首页快照
agent-browser screenshot homepage.png --full

# 4. 获取页面信息
agent-browser get title   # 获取网站标题
agent-browser get url     # 确认当前 URL
```

**输出**：创建输出目录 `{网站名称}_scraped/`

### 阶段二：导航结构分析（关键阶段）

**⚠️ 这是最关键的阶段，必须确保所有嵌套菜单都完全展开！**

```bash
# 1. 获取交互元素快照
agent-browser snapshot -i

# 2. 识别导航元素类型
#    - 侧边栏（sidebar, nav, menu）
#    - 顶部导航（header nav）
#    - Tab 标签（tabs, tablist）
#    - 面包屑（breadcrumb）
#    - 折叠按钮（▸ ▾ + - 箭头图标）
```

#### 🔴 递归展开所有嵌套菜单（核心算法）

```
算法：递归展开菜单
─────────────────────────────────────────
1. 截图并获取 snapshot -i
2. 识别所有"折叠状态"的菜单项：
   - 带有 ▸ ▶ + 箭头的项
   - aria-expanded="false" 的项
   - 有子菜单但未展开的项
3. 如果找到折叠项：
   a. 点击第一个折叠项的展开按钮
   b. 等待 500-1000ms
   c. 重新获取 snapshot -i
   d. 回到步骤 2（递归）
4. 如果没有更多折叠项，进入下一阶段
─────────────────────────────────────────
```

**具体命令序列**：

```bash
# === 第一轮：展开一级菜单 ===
agent-browser snapshot -i
# 输出示例：
# - text: "建站管理" [ref=e10]  ← 可能是折叠状态
#   - img  ← 箭头图标，表示可展开

agent-browser click "建站管理"   # 或 click @e10
agent-browser wait 800
agent-browser snapshot -i

# === 第二轮：展开二级菜单 ===
# 输出示例：
# - text: "建站管理"
#   - text: "橙子建站落地页管理" [ref=e11] ← 可能还有下级
#   - text: "第三方落地页管理" [ref=e12]

agent-browser click "橙子建站落地页管理"
agent-browser wait 800
agent-browser snapshot -i

# === 第三轮：继续展开直到所有叶子节点 ===
# 重复上述过程...

# === 最终确认 ===
# 当 snapshot -i 不再出现新的折叠项时，完成
```

**判断菜单是否需要展开的特征**：

| 特征 | 说明 | 示例 |
|-----|------|------|
| 箭头图标 | ▸ ▶ ► + 表示折叠 | `- img` 在菜单项旁边 |
| 箭头图标 | ▾ ▼ - 表示已展开 | 展开后箭头方向变化 |
| aria-expanded | "false" 表示折叠 | `aria-expanded="false"` |
| 子元素缺失 | 没有子链接显示 | 只有标题没有子项 |
| CSS类名 | collapsed, closed | `class="menu-collapsed"` |

**⚠️ 常见陷阱**：
1. **点击文字 vs 点击箭头**：有些菜单点击文字是导航，点击箭头才是展开
2. **悬停展开**：部分菜单需要 hover 而不是 click
3. **异步加载**：子菜单可能异步加载，需要足够的等待时间

```bash
# 处理"悬停展开"类型的菜单
agent-browser hover "建站管理"
agent-browser wait 1000
agent-browser snapshot -i

# 处理"点击箭头"类型的菜单（坐标定位）
agent-browser click --x 25 --y 510  # 点击菜单项左侧的箭头位置
```

**关键策略**：
- ✅ 识别 `aria-expanded="false"` 的折叠菜单并展开
- ✅ **递归展开所有层级，直到没有更多可展开的项**
- ✅ 提取所有 `<a href>` 链接
- ✅ 建立 URL 队列（广度优先，自动去重）
- ✅ **记录导航层级关系**（用于生成目录结构）

### 阶段三：深度遍历爬取

```bash
# 对队列中每个 URL 执行：

# 1. 访问页面
agent-browser open <page-url>
agent-browser wait --load networkidle

# 2. 提取页面标题
agent-browser get title

# 3. 获取页面内容
agent-browser snapshot    # 获取完整内容树

# 4. 提取文本内容
agent-browser get text @main-content  # 获取主要内容区域

# 5. 处理动态内容（如有）
agent-browser scroll down 1000   # 触发懒加载
agent-browser wait 1000
agent-browser snapshot           # 重新获取

# 6. 发现新链接加入队列
```

**遍历规则**：
- 广度优先遍历
- 同域名链接优先
- 自动过滤已访问 URL
- 记录页面层级关系

### 阶段四：内容结构化

将爬取的内容按原网站目录结构保存：

```
{网站名称}_scraped/
├── README.md                    # 总目录索引 + 爬取报告
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

### 阶段五：完整性校验

```bash
# 1. 统计爬取结果
#    - 总页面数量
#    - 成功/失败比例
#    - 覆盖的板块

# 2. 检查关键内容
#    - 认证授权文档 ✓
#    - API 接口列表 ✓
#    - SDK 下载链接 ✓
#    - 错误码表格 ✓

# 3. 生成爬取报告（写入 README.md）

# 4. 关闭浏览器
agent-browser close
```

---

## agent-browser 命令速查

### 导航命令

| 命令 | 说明 |
|-----|------|
| `open <url>` | 打开页面 |
| `back` / `forward` | 前进/后退 |
| `reload` | 刷新页面 |
| `close` | 关闭浏览器 |

### 快照命令

| 命令 | 说明 |
|-----|------|
| `snapshot` | 完整 DOM 树 |
| `snapshot -i` | 仅交互元素（带 @ref） |
| `snapshot -c` | 紧凑输出 |
| `snapshot -d 3` | 限制深度为 3 |

### 交互命令

| 命令 | 说明 |
|-----|------|
| `click @e1` | 点击元素 |
| `fill @e1 "text"` | 填写输入框 |
| `scroll down 500` | 向下滚动 500px |
| `scrollintoview @e1` | 滚动到元素可见 |
| `hover @e1` | 悬停元素 |

### 获取信息

| 命令 | 说明 |
|-----|------|
| `get text @e1` | 获取元素文本 |
| `get title` | 获取页面标题 |
| `get url` | 获取当前 URL |
| `get value @e1` | 获取输入框值 |

### 等待命令

| 命令 | 说明 |
|-----|------|
| `wait @e1` | 等待元素出现 |
| `wait 2000` | 等待 2 秒 |
| `wait --text "Success"` | 等待文本出现 |
| `wait --load networkidle` | 等待网络空闲 |

### 截图命令

| 命令 | 说明 |
|-----|------|
| `screenshot` | 截图到标准输出 |
| `screenshot path.png` | 保存到文件 |
| `screenshot --full` | 完整页面截图 |

---

## 链接发现策略（6 种方法）

### 1. 侧边栏导航

```bash
agent-browser snapshot -i
# 查找 nav, sidebar, menu 元素
# 提取所有 <a> 链接
```

### 2. 展开折叠菜单

```bash
# 识别折叠状态
agent-browser snapshot -i
# 查找 aria-expanded="false" 或带有展开图标的元素

# 逐个展开
agent-browser click @collapse-toggle
agent-browser wait 500
agent-browser snapshot -i  # 重新获取展开后的链接
```

### 3. Tab 标签页

```bash
# 获取所有 Tab
agent-browser snapshot -i
# 识别 role="tab" 或 tab/tablist 类名

# 遍历每个 Tab
agent-browser click @tab1
agent-browser wait 500
agent-browser get text @tab-content
# 重复...
```

### 4. 分页内容

```bash
# 检测分页器
agent-browser snapshot -i
# 查找 pagination, page-next, 下一页 等元素

# 遍历分页
agent-browser click @next-page
agent-browser wait --load networkidle
# 重复直到 next 按钮 disabled
```

### 5. 无限滚动

```bash
# 记录当前内容数量
# 滚动触发加载
agent-browser scroll down 1000
agent-browser wait 1500
agent-browser snapshot
# 检查是否有新内容
# 重复直到无新内容
```

### 6. 动态路由（SPA）⚠️ 重点

**SPA 网站的核心问题**：URL 改变但页面不刷新，直接访问 URL 可能不加载正确内容。

```bash
# ❌ 错误方式：直接访问 URL
agent-browser open https://example.com/docs/api/user
# 结果：可能显示首页内容，而不是 /api/user 页面

# ✅ 正确方式：通过点击导航切换
agent-browser open https://example.com/docs   # 先打开首页
agent-browser wait 3000                        # 等待 SPA 完全加载
agent-browser click "API 参考"                 # 点击导航
agent-browser wait 2000                        # 等待内容更新
agent-browser click "用户接口"                 # 点击子菜单
agent-browser wait 2000                        # 等待内容更新
agent-browser snapshot                         # 现在获取的是正确内容
```

**SPA 网站爬取策略**：

```
策略：SPA 导航式爬取
─────────────────────────────────────────
1. 只在开始时 open 一次首页 URL
2. 之后所有页面切换都通过 click 导航链接
3. 每次 click 后必须 wait 2000+ ms
4. 通过 get url 确认 URL 已变化
5. 通过 snapshot 获取当前页面内容
6. 如果需要返回上级，用 click 返回导航
   而不是用 back 或重新 open
─────────────────────────────────────────
```

**判断网站是否为 SPA**：
1. 点击链接后 URL 变化但页面没有白屏刷新
2. 页面切换有过渡动画
3. 使用了 React/Vue/Angular 等框架
4. URL 包含 `#` 或使用 History API

**SPA 爬取的完整示例**：

```bash
# 1. 初始化（只执行一次）
agent-browser open https://open.example.com/docs
agent-browser wait 3000

# 2. 展开所有菜单（在同一个页面上操作）
agent-browser click "账号服务"      # 展开一级
agent-browser wait 800
agent-browser click "客户信息管理"   # 展开二级
agent-browser wait 800
agent-browser snapshot -i            # 收集所有链接

# 3. 逐个点击叶子节点获取内容
agent-browser click "获取客户信息"   # 点击具体 API
agent-browser wait 2000
agent-browser get url                # 确认 URL: /docs/api/user/info
agent-browser snapshot               # 获取 API 文档内容
# -> 保存内容到文件

# 4. 返回并访问下一个（不要用 back）
agent-browser click "获取客户列表"   # 直接点击下一个 API
agent-browser wait 2000
agent-browser snapshot
# -> 保存内容到文件

# 5. 如果需要切换到另一个模块
agent-browser click "投放管理"       # 点击另一个一级菜单
agent-browser wait 800
# ... 继续
```

---

## 内容提取方法

### 文本内容

```bash
# 获取整体内容
agent-browser get text @main

# 获取特定区域
agent-browser get text @article
agent-browser get text @content-body
```

### 表格数据

```bash
# 定位表格
agent-browser snapshot -i
# 找到 table 元素

# 提取表格内容
agent-browser get text @table
# 或逐行提取
agent-browser get text @tr1
agent-browser get text @tr2
```

### 代码块

```bash
# 代码块通常在 <pre><code> 中
agent-browser snapshot
# 识别 code, pre, highlight 等元素
agent-browser get text @code-block
```

### API 接口信息

```bash
# API 文档通常包含：
# - 端点 URL
# - HTTP 方法
# - 请求参数表格
# - 响应示例

# 提取策略：
agent-browser snapshot
# 识别 endpoint, method, parameters, response 区块
agent-browser get text @endpoint
agent-browser get text @params-table
agent-browser get text @response-example
```

---

## 动态内容处理指南

### 处理 Cookie 弹窗

```bash
agent-browser open <url>
agent-browser wait 1000
agent-browser snapshot -i
# 查找 cookie-banner, consent, accept 按钮
agent-browser click @accept-cookies
agent-browser wait 500
```

### 处理登录弹窗

```bash
# 检测登录弹窗
agent-browser snapshot -i
# 查找 modal, login-popup, close 按钮
agent-browser click @close-modal
# 或按 ESC 关闭
agent-browser press Escape
```

### 处理懒加载图片

```bash
# 滚动触发图片加载
agent-browser scroll down 500
agent-browser wait 1000
# 重复直到页面底部
```

### 处理 iframe

```bash
# 暂不支持直接操作 iframe 内容
# 可尝试直接访问 iframe src URL
agent-browser snapshot
# 找到 iframe src 属性
agent-browser open <iframe-src>
```

---

## 开放平台专项爬取指南

### 必爬内容清单

| 内容类型 | 关键标识 | 提取方式 |
|---------|---------|---------|
| **认证授权** | OAuth, Token, 密钥, AppID | 完整文本 + 流程图描述 |
| **API 接口** | 端点, 方法, 参数, 响应 | 表格结构化提取 |
| **SDK 下载** | 下载链接, 版本号, 安装命令 | 链接 + 代码块 |
| **示例代码** | `<code>`, `<pre>` 标签 | 保留完整代码格式 |
| **错误码** | 错误码表格 | 表格结构化提取 |
| **更新日志** | Changelog, 版本历史 | 按版本分段提取 |
| **接口限制** | 频率限制, QPS, 配额 | 完整规则说明 |

### API 文档结构化模板

对每个 API 接口，提取并格式化为：

```markdown
## 接口名称

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

## URL 过滤规则

### 白名单（自动包含）

```
/docs/, /doc/, /documentation/
/api/, /api-reference/, /reference/
/guide/, /guides/, /tutorial/, /tutorials/
/sdk/, /download/, /downloads/
/faq/, /help/, /support/
/changelog/, /release-notes/, /updates/
/getting-started/, /quickstart/
/authentication/, /auth/, /oauth/
/error/, /errors/, /error-code/
```

### 黑名单（自动排除）

```
# 用户相关
/login, /register, /signup, /signin
/user/, /account/, /profile/, /settings/
/logout, /forgot-password

# 外部链接
非同域名的所有链接

# 静态资源
.css, .js, .png, .jpg, .jpeg, .gif, .svg, .ico
.woff, .woff2, .ttf, .eot
.pdf, .zip, .tar.gz（记录链接但不访问）

# 重复内容
#section（同页面锚点）
?tab=xxx（同页面 Tab 参数，需特殊处理）

# 社交/分享
/share, /tweet, /weibo
github.com, twitter.com, facebook.com（外链）
```

### 去重策略

```python
# 伪代码
def normalize_url(url):
    # 移除末尾斜杠
    url = url.rstrip('/')
    # 移除锚点
    url = url.split('#')[0]
    # 统一协议
    url = url.replace('http://', 'https://')
    return url

visited = set()
def should_visit(url):
    normalized = normalize_url(url)
    if normalized in visited:
        return False
    visited.add(normalized)
    return True
```

---

## 多文件输出格式规范

### 目录命名规则

```
{序号}_{目录名}/
├── {序号}_{文件名}.md
```

- 序号：两位数字，从 00 开始
- 目录名/文件名：使用原网站导航名称
- 特殊字符替换为下划线

### README.md 模板（总目录）

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
```

### 单页 Markdown 模板

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

## 实战示例：爬取开放平台

### 完整命令序列

```bash
# ===== 阶段一：初始化 =====
agent-browser open https://open.example.com/docs
agent-browser wait --load networkidle
agent-browser wait 2000
agent-browser screenshot homepage.png --full
agent-browser get title
# 输出：Example 开放平台 - 开发文档

# ===== 阶段二：导航分析 =====
agent-browser snapshot -i
# 输出：
# nav "侧边栏" [ref=e1]
#   link "快速入门" [ref=e2]
#   button "API 参考 ▸" [ref=e3] aria-expanded="false"
#   link "SDK 下载" [ref=e4]
#   link "错误码" [ref=e5]

# 展开折叠菜单
agent-browser click @e3
agent-browser wait 500
agent-browser snapshot -i
# 输出新增：
#   link "用户接口" [ref=e6]
#   link "订单接口" [ref=e7]
#   link "支付接口" [ref=e8]

# ===== 阶段三：遍历爬取 =====
# 访问"快速入门"
agent-browser click @e2
agent-browser wait --load networkidle
agent-browser get title
agent-browser get text @main-content
# 保存为：00_快速入门/01_介绍.md

# 访问"用户接口"
agent-browser click @e6
agent-browser wait --load networkidle
agent-browser get text @main-content
# 保存为：01_API参考/01_用户接口.md

# ... 继续遍历所有链接 ...

# ===== 阶段四：内容结构化 =====
# 创建目录结构，保存所有 Markdown 文件

# ===== 阶段五：校验完成 =====
agent-browser close
# 生成 README.md 爬取报告
```

---

## 常见问题处理

### Q: 页面内容加载不完整

```bash
# 增加等待时间
agent-browser wait --load networkidle
agent-browser wait 3000  # 额外等待

# 触发懒加载
agent-browser scroll down 500
agent-browser wait 1000
agent-browser scroll down 500
```

### Q: 侧边栏菜单无法展开

```bash
# 方法1：尝试不同的点击方式
agent-browser click @menu-item          # 使用 ref 定位
agent-browser click "菜单文字"          # 使用文字定位
agent-browser dblclick @menu-item       # 双击
agent-browser hover @menu-item          # 悬停触发

# 方法2：点击展开箭头而非文字
# 先截图确认箭头位置
agent-browser screenshot menu.png
# 计算箭头的坐标位置（通常在菜单项左侧）
agent-browser click --x 30 --y 400      # 使用坐标点击

# 方法3：使用语义定位
agent-browser find text "API 参考" click

# 方法4：检查是否需要先滚动到可见
agent-browser scrollintoview @menu-item
agent-browser wait 500
agent-browser click @menu-item
```

**针对巨量引擎等复杂 SPA 的特殊处理**：

```bash
# 巨量引擎开放平台的菜单是嵌套的折叠结构
# 需要逐层展开，不能跳跃

# 错误：直接点击三级菜单
agent-browser click "获取客户信息"  # ❌ 可能无效

# 正确：逐层展开
agent-browser click "账号服务"           # 1. 先展开一级
agent-browser wait 1000
agent-browser click "客户信息与资质管理"  # 2. 再展开二级
agent-browser wait 1000
agent-browser click "获取客户信息"       # 3. 最后点击目标
agent-browser wait 2000
agent-browser snapshot                   # 4. 获取内容
```

### Q: 遇到需要登录的页面

```bash
# 保存登录状态
agent-browser fill @username "user"
agent-browser fill @password "pass"
agent-browser click @login-btn
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# 后续使用
agent-browser state load auth.json
```

### Q: 链接是相对路径

```bash
# agent-browser 会自动处理相对路径
# 如果需要手动处理，获取当前 URL 后拼接
agent-browser get url
# 输出：https://open.example.com/docs/api
# 相对链接 ./user -> https://open.example.com/docs/api/user
```

### Q: 内容在多个 Tab 中

```bash
# 遍历所有 Tab
agent-browser snapshot -i
# 找到所有 tab 元素

agent-browser click @tab1
agent-browser wait 500
agent-browser get text @tab-content
# 保存内容

agent-browser click @tab2
agent-browser wait 500
agent-browser get text @tab-content
# 保存内容
```

---

## 最佳实践

### 1. 爬取前准备

- [ ] 确认目标网站的 robots.txt 允许爬取
- [ ] 了解网站结构，确定入口 URL
- [ ] 准备输出目录
- [ ] 如需登录，准备账号凭据

### 2. 爬取策略

- **优先广度**：先爬取所有一级导航，再深入
- **及时保存**：每爬完一个页面立即保存，避免丢失
- **控制频率**：页面间适当等待，避免触发反爬
- **断点续爬**：记录已访问 URL，支持中断后继续

### 3. 内容处理

- **保留原格式**：尽量保持原有的标题层级、列表、表格格式
- **代码完整**：代码块完整提取，保留语言标注
- **链接转换**：外部链接保留原 URL，内部链接转为相对路径
- **图片处理**：记录图片 URL，可选择是否下载

### 4. 质量检查

- 检查目录结构是否完整
- 验证关键页面是否都已爬取
- 确认 Markdown 格式正确可读
- 检查链接是否正确指向

### 5. 注意事项

- **尊重 robots.txt**：遵守网站爬取规则
- **适度频率**：避免高频访问对网站造成压力
- **版权意识**：爬取内容仅供个人学习使用
- **敏感信息**：不要爬取或存储个人隐私数据
