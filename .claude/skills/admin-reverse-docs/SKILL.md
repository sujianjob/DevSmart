---
name: admin-reverse-docs
description: 读取后台管理系统、提取功能列表并反向生成系统文档的智能工具。支持自动登录状态管理、菜单递归展开、界面元素提取、API 监听分析，输出完整的系统文档。
---

# Admin Reverse Docs - 后台管理系统反向文档生成工具

基于 `agent-browser` 的智能分析工具，专门针对后台管理系统进行功能提取和文档反向生成。

---

## 快速开始

```bash
# 1. 手动登录并保存状态
agent-browser open https://admin.example.com/login
# 用户手动完成登录...
agent-browser state save admin-auth.json

# 2. 后续启动时加载状态
agent-browser state load admin-auth.json
agent-browser open https://admin.example.com/dashboard

# 3. 分析导航结构
agent-browser snapshot -i

# 4. 按工作流执行分析
```

### 完整示例

```bash
agent-browser state load admin-auth.json
agent-browser open https://admin.example.com
agent-browser wait --load networkidle
agent-browser snapshot -i
# 递归展开菜单 -> 遍历所有模块 -> 提取界面元素 -> 生成文档
agent-browser close
```

---

## 核心概念

### 输入

- **后台 URL**：目标后台管理系统地址
- **登录状态**：已保存的浏览器认证状态文件

### 输出

1. **原样记录**：按后台原有结构记录的功能清单
2. **智能分析**：反向推导的数据模型、API 文档、业务分析

---

## 登录状态管理

### 首次登录

```bash
# 1. 打开登录页面
agent-browser open https://admin.example.com/login

# 2. 提示用户手动登录
# （用户在浏览器中完成登录操作）

# 3. 确认登录成功后保存状态
agent-browser wait --url "**/dashboard"  # 等待跳转到后台首页
agent-browser state save admin-auth.json
```

### 加载已保存状态

```bash
agent-browser state load admin-auth.json
agent-browser open https://admin.example.com/dashboard
agent-browser wait 2000

# 验证登录状态是否有效
agent-browser snapshot -i
# 检查是否显示用户信息或后台内容
```

### 状态失效处理

```
⚠️ 检测到登录状态失效！
   页面跳转到登录页或显示"请登录"

处理方式：
1. 请在浏览器中重新登录
2. 登录成功后执行: agent-browser state save admin-auth.json
3. 然后继续执行分析流程
```

---

## 核心工作流（6 阶段）

### 阶段一：系统识别与登录

```bash
# 加载登录状态
agent-browser state load admin-auth.json

# 打开后台首页
agent-browser open https://admin.example.com
agent-browser wait --load networkidle
agent-browser wait 2000

# 验证登录状态
agent-browser snapshot -i
agent-browser screenshot homepage.png --full
agent-browser get title
```

**输出**：创建目录 `{系统名}_admin_docs/`

**验证点**：
- 检查是否显示用户头像/用户名
- 检查是否有管理菜单/侧边栏
- 如显示登录页，提示用户重新登录

### 阶段二：导航结构分析

**目标**：提取完整的菜单树结构

```bash
agent-browser snapshot -i
# 识别侧边栏 sidebar, nav-menu, ant-menu, el-menu 等
# 识别顶部导航栏
```

#### 递归展开菜单算法

```
1. 截图并获取 snapshot -i
2. 识别所有"折叠状态"的菜单项：
   - 带有 ▸ ▶ + 箭头的项
   - aria-expanded="false" 的项
   - 带有 submenu-collapsed 类名的项
3. 如果找到折叠项：
   a. 点击第一个折叠项的展开按钮
   b. 等待 500-1000ms
   c. 重新获取 snapshot -i
   d. 回到步骤 2（递归）
4. 如果没有更多折叠项，记录完整菜单树
```

**具体命令**：

```bash
# === 展开一级菜单 ===
agent-browser snapshot -i
agent-browser click "用户管理"
agent-browser wait 800
agent-browser snapshot -i

# === 展开二级菜单 ===
agent-browser click "用户列表"
agent-browser wait 800
agent-browser snapshot -i

# === 继续直到所有叶子节点 ===
```

