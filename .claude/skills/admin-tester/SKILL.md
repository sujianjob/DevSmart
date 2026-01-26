---
name: admin-tester
description: 基于 admin-reverse-docs 输出的 UI 功能测试工具。解析反向文档生成测试用例，支持人工审核后执行，输出完整测试报告。
---

# Admin Tester - 后台管理系统 UI 测试工具

基于 `admin-reverse-docs` 输出的智能测试工具，自动生成测试用例并执行 UI 功能测试。

---

## 快速开始

```bash
# 1. 确保已有 admin-reverse-docs 输出
ls {系统名}_admin_docs/

# 2. 加载浏览器登录状态
agent-browser state load admin-auth.json

# 3. 生成测试用例
# Claude 解析文档并生成 → {系统名}_test_suite/01_测试用例/

# 4. 用户审核测试用例
# 编辑 _index.yaml 启用/禁用用例

# 5. 执行测试
agent-browser open https://admin.example.com
# 按优先级执行选中的用例

# 6. 查看测试报告
cat {系统名}_test_suite/03_测试报告/latest-report.md
```

### 完整示例

```bash
# 加载登录状态
agent-browser state load admin-auth.json

# 打开后台首页
agent-browser open https://admin.example.com
agent-browser wait --load networkidle

# 执行测试用例（以用户列表为例）
agent-browser click "用户管理"
agent-browser wait 1000
agent-browser click "用户列表"
agent-browser wait 2000
agent-browser snapshot -i

# 验证表格结构
# 检查表头是否包含预期列
agent-browser screenshot user_list_verify.png

agent-browser close
```

---

## 核心概念

### 输入

- **admin-reverse-docs 输出目录**：包含导航结构、模块列表、页面结构等文档
- **登录状态文件**：已保存的浏览器认证状态

### 输出

1. **测试用例**：基于文档生成的 YAML 格式用例
2. **测试报告**：执行结果汇总、覆盖率分析、失败详情

---

## 核心工作流（5 阶段）

### 阶段一：加载与解析

```bash
# 1. 确认 admin-reverse-docs 输出目录存在
ls {系统名}_admin_docs/

# 2. 读取并解析关键文档
cat {系统名}_admin_docs/01_原始记录/导航结构.md
cat {系统名}_admin_docs/01_原始记录/模块列表.md

# 3. 解析各模块详情
ls {系统名}_admin_docs/01_原始记录/{模块名}/
cat {系统名}_admin_docs/01_原始记录/{模块名}/列表页.md
cat {系统名}_admin_docs/01_原始记录/{模块名}/详情页.md
```

**解析内容**：

| 文档 | 提取内容 |
|-----|---------|
| 导航结构.md | 菜单层级、模块路径 |
| 模块列表.md | 所有模块清单 |
| 列表页.md | 表格结构、筛选条件、操作按钮 |
| 详情页.md | 表单字段、验证规则、枚举值 |
| 权限矩阵.md | CRUD 权限映射（可选） |

**输出**：创建目录 `{系统名}_test_suite/`

### 阶段二：测试用例生成

根据解析结果，生成四类测试用例：

#### 1. 列表页测试

```yaml
- id: TC_{模块}_LIST_001
  name: "表格结构验证"
  module: "{模块名}"
  page: "{页面路径}"
  priority: P1
  enabled: true

  steps:
    - action: navigate
      target: "{页面路径}"
      wait: 2000

    - action: verify
      type: table_columns
      expected: ["列1", "列2", "列3", ...]

    - action: screenshot
      name: "{模块}_list_structure"

  expected_result: "表格包含所有预期列"
```

#### 2. 表单测试

```yaml
- id: TC_{模块}_FORM_001
  name: "必填字段验证"
  module: "{模块名}"
  page: "{表单路径}"
  priority: P1
  enabled: true

  steps:
    - action: navigate
      target: "{表单路径}"
      wait: 2000

    - action: click
      target: "提交按钮"

    - action: verify
      type: validation_errors
      expected: ["字段1不能为空", "字段2不能为空", ...]

    - action: screenshot
      name: "{模块}_form_validation"

  expected_result: "显示必填字段验证错误"
```

#### 3. 导航测试

```yaml
- id: TC_NAV_001
  name: "菜单导航验证"
  priority: P0
  enabled: true

  steps:
    - action: click
      target: "{菜单项}"
      wait: 1000

    - action: verify
      type: url
      expected: "{预期URL}"

    - action: verify
      type: page_title
      expected: "{预期标题}"

    - action: screenshot
      name: "nav_{菜单项}"

  expected_result: "菜单点击后正确跳转到目标页面"
```

