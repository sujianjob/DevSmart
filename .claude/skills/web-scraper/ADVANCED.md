# Web Scraper - 高级功能指南

本文档包含 Web Scraper 的高级功能和详细配置说明。

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

### 6. 动态路由（SPA）

**SPA 网站的核心问题**：URL 改变但页面不刷新，直接访问 URL 可能不加载正确内容。

```bash
# ❌ 错误方式：直接访问 URL
agent-browser open https://example.com/docs/api/user
# 结果：可能显示首页内容

# ✅ 正确方式：通过点击导航切换
agent-browser open https://example.com/docs   # 先打开首页
agent-browser wait 3000                        # 等待 SPA 完全加载
agent-browser click "API 参考"                 # 点击导航
agent-browser wait 2000
agent-browser click "用户接口"
agent-browser wait 2000
agent-browser snapshot                         # 获取正确内容
```

---

## 动态内容处理

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

### 处理懒加载

```bash
# 滚动触发加载
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
?tab=xxx（同页面 Tab 参数）

# 社交/分享
/share, /tweet, /weibo
github.com, twitter.com, facebook.com（外链）
```

### 去重策略

```python
# 伪代码
def normalize_url(url):
    url = url.rstrip('/')      # 移除末尾斜杠
    url = url.split('#')[0]    # 移除锚点
    url = url.replace('http://', 'https://')  # 统一协议
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

## 开放平台专项指南

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

### 内容提取方法

```bash
# 获取整体内容
agent-browser get text @main

# 获取特定区域
agent-browser get text @article
agent-browser get text @content-body

# 提取表格
agent-browser snapshot -i
agent-browser get text @table

# 提取代码块
agent-browser get text @code-block
```

---

## 可视化模式配置

### 开启可视化模式

```
我要开启可视化模式爬取网站，请：
1. 使用 --headed 参数显示浏览器窗口
2. 每个关键步骤都截图保存
3. 截图命名格式：step_{序号}_{操作描述}.png
```

### 命令变化对比

| 操作 | 普通模式 | 可视化模式 |
|-----|---------|-----------|
| 打开页面 | `agent-browser open <url>` | `agent-browser open <url> --headed` |
| 首页截图 | （跳过） | `agent-browser screenshot step_01_homepage.png --full` |
| 展开菜单 | `agent-browser click "菜单"` | `+ screenshot step_02_expand.png` |
| 页面切换 | `agent-browser click "链接"` | `+ wait 2000` + `screenshot` |

### 截图命名规范

```
step_{序号}_{操作类型}_{描述}.png

示例：
step_01_init_homepage.png
step_02_nav_sidebar.png
step_03_expand_api.png
step_04_page_token.png
step_final_complete.png
```

### 可视化模式用途

1. **调试问题**：观察哪一步出错
2. **验证结果**：确认爬取内容完整
3. **学习结构**：了解 SPA 的导航行为
4. **生成演示**：截图用于文档报告

---

## 模型选择建议

### Opus vs Sonnet 对比

| 特性 | Claude Opus | Claude Sonnet |
|-----|-------------|---------------|
| **复杂导航分析** | ⭐⭐⭐ 最佳 | ⭐⭐ 良好 |
| **SPA 识别准确度** | ⭐⭐⭐ 高 | ⭐⭐ 中等 |
| **递归展开策略** | ⭐⭐⭐ 深度理解 | ⭐⭐ 基本正确 |
| **执行速度** | ⭐ 较慢 | ⭐⭐⭐ 快 |
| **Token 成本** | ⭐ 高 | ⭐⭐⭐ 低 |

### 推荐场景

| 场景 | 推荐模型 | 原因 |
|-----|---------|------|
| 复杂 SPA 网站 | Opus | 需要处理多层嵌套菜单 |
| 简单文档站点 | Sonnet | 结构清晰，速度更快 |
| 首次探测新网站 | Opus | 更好理解网站结构 |
| 批量爬取同类站 | Sonnet | 策略已确定，节省成本 |

### 切换模型

```bash
claude --model opus    # 复杂任务
claude --model sonnet  # 快速任务
```

---

## 常见问题 Q&A

### Q: 页面内容加载不完整

```bash
agent-browser wait --load networkidle
agent-browser wait 3000  # 额外等待
agent-browser scroll down 500
agent-browser wait 1000
```

### Q: 侧边栏菜单无法展开

```bash
# 方法1：不同点击方式
agent-browser click @menu-item
agent-browser click "菜单文字"
agent-browser dblclick @menu-item
agent-browser hover @menu-item

# 方法2：点击展开箭头
agent-browser screenshot menu.png
agent-browser click --x 30 --y 400

# 方法3：先滚动到可见
agent-browser scrollintoview @menu-item
agent-browser wait 500
agent-browser click @menu-item
```

### Q: 复杂 SPA 菜单处理（如巨量引擎）

```bash
# 必须逐层展开，不能跳跃
agent-browser click "账号服务"           # 1. 展开一级
agent-browser wait 1000
agent-browser click "客户信息与资质管理"  # 2. 展开二级
agent-browser wait 1000
agent-browser click "获取客户信息"       # 3. 点击目标
agent-browser wait 2000
agent-browser snapshot
```

### Q: 需要登录的页面

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

### Q: 内容在多个 Tab 中

```bash
agent-browser snapshot -i
agent-browser click @tab1
agent-browser wait 500
agent-browser get text @tab-content
agent-browser click @tab2
agent-browser wait 500
agent-browser get text @tab-content
```

---

## 最佳实践

### 爬取前准备

- [ ] 确认 robots.txt 允许爬取
- [ ] 了解网站结构，确定入口 URL
- [ ] 准备输出目录
- [ ] 如需登录，准备账号凭据

### 爬取策略

- **优先广度**：先爬所有一级导航，再深入
- **及时保存**：每爬完一个页面立即保存
- **控制频率**：页面间适当等待，避免反爬
- **断点续爬**：记录已访问 URL，支持中断继续

### 内容处理

- **保留原格式**：保持标题层级、列表、表格
- **代码完整**：代码块完整提取，保留语言标注
- **链接转换**：外链保留原 URL，内链转相对路径

### 质量检查

- 检查目录结构完整
- 验证关键页面已爬取
- 确认 Markdown 格式正确
- 检查链接指向正确

### 注意事项

- **尊重 robots.txt**：遵守网站规则
- **适度频率**：避免高频访问
- **版权意识**：仅供个人学习
- **敏感信息**：不爬取隐私数据