**输出**：`01_原始记录/导航结构.md`

### 阶段三：功能模块遍历

**遍历策略**：广度优先，按菜单层级逐级遍历

```bash
# 对队列中每个模块执行：
agent-browser click "目标菜单项"
agent-browser wait 2000
agent-browser get title
agent-browser get url
agent-browser screenshot {模块名}.png --full
agent-browser snapshot -i
# 识别页面类型 -> 提取对应元素
```

#### 页面类型识别

| 类型 | 特征 | 提取内容 |
|-----|------|---------|
| **列表页** | 有表格/Table、分页器 | 表头、列定义、筛选条件、操作按钮 |
| **详情页** | 有表单/Form、详情描述 | 字段名、字段类型、验证规则 |
| **Dashboard** | 有统计卡片、图表 | 指标名称、图表类型 |
| **设置页** | 有配置项、开关 | 配置项名称、选项 |

### 阶段四：界面元素提取

#### 表格分析

```bash
agent-browser snapshot -i
# 查找 table, .ant-table, .el-table 元素

# 提取表头
agent-browser get text @table-header
# 提取操作列按钮
agent-browser get text @action-column
```

**提取内容**：

| 元素 | 提取信息 |
|-----|---------|
| 表头 | 列名、列宽、是否可排序 |
| 数据行 | 数据类型推断 |
| 操作列 | 按钮名称、权限标识 |
| 分页 | 每页条数、总数 |
| 筛选 | 筛选字段、类型 |

#### 表单分析

```bash
agent-browser snapshot -i
# 查找 form, .ant-form, .el-form 元素

# 提取表单字段
agent-browser get text @form-labels
```

**提取内容**：

| 元素 | 提取信息 |
|-----|---------|
| 字段标签 | 字段名称、是否必填 |
| 输入控件 | 类型（文本/数字/日期/选择器） |
| 验证提示 | 验证规则描述 |
| 下拉选项 | 枚举值列表 |

#### 按钮与权限

```bash
agent-browser snapshot -i
# 查找所有按钮元素
# 识别 disabled 状态（可能表示权限不足）
```

**提取内容**：

| 元素 | 提取信息 |
|-----|---------|
| 操作按钮 | 名称、位置、触发动作 |
| 禁用按钮 | 可能的权限要求 |
| 批量操作 | 支持的批量功能 |

### 阶段五：API 端点发现

**启用网络监听**：

```bash
# 开始监听网络请求
agent-browser network start

# 执行页面操作触发 API 调用
agent-browser click "搜索"
agent-browser wait 2000

# 获取捕获的请求
agent-browser network list
```

**分析内容**：

| 请求属性 | 分析目标 |
|---------|---------|
| URL 路径 | API 端点命名规律 |
| 请求方法 | RESTful 风格识别 |
| 请求参数 | 参数名称和类型 |
| 响应结构 | 数据模型推断 |
| 状态码 | 错误处理方式 |

**输出**：`03_API文档/` 目录

### 阶段六：文档生成

#### 生成原样记录

```
01_原始记录/
├── 导航结构.md      # 完整菜单树
├── 模块列表.md      # 扁平化模块清单
└── {模块名}/
    ├── 概述.md      # 模块基本信息
    ├── 列表页.md    # 表格结构记录
    ├── 详情页.md    # 表单字段记录
    └── screenshots/ # 界面截图
```

#### 生成智能分析

```
02_数据模型/
├── 实体关系.md      # 从表格/表单推导的实体
├── 字段字典.md      # 所有字段汇总
└── 数据流向.md      # 数据关联分析

03_API文档/
├── README.md        # API 概览
├── 接口列表.md      # 所有端点清单
└── {模块名}_api.md  # 按模块分组的详情

04_业务分析/
├── 业务流程.md      # 主要业务流程
├── 权限矩阵.md      # CRUD 权限映射
└── 系统架构.md      # 推断的系统架构
```