#### 4. 操作测试

```yaml
- id: TC_{模块}_ACTION_001
  name: "删除操作确认"
  module: "{模块名}"
  priority: P2
  enabled: true

  steps:
    - action: navigate
      target: "{列表页路径}"
      wait: 2000

    - action: click
      target: "删除按钮"

    - action: verify
      type: dialog
      expected: "确认删除"

    - action: screenshot
      name: "{模块}_delete_confirm"

  expected_result: "点击删除后显示确认弹窗"
```

**输出**：`{系统名}_test_suite/01_测试用例/` 目录

### 阶段三：用例审核（人工）

```
📋 测试用例生成完成！

生成统计：
├─ 列表页测试: 15 条
├─ 表单测试: 23 条
├─ 导航测试: 8 条
└─ 操作测试: 12 条

请审核测试用例：
1. 查看用例：cat {系统名}_test_suite/01_测试用例/_index.yaml
2. 修改启用状态：设置 enabled: true/false
3. 调整测试数据：编辑 02_测试数据/test-data.yaml
4. 确认后告知 Claude 开始执行
```

**用例索引文件** `_index.yaml`：

```yaml
version: "1.0"
generated_at: "2024-01-15T10:30:00Z"
source: "{系统名}_admin_docs"

summary:
  total: 58
  enabled: 58
  disabled: 0

modules:
  - name: "用户管理"
    cases:
      - id: TC_USER_LIST_001
        name: "用户列表 - 表格结构验证"
        priority: P1
        enabled: true  # ← 用户可修改
      - id: TC_USER_FORM_001
        name: "用户表单 - 必填字段验证"
        priority: P1
        enabled: true
```

### 阶段四：执行测试

```bash
# 1. 加载浏览器状态
agent-browser state load admin-auth.json

# 2. 打开后台首页
agent-browser open https://admin.example.com
agent-browser wait --load networkidle

# 3. 按优先级执行用例（P0 → P1 → P2 → P3）
# 每个用例执行流程：
```

#### 执行流程

```
对于每个启用的用例：
  1. 更新状态为 "running"
  2. 执行用例中的每个步骤：
     - navigate: agent-browser open/click
     - click: agent-browser click @ref
     - fill: agent-browser fill @ref "value"
     - verify: 检查断言条件
     - screenshot: agent-browser screenshot
  3. 记录执行结果（pass/fail/skip）
  4. 如果失败，保存错误信息和截图
  5. 更新进度状态
```

#### 进度显示

```
🧪 测试执行中: [████████░░░░░░░░] 12/25 (48%)
   ├─ 当前用例: TC_USER_LIST_001 - 用户列表表格结构验证
   ├─ 优先级: P1
   └─ 状态: ✓ 10 | ✗ 1 | ○ 14

✅ 通过: TC_USER_LIST_001
❌ 失败: TC_USER_FORM_001 - 必填验证未触发
⏭️ 跳过: TC_PERMISSION_001 - 用例已禁用
```

### 阶段五：报告生成

执行完成后生成测试报告：

```markdown
# 测试执行报告

## 执行概览

| 指标 | 数值 |
|-----|------|
| 执行时间 | 2024-01-15 10:30:00 - 11:15:00 |
| 总用例数 | 58 |
| 执行数 | 45 |
| 通过数 | 42 |
| 失败数 | 3 |
| 跳过数 | 13 |
| 通过率 | 93.3% |

## 覆盖率分析

| 模块 | 用例数 | 覆盖率 |
|-----|-------|--------|
| 用户管理 | 12/15 | 80% |
| 订单管理 | 18/20 | 90% |
| 系统设置 | 15/23 | 65% |

## 失败用例详情

### TC_USER_FORM_001 - 必填字段验证

- **模块**: 用户管理
- **优先级**: P1
- **失败原因**: 提交后未显示验证错误信息
- **截图**: [查看](./failures/TC_USER_FORM_001/screenshot.png)

```
预期: 显示 "用户名不能为空" 错误
实际: 未找到错误提示元素
```
```

**输出**：`{系统名}_test_suite/03_测试报告/` 目录

---

## 测试类型详解

### UI 功能测试（核心）

