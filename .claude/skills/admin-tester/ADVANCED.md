# Admin Tester - 高级功能

本文档涵盖 admin-tester 的高级功能配置和扩展用法。

---

## 目录

1. [权限测试配置](#权限测试配置)
2. [API 测试扩展](#api-测试扩展)
3. [自定义验证规则](#自定义验证规则)
4. [测试数据管理](#测试数据管理)
5. [多环境配置](#多环境配置)
6. [常见问题 Q&A](#常见问题-qa)

---

## 权限测试配置

基于 admin-reverse-docs 输出的权限矩阵，可以配置权限相关的测试用例。

### 权限测试类型

| 类型 | 说明 | 验证方式 |
|-----|------|---------|
| 按钮可见性 | 无权限时按钮不显示 | 检查元素是否存在 |
| 按钮可用性 | 无权限时按钮禁用 | 检查 disabled 属性 |
| 菜单可见性 | 无权限时菜单不显示 | 检查菜单项是否存在 |
| 页面访问 | 无权限时无法访问 | 检查是否跳转到 403 页面 |

### 配置多角色测试

在 `02_测试数据/test-data.yaml` 中配置多角色登录状态：

```yaml
# 文件: 02_测试数据/test-data.yaml

roles:
  admin:
    name: "管理员"
    auth_file: "admin-auth.json"
    permissions:
      - "user:read"
      - "user:write"
      - "user:delete"
      - "order:read"
      - "order:write"
      - "system:config"

  operator:
    name: "操作员"
    auth_file: "operator-auth.json"
    permissions:
      - "user:read"
      - "order:read"
      - "order:write"

  viewer:
    name: "只读用户"
    auth_file: "viewer-auth.json"
    permissions:
      - "user:read"
      - "order:read"
```

### 权限测试用例示例

```yaml
# 文件: 01_测试用例/权限测试/用户管理权限.yaml

module: "用户管理"
test_type: "permission"

cases:
  # === 按钮权限验证 ===
  - id: TC_PERM_USER_001
    name: "用户管理 - 新增按钮权限验证"
    description: "验证不同角色对新增按钮的访问权限"
    priority: P2
    enabled: true
    tags: ["权限", "按钮"]

    role_tests:
      - role: "admin"
        expected:
          button_visible: true
          button_enabled: true

      - role: "operator"
        expected:
          button_visible: false

      - role: "viewer"
        expected:
          button_visible: false

    steps:
      - seq: 1
        action: load_role
        params:
          role: "{{current_role}}"

      - seq: 2
        action: navigate
        params:
          method: "menu"
          path: ["用户管理", "用户列表"]
        wait: 2000

      - seq: 3
        action: verify
        params:
          type: element_visibility
          target: "新增按钮"
          expected: "{{expected.button_visible}}"

      - seq: 4
        action: verify
        condition: "{{expected.button_visible}} == true"
        params:
          type: element_enabled
          target: "新增按钮"
          expected: "{{expected.button_enabled}}"

      - seq: 5
        action: screenshot
        params:
          name: "perm_user_add_{{current_role}}"

  # === 删除按钮权限验证 ===
  - id: TC_PERM_USER_002
    name: "用户管理 - 删除按钮权限验证"
    priority: P2
    enabled: true

    role_tests:
      - role: "admin"
        expected:
          button_visible: true
          button_enabled: true

      - role: "operator"
        expected:
          button_visible: true
          button_enabled: false  # 显示但禁用

      - role: "viewer"
        expected:
          button_visible: false

    steps:
      - seq: 1
        action: load_role
        params:
          role: "{{current_role}}"

      - seq: 2
        action: navigate
        params:
          path: ["用户管理", "用户列表"]
        wait: 2000

      - seq: 3
        action: verify
        params:
          type: element_visibility
          target: "表格第一行:删除"
          expected: "{{expected.button_visible}}"

      - seq: 4
        action: verify
        condition: "{{expected.button_visible}} == true"
        params:
          type: element_enabled
          target: "表格第一行:删除"
          expected: "{{expected.button_enabled}}"

  # === 菜单权限验证 ===
  - id: TC_PERM_MENU_001
    name: "系统设置菜单权限验证"
    description: "验证不同角色对系统设置菜单的访问权限"
    priority: P1
    enabled: true
    tags: ["权限", "菜单"]

    role_tests:
      - role: "admin"
        expected:
          menu_visible: true

      - role: "operator"
        expected:
          menu_visible: false

      - role: "viewer"
        expected:
          menu_visible: false

    steps:
      - seq: 1
        action: load_role
        params:
          role: "{{current_role}}"

      - seq: 2
        action: navigate
        params:
          url: "/"
        wait: 2000

      - seq: 3
        action: snapshot

      - seq: 4
        action: verify
        params:
          type: menu_visibility
          target: "系统设置"
          expected: "{{expected.menu_visible}}"

  # === 页面访问权限验证 ===
  - id: TC_PERM_ACCESS_001
    name: "系统设置页面直接访问权限验证"
    description: "验证无权限用户直接访问页面时的处理"
    priority: P1
    enabled: true
    tags: ["权限", "访问控制"]

    role_tests:
      - role: "admin"
        expected:
          can_access: true

      - role: "operator"
        expected:
          can_access: false
          redirect_to: "/403"

    steps:
      - seq: 1
        action: load_role
        params:
          role: "{{current_role}}"

      - seq: 2
        action: navigate
        params:
          url: "/system/config"
        wait: 2000

      - seq: 3
        action: verify
        params:
          type: access_result
          expected_access: "{{expected.can_access}}"
          expected_redirect: "{{expected.redirect_to}}"
```

### 权限测试执行流程

```
对于每个权限测试用例：
  1. 读取 role_tests 配置
  2. 对于每个角色：
     a. 加载对应的 auth_file
     b. 执行测试步骤
     c. 记录该角色的测试结果
  3. ��总所有角色的测试结果
```

---

## API 测试扩展

结合 admin-reverse-docs 输出的 API 文档，可以扩展 API 级别的测试。

### 启用网络监听

```yaml
# 在测试用例中启用网络监听
- id: TC_API_USER_LIST
  name: "用户列表 - API 响应验证"
  priority: P2
  enabled: true

  config:
    network_monitor: true  # 启用网络监听

  steps:
    - seq: 1
      action: network_start
      description: "开始监听网络请求"

    - seq: 2
      action: navigate
      params:
        path: ["用户管理", "用户列表"]
      wait: 2000

    - seq: 3
      action: network_wait
      description: "等待 API 请求完成"
      params:
        url_pattern: "/api/users"
        timeout: 5000

    - seq: 4
      action: verify
      description: "验证 API 响应"
      params:
        type: api_response
        url_pattern: "/api/users"
        expected:
          status: 200
          body_contains: ["data", "total"]

    - seq: 5
      action: network_stop
```

### API 验证类型

| 类型 | 说明 | 示例 |
|-----|------|------|
| `api_status` | 验证响应状态码 | `expected: 200` |
| `api_body_contains` | 验证响应包含字段 | `expected: ["data", "total"]` |
| `api_body_match` | 验证响应结构 | 使用 JSON Schema |
| `api_timing` | 验证响应时间 | `max_ms: 1000` |
| `api_count` | 验证请求次数 | `expected: 1` |

### API 测试用例示例

```yaml
# 文件: 01_测试用例/API测试/用户接口测试.yaml

test_type: "api"
module: "用户管理"

cases:
  - id: TC_API_USER_001
    name: "用户列表接口 - 正常响应验证"
    priority: P1
    enabled: true
    tags: ["API", "列表"]

    config:
      network_monitor: true

    steps:
      - seq: 1
        action: network_start

      - seq: 2
        action: navigate
        params:
          path: ["用户管理", "用户列表"]
        wait: 3000

      - seq: 3
        action: verify
        params:
          type: api_response
          method: "GET"
          url_pattern: "/api/users"
          expected:
            status: 200
            response_time_max: 2000
            body:
              has_fields: ["code", "data", "message"]
              data_has_fields: ["list", "total", "page", "pageSize"]

      - seq: 4
        action: network_stop

  - id: TC_API_USER_002
    name: "用户搜索接口 - 参数验证"
    priority: P2
    enabled: true

    config:
      network_monitor: true

    steps:
      - seq: 1
        action: network_start

      - seq: 2
        action: navigate
        params:
          path: ["用户管理", "用户列表"]
        wait: 2000

      - seq: 3
        action: fill
        params:
          target: "用户名"
          value: "admin"

      - seq: 4
        action: click
        params:
          target: "搜索"
        wait: 2000

      - seq: 5
        action: verify
        description: "验证搜索接口参数"
        params:
          type: api_request
          method: "GET"
          url_pattern: "/api/users"
          expected:
            params:
              username: "admin"

      - seq: 6
        action: network_stop
```

---

## 自定义验证规则

### 验证规则类型

admin-tester 支持以下验证规则：

| 规则类型 | 说明 | 参数 |
|---------|------|------|
| `element_exists` | 元素存在 | `target` |
| `element_not_exists` | 元素不存在 | `target` |
| `element_visible` | 元素可见 | `target` |
| `element_hidden` | 元素隐藏 | `target` |
| `element_enabled` | 元素可用 | `target` |
| `element_disabled` | 元素禁用 | `target` |
| `element_text` | 元素文本匹配 | `target`, `expected` |
| `element_text_contains` | 元素文本包含 | `target`, `contains` |
| `element_count` | 元素数量 | `target`, `expected` |
| `url_equals` | URL 完全匹配 | `expected` |
| `url_contains` | URL 包含 | `contains` |
| `title_equals` | 标题完全匹配 | `expected` |
| `title_contains` | 标题包含 | `contains` |
| `table_columns` | 表格列匹配 | `expected[]` |
| `table_row_count` | 表格行数 | `min`, `max`, `exact` |
| `form_field_value` | 表单字段值 | `field`, `expected` |
| `validation_error` | 验证错误存在 | `field`, `message` |
| `dialog_visible` | 弹窗可见 | `title` |
| `toast_message` | Toast 消息 | `type`, `message` |

### 自定义复合验证

```yaml
# 复合验证示例
- seq: 5
  action: verify
  description: "复合验证 - 表格和分页"
  params:
    type: composite
    rules:
      - type: table_columns
        expected: ["ID", "用户名", "状态"]
      - type: element_visible
        target: ".pagination"
      - type: table_row_count
        min: 1
        max: 20
    match: "all"  # all | any
```

### 条件验证

```yaml
# 条件验证示例
- seq: 6
  action: verify
  condition: "{{table_has_data}} == true"
  params:
    type: element_visible
    target: "表格第一行:编辑"
```

### 延迟验证

```yaml
# 等待条件满足
- seq: 7
  action: verify
  params:
    type: element_visible
    target: ".success-message"
    wait: true        # 等待条件满足
    timeout: 5000     # 最大等待时间
    interval: 500     # 检查间隔
```

---

## 测试数据管理

### 数据变量

| 变量 | 说明 | 示例输出 |
|-----|------|---------|
| `{{TIMESTAMP}}` | Unix 时间戳 | `1705312200` |
| `{{DATETIME}}` | 日期时间 | `2024-01-15 10:30:00` |
| `{{DATE}}` | 日期 | `2024-01-15` |
| `{{TIME}}` | 时间 | `10:30:00` |
| `{{RANDOM:N}}` | N位随机字符串 | `a1b2c3` |
| `{{RANDOM_NUM:N}}` | N位随机数字 | `123456` |
| `{{UUID}}` | UUID | `550e8400-e29b...` |
| `{{TODAY}}` | 今天日期 | `2024-01-15` |
| `{{TODAY:+N}}` | N天后 | `2024-01-16` |
| `{{TODAY:-N}}` | N天前 | `2024-01-14` |
| `{{ENV:name}}` | 环境变量 | - |

### 数据引用

```yaml
# 在用例中引用测试数据
- id: TC_USER_FORM_001
  test_data_ref: "user.valid_form_data"

  steps:
    - seq: 1
      action: fill_form
      params:
        use_test_data: "user.valid_form_data"
        # 或直接引用单个字段
        # fields:
        #   - name: "用户名"
        #     value: "{{test_data.user.valid_form_data.用户名}}"
```

### 数据清理

```yaml
# 用例定义数据清理步骤
- id: TC_USER_CREATE_001
  cleanup:
    - action: "delete"
      target: "user"
      identifier: "{{created_user_id}}"
    - action: "sql"
      query: "DELETE FROM users WHERE username LIKE 'TEST_%'"
```

### 数据依赖

```yaml
# 用例间数据依赖
- id: TC_ORDER_CREATE_001
  depends_on:
    - TC_USER_CREATE_001  # 依赖用户创建用例

  use_output_from:
    TC_USER_CREATE_001:
      user_id: "{{output.user_id}}"
```

---

## 多环境配置

### 环境配置文件

```yaml
# 文件: 02_测试数据/environments.yaml

environments:
  dev:
    name: "开发环境"
    base_url: "https://dev-admin.example.com"
    auth_file: "dev-auth.json"
    database:
      host: "dev-db.example.com"
      name: "dev_db"

  staging:
    name: "预发布环境"
    base_url: "https://staging-admin.example.com"
    auth_file: "staging-auth.json"
    database:
      host: "staging-db.example.com"
      name: "staging_db"

  prod:
    name: "生产环境"
    base_url: "https://admin.example.com"
    auth_file: "prod-auth.json"
    database:
      host: "prod-db.example.com"
      name: "prod_db"
    # 生产环境禁用写操作测试
    disabled_tags: ["写操作", "删除"]

default_environment: "dev"
```

### 环境切换

在执行测试时指定环境：

```
请在 staging 环境执行测试用例
```

Claude 会：
1. 读取 `environments.yaml` 中的 staging 配置
2. 使用对应的 `base_url` 和 `auth_file`
3. 根据 `disabled_tags` 跳过特定用例

### 环境特定测试数据

```yaml
# 文件: 02_测试数据/test-data.yaml

# 通用数据
common:
  timeout: 30000

# 环境特定数据
env_specific:
  dev:
    user:
      valid_form_data:
        用户名: "dev_test_user"
        邮箱: "dev@test.com"

  staging:
    user:
      valid_form_data:
        用户名: "staging_test_user"
        邮箱: "staging@test.com"
```

---

## 常见问题 Q&A

### Q1: 如何处理动态生成的元素 ID？

**问题**：某些框架生成的元素 ID 是动态的，如 `input_abc123`。

**解决方案**：

1. **使用相对选择器**：
   ```yaml
   target: "用户名输入框"  # 通过 label 关联
   target: "表单:第一个输入框"
   ```

2. **使用属性选择器**：
   ```yaml
   target: "[placeholder='请输入用户名']"
   target: "[name='username']"
   ```

3. **使用层级关系**：
   ```yaml
   target: ".user-form .username-field input"
   ```

---

### Q2: 如何处理异步加载的内容？

**问题**：页面内容通过 AJAX 异步加载，直接验证会失败。

**解决方案**：

1. **使用 wait 参数**：
   ```yaml
   - action: navigate
     params:
       url: "/user/list"
     wait: 3000  # 等待 3 秒
   ```

2. **使用条件等待**：
   ```yaml
   - action: wait_for
     params:
       type: element_visible
       target: ".ant-table-row"
       timeout: 10000
   ```

3. **使用网络空闲等待**：
   ```yaml
   - action: wait
     params:
       type: network_idle
       timeout: 5000
   ```

---

### Q3: 如何处理弹窗和对话框？

**问题**：点击按钮后出现确认弹窗，需要处理。

**解决方案**：

```yaml
# 验证弹窗出现
- action: verify
  params:
    type: dialog_visible
    title: "确认删除"

# 点击弹窗按钮
- action: click
  params:
    target: "dialog:确定"
    # 或
    target: ".ant-modal-confirm-btns .ant-btn-primary"

# 验证弹窗关闭
- action: verify
  params:
    type: dialog_closed
```

---

### Q4: 如何处理文件上传测试？

**问题**：需要测试文件上传功能。

**解决方案**：

```yaml
- id: TC_UPLOAD_001
  name: "文件上传测试"

  test_files:
    - name: "test_image.png"
      path: "02_测试数据/files/test_image.png"

  steps:
    - action: click
      params:
        target: "上传按钮"

    - action: upload
      params:
        target: "input[type='file']"
        file: "{{test_files.test_image.path}}"

    - action: wait
      params:
        timeout: 3000

    - action: verify
      params:
        type: element_visible
        target: ".upload-success"
```

---

### Q5: 如何跳过已知失败的用例？

**问题**：某些用例因为已知 bug 会失败，想暂时跳过。

**解决方案**：

1. **在索引中禁用**：
   ```yaml
   # _index.yaml
   - id: TC_USER_FORM_001
     enabled: false
     skip_reason: "等待 BUG-123 修复"
   ```

2. **使用标签过滤**：
   ```yaml
   # 用例中添加标签
   tags: ["skip-known-bug", "BUG-123"]

   # 执行时排除标签
   # "执行测试，跳过 skip-known-bug 标签的用例"
   ```

---

### Q6: 如何处理验证码？

**问题**：登录或操作需要验证码。

**解决方案**：

1. **测试环境禁用验证码**（推荐）

2. **使用固定测试验证码**：
   ```yaml
   test_captcha:
     image_captcha: "1234"
     sms_captcha: "123456"
   ```

3. **手动介入模式**：
   ```yaml
   - action: pause
     params:
       message: "请手动输入验证码，完成后告知 Claude 继续"
   ```

---

### Q7: 测试执行太慢怎么办？

**问题**：测试用例数量多，执行时间长。

**解决方案**：

1. **优先级执行**：只执行高优先级用例
   ```
   只执行 P0 和 P1 优先级的用例
   ```

2. **标签过滤**：只执行特定标签的用例
   ```
   只执行 "冒烟测试" 标签的用例
   ```

3. **模块过滤**：只执行特定模块的用例
   ```
   只执行 "用户管理" 模块的用例
   ```

4. **调整等待时间**：
   ```yaml
   config:
     default_wait: 1000  # 减少默认等待时间
   ```

---

### Q8: 如何查看测试失败的详细信息？

**解决方案**：

1. **查看报告**：
   ```bash
   cat 03_测试报告/latest-report.md
   ```

2. **查看失败截图**：
   ```bash
   ls 03_测试报告/failures/{用例ID}/
   ```

3. **查看错误详情**：
   ```bash
   cat 03_测试报告/failures/{用例ID}/error.txt
   ```

4. **查看执行日志**：
   ```bash
   # 在报告的"执行日志"部分查看
   ```

---

### Q9: 如何自定义测试报告格式？

**解决方案**：

在配置中指定报告模板：

```yaml
# _index.yaml
config:
  report:
    format: "markdown"  # markdown | html | json
    template: "custom-report-template.md"  # 自定义模板路径
    include_screenshots: true
    include_logs: true
```

---

### Q10: 断点续测后数据状态不一致怎么办？

**问题**：测试中断后恢复，但之前创建的测试数据状态不确定。

**解决方案**：

1. **使用唯一标识**：测试数据使用时间戳或随机后缀
   ```yaml
   用户名: "TEST_{{TIMESTAMP}}_user"
   ```

2. **执行前清理**：
   ```yaml
   setup:
     - action: cleanup
       params:
         pattern: "TEST_%"
   ```

3. **独立测试数据**：每个用例使用独立的测试数据集

4. **手动确认恢复点**：
   ```
   从 TC_ORDER_LIST_001 重新开始执行
   ```