---

## 状态管理（断点续爬）

### 状态文件

分析过程会自动生成 `.reverse-state.json`：

```json
{
  "version": "1.0",
  "system": {
    "name": "XX 管理后台",
    "entry_url": "https://admin.example.com",
    "auth_file": "admin-auth.json"
  },
  "progress": {
    "phase": "crawl",
    "started_at": "2024-01-15T10:30:00Z",
    "total_modules": 25,
    "completed": 12,
    "failed": 1,
    "pending": 12
  },
  "navigation_tree": {
    "用户管理": {
      "expanded": true,
      "children": ["用户列表", "角色管理", "权限配置"]
    }
  },
  "module_queue": [
    {"path": "/user/list", "status": "completed", "type": "list"},
    {"path": "/user/detail", "status": "pending", "type": "detail"}
  ],
  "api_endpoints": [
    {"method": "GET", "path": "/api/users", "module": "用户管理"}
  ]
}
```

### 恢复逻辑

1. 检测输出目录是否存在 `.reverse-state.json`
2. 提示用户是否继续上次任务
3. 加载保存的认证状态
4. 从 `module_queue` 中找到第一个 `pending` 项继续

---

## 进度显示

```
📊 分析进度: [████████░░░░░░░░] 12/25 (48%)
   ├─ 当前模块: 用户管理 > 用户列表
   ├─ 已发现 API: 8 个
   └─ 状态: ✓ 12 | ✗ 1 | ○ 12

✅ 完成模块: 用户管理 (3/3 页)
⏳ 下一模块: 订单管理
```

---

## 界面框架识别

### 常见后台框架

| 框架 | 识别特征 | 特殊处理 |
|-----|---------|---------|
| **Ant Design Pro** | `.ant-*` 类名、ProTable | 标准表格/表单提取 |
| **Element UI** | `.el-*` 类名 | Vue 组件结构 |
| **Arco Design** | `.arco-*` 类名 | 字节系组件 |
| **iView/View UI** | `.ivu-*` 类名 | 菜单展开方式特殊 |
| **LayUI** | `.layui-*` 类名 | 传统多页应用 |
| **Bootstrap Admin** | `.navbar`, `.sidebar` | 响应式布局 |

### 框架检测命令

```bash
agent-browser snapshot -i
# 分析返回的 HTML 结构识别框架
# 根据类名前缀判断：ant-, el-, arco-, ivu-, layui-
```

---

## 命令速查

### 登录状态

| 命令 | 说明 |
|-----|------|
| `state save <file>` | 保存当前浏览器状态 |
| `state load <file>` | 加载已保存状态 |

### 导航

| 命令 | 说明 |
|-----|------|
| `open <url>` | 打开页面 |
| `click "菜单项"` | 点击菜单导航 |
| `back` / `forward` | 前进/后退 |

### 元素获取

| 命令 | 说明 |
|-----|------|
| `snapshot -i` | 获取交互元素（带 @ref） |
| `get text @ref` | 获取元素文本 |
| `get title` | 获取页面标题 |
| `get url` | 获取当前 URL |

### 网络监听

| 命令 | 说明 |
|-----|------|
| `network start` | 开始监听网络请求 |
| `network list` | 列出捕获的请求 |
| `network stop` | 停止监听 |

### 截图

| 命令 | 说明 |
|-----|------|
| `screenshot path.png` | 保存截图 |
| `screenshot --full` | 完整页面截图 |

---

## 更多资源

- **高级功能**：[ADVANCED.md](./ADVANCED.md)
  - API 深度分析
  - 权限矩阵生成
  - 数据模型推导
  - 业务流程分析
  - 常见问题 Q&A

- **输出模板**：[TEMPLATES.md](./TEMPLATES.md)
  - README 总目录模板
  - 模块文档模板
  - API 文档模板
  - 状态文件格式

- **预设配置**：[presets/](./presets/)
  - 预设使用说明
  - 通用后台管理系统预设