| 测试类型 | 测试内容 | 数据来源 |
|---------|---------|---------|
| **列表页** | 表格结构验证、筛选功能、分页、排序 | 列表页.md |
| **表单页** | 必填字段、格式验证、下拉选项、提交 | 详情页.md |
| **导航** | 菜单展开、页面跳转、面包屑 | 导航结构.md |
| **操作** | 按钮点击、弹窗交互、删除确认 | 列表页.md 操作列 |

### 验证类型

| 类型 | 说明 | 示例 |
|-----|------|------|
| `table_columns` | 验证表格列是否存在 | `expected: ["ID", "用户名"]` |
| `form_fields` | 验证表单字段是否存在 | `expected: ["用户名", "邮箱"]` |
| `validation_errors` | 验证错误提示是否显示 | `expected: ["不能为空"]` |
| `url` | 验证当前 URL | `expected: "/user/list"` |
| `page_title` | 验证页面标题 | `expected: "用户列表"` |
| `element_visible` | 验证元素是否可见 | `target: "新增按钮"` |
| `element_text` | 验证元素文本内容 | `target: @ref, expected: "保存"` |
| `dialog` | 验证弹窗是否出现 | `expected: "确认删除"` |

---

## 状态管理（断点续测）

### 状态文件

测试过程会自动生成 `.test-state.json`：

```json
{
  "version": "1.0",
  "source": {
    "docs_dir": "{系统名}_admin_docs",
    "auth_file": "admin-auth.json",
    "entry_url": "https://admin.example.com"
  },
  "progress": {
    "phase": "execute",
    "started_at": "2024-01-15T10:30:00Z",
    "total_cases": 58,
    "executed": 12,
    "passed": 10,
    "failed": 1,
    "skipped": 1
  },
  "current_case": {
    "id": "TC_USER_FORM_001",
    "step": 2,
    "status": "running"
  },
  "results": [
    {
      "id": "TC_USER_LIST_001",
      "status": "passed",
      "duration": 5200,
      "timestamp": "2024-01-15T10:32:00Z"
    }
  ]
}
```

### 恢复逻辑

1. 检测测试套件目录是否存在 `.test-state.json`
2. 提示用户是否继续上次测试
3. 加载保存的浏览器状态
4. 从 `current_case` 继续执行

---

## 输出目录结构

```
{系统名}_test_suite/
├── README.md                    # 测试套件概览 + 执行说明
├── .test-state.json             # 执行状态（断点续测）
│
├── 01_测试用例/
│   ├── _index.yaml              # 用例索引（用户可编辑启用/禁用）
│   └── {模块名}/
│       ├── 列表页测试.yaml      # 列表页测试用例
│       ├── 表单测试.yaml        # 表单测试用例
│       └── 导航测试.yaml        # 导航测试用例
│
├── 02_测试数据/
│   └── test-data.yaml           # 测试数据配置（用户可编辑）
│
├── 03_测试报告/
│   ├── latest-report.md         # 最新执行报告
│   ├── coverage.md              # 覆盖率分析
│   └── failures/
│       └── {用例ID}/
│           ├── error.txt        # 错误信息
│           └── screenshot.png   # 失败截图
│
└── _assets/
    └── screenshots/             # 执行过程截图
```

---

## 命令速查

### 浏览器操作

| 命令 | 说明 |
|-----|------|
| `state load <file>` | 加载登录状态 |
| `open <url>` | 打开页面 |
| `click @ref` | 点击元素 |
| `fill @ref "text"` | 填充输入框 |
| `snapshot -i` | 获取交互元素 |
| `screenshot <path>` | 保存截图 |

### 断言检查

| 动作 | 说明 |
|-----|------|
| 检查元素存在 | `snapshot -i` 后查找目标元素 |
| 检查文本内容 | `get text @ref` 获取并比对 |
| 检查 URL | `get url` 获取并比对 |
| 检查页面标题 | `get title` 获取并比对 |

---

## 更多资源

- **高级功能**：[ADVANCED.md](./ADVANCED.md)
  - 权限测试配置
  - API 测试扩展
  - 自定义验证规则
  - 测试数据管理
  - 常见问题 Q&A

- **输出模板**：[TEMPLATES.md](./TEMPLATES.md)
  - 测试用例模板
  - 测试报告模板
  - 状态文件格式
  - 测试数据格式

- **预设配置**：[presets/](./presets/)
  - 预设使用说明
  - 通用测试配置
