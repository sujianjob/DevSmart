# Admin Tester - 输出模板

本文档定义 admin-tester 生成的所有文件模板格式。

---

## 目录

1. [测试用例模板](#测试用例模板)
2. [用例索引模板](#用例索引模板)
3. [测试数据模板](#测试数据模板)
4. [测试报告模板](#测试报告模板)
5. [状态文件模板](#状态文件模板)
6. [README 模板](#readme-模板)

---

## 测试用例模板

### 列表页测试用例

```yaml
# 文件: 01_测试用例/{模块名}/列表页测试.yaml

module: "{模块名}"
page_type: "list"
page_path: "{页面路径}"
generated_at: "{生成时间}"

cases:
  # === 表格结构验证 ===
  - id: TC_{MODULE}_LIST_001
    name: "{模块名}列表 - 表格结构验证"
    description: "验证列表页表格包含所有预期列"
    priority: P1
    enabled: true
    tags: ["结构验证", "列表页"]

    preconditions:
      - "用户已登录"
      - "有查看{模块名}列表的权限"

    steps:
      - seq: 1
        action: navigate
        description: "导航到{模块名}列表页"
        params:
          method: "menu"  # menu | url
          path: ["{一级菜单}", "{二级菜单}"]
          # 或 url: "{页面路径}"
        wait: 2000

      - seq: 2
        action: snapshot
        description: "获取页面元素"

      - seq: 3
        action: verify
        description: "验证表格列是否完整"
        params:
          type: table_columns
          expected:
            - "ID"
            - "名称"
            - "状态"
            - "创建时间"
            - "操作"

      - seq: 4
        action: screenshot
        description: "保存表格结构截图"
        params:
          name: "{module}_list_structure"
          full_page: true

    expected_result: "表格包含所有预期列，布局正确"

  # === 筛选功能验证 ===
  - id: TC_{MODULE}_LIST_002
    name: "{模块名}列表 - 筛选功能验证"
    description: "验证列表页筛选条件是否正常工作"
    priority: P2
    enabled: true
    tags: ["功能验证", "筛选"]

    preconditions:
      - "用户已登录"
      - "列表中有测试数据"

    steps:
      - seq: 1
        action: navigate
        description: "导航到{模块名}列表页"
        params:
          method: "menu"
          path: ["{一级菜单}", "{二级菜单}"]
        wait: 2000

      - seq: 2
        action: snapshot
        description: "获取筛选区域元素"

      - seq: 3
        action: fill
        description: "填写筛选条件"
        params:
          target: "{筛选字段}"
          value: "{测试值}"

      - seq: 4
        action: click
        description: "点击搜索按钮"
        params:
          target: "搜索"
        wait: 1500

      - seq: 5
        action: verify
        description: "验证筛选结果"
        params:
          type: table_not_empty
          # 或更严格的验证
          # type: table_contains
          # expected: "{预期内容}"

      - seq: 6
        action: screenshot
        description: "保存筛选结果截图"
        params:
          name: "{module}_filter_result"

    expected_result: "筛选后表格显示匹配的数据"

  # === 分页功能验证 ===
  - id: TC_{MODULE}_LIST_003
    name: "{模块名}列表 - 分页功能验证"
    description: "验证列表页分页功能是否正常工作"
    priority: P2
    enabled: true
    tags: ["功能验证", "分页"]

    steps:
      - seq: 1
        action: navigate
        params:
          method: "menu"
          path: ["{一级菜单}", "{二级菜单}"]
        wait: 2000

      - seq: 2
        action: verify
        description: "验证分页组件存在"
        params:
          type: element_visible
          target: ".pagination, .ant-pagination, .el-pagination"

      - seq: 3
        action: click
        description: "点击下一页"
        params:
          target: "下一页"
        wait: 1500

      - seq: 4
        action: verify
        description: "验证页码变化"
        params:
          type: page_changed
          expected_page: 2

      - seq: 5
        action: screenshot
        params:
          name: "{module}_pagination"

    expected_result: "分页组件正常工作，页码切换后数据更新"
```

### 表单测试用例

```yaml
# 文件: 01_测试用例/{模块名}/表单测试.yaml

module: "{模块名}"
page_type: "form"
page_path: "{表单路径}"
generated_at: "{生成时间}"

cases:
  # === 必填字段验证 ===
  - id: TC_{MODULE}_FORM_001
    name: "{模块名}表单 - 必填字段验证"
    description: "验证表单必填字段的验证功能"
    priority: P1
    enabled: true
    tags: ["验证规则", "必填字段"]

    preconditions:
      - "用户已登录"
      - "有创建{模块名}的权限"

    steps:
      - seq: 1
        action: navigate
        description: "导航到新增{模块名}页面"
        params:
          method: "click"
          path: ["{一级菜单}", "{二级菜单}", "新增"]
        wait: 2000

      - seq: 2
        action: snapshot
        description: "获取表单元素"

      - seq: 3
        action: click
        description: "直接点击提交按钮"
        params:
          target: "提交, 保存, 确定"
        wait: 1000

      - seq: 4
        action: verify
        description: "验证必填字段错误提示"
        params:
          type: validation_errors
          expected:
            - "{字段1}不能为空"
            - "{字段2}不能为空"

      - seq: 5
        action: screenshot
        params:
          name: "{module}_required_validation"

    expected_result: "显示所有必填字段的验证错误提示"

  # === 格式验证 ===
  - id: TC_{MODULE}_FORM_002
    name: "{模块名}表单 - 格式验证"
    description: "验证表单字段的格式验证功能"
    priority: P2
    enabled: true
    tags: ["验证规则", "格式验证"]

    test_data_ref: "invalid_format_data"

    steps:
      - seq: 1
        action: navigate
        params:
          method: "click"
          path: ["{一级菜单}", "{二级菜单}", "新增"]
        wait: 2000

      - seq: 2
        action: fill_form
        description: "填写格式错误的数据"
        params:
          fields:
            - name: "邮箱"
              value: "invalid-email"
            - name: "手机号"
              value: "123"
            - name: "身份证"
              value: "abc"

      - seq: 3
        action: click
        params:
          target: "提交"
        wait: 1000

      - seq: 4
        action: verify
        params:
          type: validation_errors
          expected:
            - "邮箱格式不正确"
            - "手机号格式不正确"

      - seq: 5
        action: screenshot
        params:
          name: "{module}_format_validation"

    expected_result: "显示格式验证错误提示"

  # === 下拉选项验证 ===
  - id: TC_{MODULE}_FORM_003
    name: "{模块名}表单 - 下拉选项验证"
    description: "验证下拉框选项是否正确"
    priority: P2
    enabled: true
    tags: ["表单元素", "下拉框"]

    steps:
      - seq: 1
        action: navigate
        params:
          method: "click"
          path: ["{一级菜单}", "{二级菜单}", "新增"]
        wait: 2000

      - seq: 2
        action: click
        description: "展开下拉框"
        params:
          target: "{下拉字段}"

      - seq: 3
        action: snapshot
        description: "获取下拉选项"

      - seq: 4
        action: verify
        params:
          type: dropdown_options
          target: "{下拉字段}"
          expected:
            - "选项1"
            - "选项2"
            - "选项3"

      - seq: 5
        action: screenshot
        params:
          name: "{module}_dropdown_options"

    expected_result: "下拉框包含所有预期选项"

  # === 表单提交成功 ===
  - id: TC_{MODULE}_FORM_004
    name: "{模块名}表单 - 提交成功验证"
    description: "验证表单正确填写后可以成功提交"
    priority: P1
    enabled: true
    tags: ["功能验证", "提交"]

    test_data_ref: "valid_form_data"

    steps:
      - seq: 1
        action: navigate
        params:
          method: "click"
          path: ["{一级菜单}", "{二级菜单}", "新增"]
        wait: 2000

      - seq: 2
        action: fill_form
        description: "填写有效表单数据"
        params:
          use_test_data: "valid_form_data"

      - seq: 3
        action: screenshot
        params:
          name: "{module}_form_filled"

      - seq: 4
        action: click
        params:
          target: "提交"
        wait: 2000

      - seq: 5
        action: verify
        params:
          type: success_message
          expected: "保存成功, 创建成功, 添加成功"

      - seq: 6
        action: screenshot
        params:
          name: "{module}_submit_success"

    expected_result: "表单提交成功，显示成功提示"
    cleanup:
      - "删除测试创建的数据"
```

### 导航测试用例

```yaml
# 文件: 01_测试用例/导航测试.yaml

page_type: "navigation"
generated_at: "{生成时间}"

cases:
  # === 一级菜单导航 ===
  - id: TC_NAV_001
    name: "一级菜单导航验证"
    description: "验证所有一级菜单点击后正确导航"
    priority: P0
    enabled: true
    tags: ["导航", "一级菜单"]

    steps:
      - seq: 1
        action: snapshot
        description: "获取菜单元素"

      - seq: 2
        action: click
        description: "点击一级菜单"
        params:
          target: "{一级菜单名}"
        wait: 1500

      - seq: 3
        action: verify
        params:
          type: url
          contains: "{预期URL片段}"

      - seq: 4
        action: verify
        params:
          type: page_title
          contains: "{预期标题}"

      - seq: 5
        action: screenshot
        params:
          name: "nav_{菜单名}"

    expected_result: "点击菜单后正确跳转到目标页面"

  # === 菜单展开/收起 ===
  - id: TC_NAV_002
    name: "菜单展开收起验证"
    description: "验证有子菜单的菜单项展开收起功能"
    priority: P1
    enabled: true
    tags: ["导航", "菜单交互"]

    steps:
      - seq: 1
        action: snapshot

      - seq: 2
        action: verify
        description: "验证子菜单初始为收起状态"
        params:
          type: element_not_visible
          target: "{子菜单项}"

      - seq: 3
        action: click
        description: "点击父菜单展开"
        params:
          target: "{父菜单名}"
        wait: 500

      - seq: 4
        action: verify
        description: "验证子菜单已展开"
        params:
          type: element_visible
          target: "{子菜单项}"

      - seq: 5
        action: click
        description: "再次点击收起"
        params:
          target: "{父菜单名}"
        wait: 500

      - seq: 6
        action: verify
        params:
          type: element_not_visible
          target: "{子菜单项}"

    expected_result: "菜单展开收起功能正常"

  # === 面包屑导航 ===
  - id: TC_NAV_003
    name: "面包屑导航验证"
    description: "验证面包屑导航显示正确且可点击"
    priority: P2
    enabled: true
    tags: ["导航", "面包屑"]

    steps:
      - seq: 1
        action: navigate
        params:
          method: "menu"
          path: ["{一级菜单}", "{二级菜单}", "{三级菜单}"]
        wait: 2000

      - seq: 2
        action: verify
        description: "验证面包屑显示"
        params:
          type: breadcrumb
          expected: ["首页", "{一级菜单}", "{二级菜单}", "{三级菜单}"]

      - seq: 3
        action: click
        description: "点击面包屑中的上级"
        params:
          target: "面包屑:{二级菜单}"
        wait: 1500

      - seq: 4
        action: verify
        params:
          type: url
          contains: "{二级菜单URL}"

    expected_result: "面包屑显示正确，点击可导航"
```

### 操作测试用例

```yaml
# 文件: 01_测试用例/{模块名}/操作测试.yaml

module: "{模块名}"
page_type: "action"
generated_at: "{生成时间}"

cases:
  # === 删除确认验证 ===
  - id: TC_{MODULE}_ACTION_001
    name: "{模块名} - 删除确认弹窗验证"
    description: "验证点击删除按钮后显示确认弹窗"
    priority: P1
    enabled: true
    tags: ["操作", "删除"]

    preconditions:
      - "列表中有可删除的数据"

    steps:
      - seq: 1
        action: navigate
        params:
          method: "menu"
          path: ["{一级菜单}", "{二级菜单}"]
        wait: 2000

      - seq: 2
        action: snapshot

      - seq: 3
        action: click
        description: "点击第一行的删除按钮"
        params:
          target: "表格第一行:删除"
        wait: 500

      - seq: 4
        action: verify
        description: "验证确认弹窗出现"
        params:
          type: dialog
          expected: "确认删除, 确定要删除, 删除后不可恢复"

      - seq: 5
        action: screenshot
        params:
          name: "{module}_delete_confirm"

      - seq: 6
        action: click
        description: "点击取消关闭弹窗"
        params:
          target: "取消"
        wait: 500

      - seq: 7
        action: verify
        description: "验证弹窗关闭"
        params:
          type: dialog_closed

    expected_result: "点击删除显示确认弹窗，点击取消关闭弹窗"

  # === 批量操作验证 ===
  - id: TC_{MODULE}_ACTION_002
    name: "{模块名} - 批量操作验证"
    description: "验证批量选择和批量操作功能"
    priority: P2
    enabled: true
    tags: ["操作", "批量"]

    steps:
      - seq: 1
        action: navigate
        params:
          method: "menu"
          path: ["{一级菜单}", "{二级菜单}"]
        wait: 2000

      - seq: 2
        action: click
        description: "勾选全选框"
        params:
          target: "全选框"

      - seq: 3
        action: verify
        description: "验证批量操作按钮出现"
        params:
          type: element_visible
          target: "批量删除, 批量导出"

      - seq: 4
        action: screenshot
        params:
          name: "{module}_batch_select"

    expected_result: "全选后显示批量操作按钮"

  # === 编辑操作验证 ===
  - id: TC_{MODULE}_ACTION_003
    name: "{模块名} - 编辑操作验证"
    description: "验证点击编辑按钮后进入编辑页面"
    priority: P1
    enabled: true
    tags: ["操作", "编辑"]

    steps:
      - seq: 1
        action: navigate
        params:
          method: "menu"
          path: ["{一级菜单}", "{二级菜单}"]
        wait: 2000

      - seq: 2
        action: click
        description: "点击第一行的编辑按钮"
        params:
          target: "表格第一行:编辑"
        wait: 2000

      - seq: 3
        action: verify
        description: "验证进入编辑页面"
        params:
          type: url
          contains: "edit, modify, update"

      - seq: 4
        action: verify
        description: "验证表单已填充数据"
        params:
          type: form_has_values

      - seq: 5
        action: screenshot
        params:
          name: "{module}_edit_page"

    expected_result: "点击编辑后进入编辑页面，表单已填充数据"
```

---

## 用例索引模板

```yaml
# 文件: 01_测试用例/_index.yaml

version: "1.0"
generated_at: "{生成时间}"
source: "{系统名}_admin_docs"

# === 执行配置 ===
config:
  base_url: "https://admin.example.com"
  auth_file: "admin-auth.json"
  screenshot_on_failure: true
  screenshot_on_success: false
  timeout: 30000  # 单步超时（毫秒）
  retry_on_failure: 1  # 失败重试次数

# === 统计摘要 ===
summary:
  total: 58
  enabled: 45
  disabled: 13
  by_priority:
    P0: 5
    P1: 20
    P2: 25
    P3: 8
  by_type:
    list: 15
    form: 23
    navigation: 8
    action: 12

# === 模块与用例列表 ===
modules:
  - name: "用户管理"
    path: "/user"
    cases:
      - id: TC_USER_LIST_001
        name: "用户列表 - 表格结构验证"
        file: "用户管理/列表页测试.yaml"
        priority: P1
        enabled: true  # ← 用户可修改

      - id: TC_USER_LIST_002
        name: "用户列表 - 筛选功能验证"
        file: "用户管理/列表页测试.yaml"
        priority: P2
        enabled: true

      - id: TC_USER_FORM_001
        name: "用户表单 - 必填字段验证"
        file: "用户管理/表单测试.yaml"
        priority: P1
        enabled: true

      - id: TC_USER_FORM_002
        name: "用户表单 - 格式验证"
        file: "用户管理/表单测试.yaml"
        priority: P2
        enabled: false  # 暂时禁用

  - name: "订单管理"
    path: "/order"
    cases:
      - id: TC_ORDER_LIST_001
        name: "订单列表 - 表格结构验证"
        file: "订单管理/列表页测试.yaml"
        priority: P1
        enabled: true

  - name: "导航"
    path: "/"
    cases:
      - id: TC_NAV_001
        name: "一级菜单导航验证"
        file: "导航测试.yaml"
        priority: P0
        enabled: true

# === 执行顺序 ===
# 按优先级排序的执行顺序（自动生成）
execution_order:
  - TC_NAV_001        # P0
  - TC_USER_LIST_001  # P1
  - TC_USER_FORM_001  # P1
  - TC_ORDER_LIST_001 # P1
  - TC_USER_LIST_002  # P2
```

---

## 测试数据模板

```yaml
# 文件: 02_测试数据/test-data.yaml

version: "1.0"
description: "测试数据配置文件，可根据实际情况修改"

# === 全局配置 ===
globals:
  timestamp: "{{TIMESTAMP}}"      # 动态时间戳
  random_suffix: "{{RANDOM:6}}"   # 6位随机字符串
  test_prefix: "TEST_"            # 测试数据前缀

# === 用户模块测试数据 ===
user:
  # 有效表单数据（用于提交成功测试）
  valid_form_data:
    用户名: "{{test_prefix}}user_{{random_suffix}}"
    邮箱: "test_{{random_suffix}}@example.com"
    手机号: "13800138000"
    密码: "Test@123456"
    确认密码: "Test@123456"
    状态: "启用"
    角色: "普通用户"

  # 格式错误数据（用于验证测试）
  invalid_format_data:
    邮箱: "invalid-email"
    手机号: "123"
    身份证: "abc123"

  # 筛选测试数据
  filter_data:
    用户名: "admin"
    状态: "启用"

# === 订单模块测试数据 ===
order:
  valid_form_data:
    订单号: "{{test_prefix}}{{timestamp}}"
    客户名称: "测试客户"
    商品名称: "测试商品"
    数量: 1
    单价: 100.00

  filter_data:
    订单状态: "待处理"
    开始日期: "2024-01-01"
    结束日期: "2024-12-31"

# === 通用测试数据 ===
common:
  # 边界值测试
  boundary:
    empty_string: ""
    long_string: "{{REPEAT:a:1000}}"  # 1000个a
    special_chars: "<script>alert('xss')</script>"
    sql_injection: "'; DROP TABLE users; --"

  # 日期数据
  dates:
    today: "{{TODAY}}"
    yesterday: "{{TODAY:-1}}"
    tomorrow: "{{TODAY:+1}}"
    last_month: "{{TODAY:-30}}"

# === 数据变量说明 ===
# {{TIMESTAMP}} - 当前时间戳
# {{RANDOM:N}} - N位随机字符串
# {{TODAY}} - 今天日期 (YYYY-MM-DD)
# {{TODAY:+N}} - N天后
# {{TODAY:-N}} - N天前
# {{REPEAT:char:N}} - 重复字符N次
```

---

## 测试报告模板

### 执行报告模板

```markdown
<!-- 文件: 03_测试报告/latest-report.md -->

# 测试执行报告

> 生成时间: {生成时间}
> 测试套件: {系统名}_test_suite

---

## 执行概览

| 指标 | 数值 |
|-----|------|
| 执行开始 | {开始时间} |
| 执行结束 | {结束时间} |
| 执行耗时 | {总耗时} |
| 总用例数 | {总数} |
| 执行数 | {执行数} |
| 通过数 | {通过数} ✅ |
| 失败数 | {失败数} ❌ |
| 跳过数 | {跳过数} ⏭️ |
| **通过率** | **{通过率}%** |

### 结果分布

```
通过 ████████████████████░░░░ 80%
失败 ████░░░░░░░░░░░░░░░░░░░░ 15%
跳过 █░░░░░░░░░░░░░░░░░░░░░░░ 5%
```

---

## 按模块统计

| 模块 | 总数 | 通过 | 失败 | 跳过 | 通过率 |
|-----|------|------|------|------|--------|
| 用户管理 | 12 | 10 | 1 | 1 | 83.3% |
| 订单管理 | 18 | 16 | 2 | 0 | 88.9% |
| 系统设置 | 15 | 12 | 2 | 1 | 80.0% |
| 导航 | 8 | 8 | 0 | 0 | 100% |

---

## 按优先级统计

| 优先级 | 总数 | 通过 | 失败 | 通过率 |
|-------|------|------|------|--------|
| P0 | 5 | 5 | 0 | 100% |
| P1 | 20 | 18 | 2 | 90% |
| P2 | 25 | 20 | 5 | 80% |
| P3 | 8 | 6 | 2 | 75% |

---

## 失败用例详情

### ❌ TC_USER_FORM_001 - 用户表单必填字段验证

| 属性 | 值 |
|-----|-----|
| 模块 | 用户管理 |
| 优先级 | P1 |
| 执行时间 | {执行时间} |
| 失败步骤 | Step 4 - 验证必填字段错误提示 |

**失败原因**：

```
预期: 显示 "用户名不能为空" 错误提示
实际: 未找到错误提示元素
选择器: .ant-form-item-explain-error, .el-form-item__error
```

**失败截图**：

![失败截图](./failures/TC_USER_FORM_001/screenshot.png)

**建议**：
- 检查表单验证是否正确绑定
- 确认错误提示的 CSS 选择器

---

### ❌ TC_ORDER_LIST_002 - 订单列表筛选功能验证

| 属性 | 值 |
|-----|-----|
| 模块 | 订单管理 |
| 优先级 | P2 |
| 执行时间 | {执行时间} |
| 失败步骤 | Step 5 - 验证筛选结果 |

**失败原因**：

```
预期: 筛选后表格数据更新
实际: 表格数据未变化，可能是筛选接口无响应
```

---

## 通过用例列表

<details>
<summary>点击展开通过用例列表（{通过数} 条）</summary>

| 用例ID | 名称 | 模块 | 耗时 |
|-------|------|------|------|
| TC_NAV_001 | 一级菜单导航验证 | 导航 | 2.3s |
| TC_USER_LIST_001 | 用户列表表格结构验证 | 用户管理 | 3.1s |
| TC_USER_LIST_002 | 用户列表筛选功能验证 | 用户管理 | 4.2s |
| ... | ... | ... | ... |

</details>

---

## 执行日志

<details>
<summary>点击展开详细执行日志</summary>

```
[10:30:00] 开始执行测试套件
[10:30:01] 加载浏览器状态: admin-auth.json
[10:30:02] 打开后台首页: https://admin.example.com
[10:30:05] ▶ 开始执行: TC_NAV_001 - 一级菜单导航验证
[10:30:07] ✅ TC_NAV_001 通过 (2.3s)
[10:30:08] ▶ 开始执行: TC_USER_LIST_001 - 用户列表表格结构验证
[10:30:11] ✅ TC_USER_LIST_001 通过 (3.1s)
[10:30:12] ▶ 开始执行: TC_USER_FORM_001 - 用户表单必填字段验证
[10:30:16] ❌ TC_USER_FORM_001 失败 - Step 4: 未找到错误提示元素
[10:30:16]    保存截图: failures/TC_USER_FORM_001/screenshot.png
...
[11:15:00] 测试执行完成
```

</details>

---

## 附件

- [覆盖率分析报告](./coverage.md)
- [失败用例截图目录](./failures/)
- [完整截图目录](../_assets/screenshots/)
```

### 覆盖率报告模板

```markdown
<!-- 文件: 03_测试报告/coverage.md -->

# 测试覆盖率分析

> 基于 {系统名}_admin_docs 分析

---

## 整体覆盖率

| 维度 | 已覆盖 | 总数 | 覆盖率 |
|-----|-------|------|--------|
| 模块 | 8 | 10 | 80% |
| 页面 | 25 | 32 | 78% |
| 功能点 | 58 | 75 | 77% |

---

## 模块覆盖详情

### 用户管理 ✅ 已覆盖

| 页面 | 测试用例数 | 状态 |
|-----|-----------|------|
| 用户列表 | 3 | ✅ |
| 用户详情 | 4 | ✅ |
| 角色管理 | 2 | ✅ |
| 权限配置 | 0 | ⚠️ 未覆盖 |

### 订单管理 ✅ 已覆盖

| 页面 | 测试用例数 | 状态 |
|-----|-----------|------|
| 订单列表 | 3 | ✅ |
| 订单详情 | 4 | ✅ |
| 退款管理 | 2 | ✅ |

### 报表中心 ⚠️ 部分覆盖

| 页面 | 测试用例数 | 状态 |
|-----|-----------|------|
| 销售报表 | 1 | ✅ |
| 用户报表 | 0 | ⚠️ 未覆盖 |
| 数据导出 | 0 | ⚠️ 未覆盖 |

### 系统设置 ❌ 未覆盖

建议添加测试用例。

---

## 功能点覆盖

### 已覆盖功能

- ✅ 列表页表格结构验证
- ✅ 列表页筛选功能
- ✅ 列表页分页功能
- ✅ 表单必填验证
- ✅ 表单格式验证
- ✅ 菜单导航
- ✅ 删除确认

### 未覆盖功能

- ⚠️ 批量导入
- ⚠️ 数据导出
- ⚠️ 图表展示
- ⚠️ 权限控制

---

## 建议

1. **优先添加**：系统设置模块的基础测试用例
2. **补充覆盖**：报表中心的数据导出功能
3. **增强验证**：权限相关的测试场景
```

---

## 状态文件模板

```json
// 文件: .test-state.json

{
  "version": "1.0",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:15:00Z",

  "source": {
    "docs_dir": "{系统名}_admin_docs",
    "auth_file": "admin-auth.json",
    "entry_url": "https://admin.example.com"
  },

  "config": {
    "screenshot_on_failure": true,
    "screenshot_on_success": false,
    "timeout": 30000,
    "retry_on_failure": 1
  },

  "progress": {
    "phase": "execute",
    "started_at": "2024-01-15T10:30:00Z",
    "total_cases": 58,
    "executed": 45,
    "passed": 42,
    "failed": 3,
    "skipped": 13
  },

  "current_case": {
    "id": "TC_ORDER_FORM_002",
    "name": "订单表单 - 格式验证",
    "step": 3,
    "status": "running",
    "started_at": "2024-01-15T11:14:30Z"
  },

  "results": [
    {
      "id": "TC_NAV_001",
      "name": "一级菜单导航验证",
      "status": "passed",
      "duration": 2300,
      "timestamp": "2024-01-15T10:30:05Z"
    },
    {
      "id": "TC_USER_LIST_001",
      "name": "用户列表表格结构验证",
      "status": "passed",
      "duration": 3100,
      "timestamp": "2024-01-15T10:30:11Z"
    },
    {
      "id": "TC_USER_FORM_001",
      "name": "用户表单必填字段验证",
      "status": "failed",
      "duration": 4200,
      "timestamp": "2024-01-15T10:30:16Z",
      "error": {
        "step": 4,
        "message": "未找到错误提示元素",
        "selector": ".ant-form-item-explain-error",
        "screenshot": "failures/TC_USER_FORM_001/screenshot.png"
      }
    }
  ],

  "screenshots": [
    {
      "case_id": "TC_NAV_001",
      "step": 5,
      "path": "_assets/screenshots/nav_用户管理.png",
      "timestamp": "2024-01-15T10:30:04Z"
    }
  ]
}
```

---

## README 模板

```markdown
<!-- 文件: README.md -->

# {系统名} 测试套件

> 基于 admin-reverse-docs 生成的 UI 功能测试套件

---

## 快速开始

### 1. 环境准备

```bash
# 确保 admin-reverse-docs 输出存在
ls {系统名}_admin_docs/

# 确保登录状态文件存在
ls admin-auth.json
```

### 2. 审核测试用例

```bash
# 查看用例索引
cat 01_测试用例/_index.yaml

# 修改启用/禁用状态
# 编辑 _index.yaml 中的 enabled 字段

# 修改测试数据
# 编辑 02_测试数据/test-data.yaml
```

### 3. 执行测试

```bash
# 告知 Claude 开始执行测试
# Claude 会加载浏览器状态并按优先级执行用例
```

### 4. 查看报告

```bash
# 查看最新执行报告
cat 03_测试报告/latest-report.md

# 查看覆盖率分析
cat 03_测试报告/coverage.md

# 查看失败详情
ls 03_测试报告/failures/
```

---

## 目录结构

```
{系统名}_test_suite/
├── README.md                    # 本文件
├── .test-state.json             # 执行状态
│
├── 01_测试用例/
│   ├── _index.yaml              # 用例索引
│   ├── 导航测试.yaml
│   └── {模块名}/
│       ├── 列表页测试.yaml
│       ├── 表单测试.yaml
│       └── 操作测试.yaml
│
├── 02_测试数据/
│   └── test-data.yaml           # 测试数据配置
│
├── 03_测试报告/
│   ├── latest-report.md         # 最新报告
│   ├── coverage.md              # 覆盖率
│   └── failures/                # 失败详情
│
└── _assets/
    └── screenshots/             # 截图
```

---

## 测试用例统计

| 类型 | 数量 |
|-----|------|
| 列表页测试 | {数量} |
| 表单测试 | {数量} |
| 导航测试 | {数量} |
| 操作测试 | {数量} |
| **总计** | **{总数}** |

---

## 配置说明

### 用例启用/禁用

编辑 `01_测试用例/_index.yaml`：

```yaml
cases:
  - id: TC_USER_FORM_001
    enabled: false  # 设为 false 禁用此用例
```

### 测试数据修改

编辑 `02_测试数据/test-data.yaml`：

```yaml
user:
  valid_form_data:
    用户名: "自定义用户名"
    邮箱: "custom@example.com"
```

---

## 断点续测

如果测试中断，下次执行时会检测 `.test-state.json` 并询问是否继续。

---

## 注意事项

1. 执行前确保登录状态有效
2. 部分测试可能创建测试数据，建议在测试环境执行
3. 失败用例请查看截图和错误信息分析原因
```
