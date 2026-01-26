# Admin Tester 预设配置

预设配置用于快速启动测试用例生成，无需手动配置每个参数。

---

## 使用方式

```
使用 generic-test 预设为 XX系统_admin_docs 生成测试用例
```

Claude 会：
1. 加载预设配置
2. 与 admin-reverse-docs 输出合并
3. 生成测试用例

---

## 可用预设

| 预设 | 说明 | 适用场景 |
|-----|------|---------|
| [generic-test.yaml](./generic-test.yaml) | 通用测试配置 | 大多数后台管理系统 |

---

## 预设结构

```yaml
# 预设元信息
preset:
  name: "预设名称"
  description: "预设说明"
  version: "1.0"

# 测试配置
config:
  # 执行配置
  execution:
    timeout: 30000
    retry_on_failure: 1
    screenshot_on_failure: true

  # 优先级配置
  priority:
    default: P2
    navigation: P0
    list_structure: P1
    form_validation: P1

# 测试用例���成规则
rules:
  # 列表页规则
  list_page:
    enabled: true
    tests:
      - structure_verify
      - filter_verify
      - pagination_verify

  # 表单规则
  form_page:
    enabled: true
    tests:
      - required_verify
      - format_verify
      - dropdown_verify
      - submit_verify

  # 导航规则
  navigation:
    enabled: true
    tests:
      - menu_click
      - breadcrumb

  # 操作规则
  actions:
    enabled: true
    tests:
      - delete_confirm
      - edit_navigate
      - batch_select

# 验证规则
validations:
  # 表格验证
  table:
    check_columns: true
    check_pagination: true
    check_empty_state: true

  # 表单验证
  form:
    check_required: true
    check_format: true
    check_dropdown: true

# 排除规则
exclusions:
  # 排除的页面类型
  page_types: []

  # 排除的模块（正则）
  modules: []

  # 排除的 URL（正则）
  urls: []
```

---

## 自定义预设

可以基于现有预设创建自定义配置：

1. 复制 `generic-test.yaml` 为 `my-preset.yaml`
2. 修改配置项
3. 使用自定义预设：

```
使用 my-preset 预设生成测试用例
```

---

## 预设参数说明

### execution 执行配置

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|--------|------|
| timeout | number | 30000 | 单步超时时间（毫秒） |
| retry_on_failure | number | 1 | 失败重试次数 |
| screenshot_on_failure | boolean | true | 失败时截图 |
| screenshot_on_success | boolean | false | 成功时截图 |
| default_wait | number | 2000 | 默认等待时间（毫秒） |

### priority 优先级配置

| 参数 | 类型 | 默认值 | 说明 |
|-----|------|--------|------|
| default | string | P2 | 默认优先级 |
| navigation | string | P0 | 导航测试优先级 |
| list_structure | string | P1 | 列表结构验证优先级 |
| form_validation | string | P1 | 表单验证优先级 |
| form_submit | string | P1 | 表单提交优先级 |
| action_delete | string | P2 | 删除操作优先级 |
| action_edit | string | P2 | 编辑操作优先级 |

### rules 测试规则

每种页面类型可配置生成的测试类型：

**list_page 列表页**：
- `structure_verify`: 表格结构验证
- `filter_verify`: 筛选功能验证
- `pagination_verify`: 分页功能验证
- `sort_verify`: 排序功能验证
- `empty_state_verify`: 空状态验证

**form_page 表单页**：
- `required_verify`: 必填字段验证
- `format_verify`: 格式验证
- `dropdown_verify`: 下拉选项验证
- `submit_verify`: 提交成功验证
- `reset_verify`: 重置功能验证

**navigation 导航**：
- `menu_click`: 菜单点击导航
- `menu_expand`: 菜单展开收起
- `breadcrumb`: 面包屑导航

**actions 操作**：
- `delete_confirm`: 删除确认弹窗
- `edit_navigate`: 编辑页面跳转
- `batch_select`: 批量选择操作
- `export`: 导出功能

### exclusions 排除规则

可以排除特定内容不生成测试用例：

```yaml
exclusions:
  # 排除 Dashboard 类型页面
  page_types:
    - "dashboard"

  # 排除特定模块
  modules:
    - "^日志.*"      # 排除以"日志"开头的模块
    - ".*测试$"      # 排除以"测试"结尾的模块

  # 排除特定 URL
  urls:
    - "/debug/.*"
    - "/internal/.*"
```
