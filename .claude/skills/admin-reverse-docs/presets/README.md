# Admin Reverse Docs - 预设配置

预设是针对特定类型后台系统优化的配置模板，包含菜单选择器、页面类型识别规则等。

---

## 可用预设

| 预设文件 | 适用场景 | 说明 |
|---------|---------|------|
| `generic-admin.yaml` | 通用后台管理系统 | 默认预设，兼容大多数后台 |

---

## 预设使用方式

### 自动检测（暂不支持）

由于后台系统通常不对外开放，URL 无法通过域名匹配自动检测预设。

### 手动指定

```
用户指令: "使用 generic-admin 预设分析后台"
```

---

## 预设文件格式

```yaml
# 预设元信息
name: preset-name
description: 预设描述
version: "1.0"

# 框架识别
framework_detection:
  selectors:
    - ".ant-layout"           # Ant Design
    - ".el-container"         # Element UI
    - ".arco-layout"          # Arco Design
  class_prefix:
    - "ant-"
    - "el-"
    - "arco-"

# 导航配置
navigation:
  # 侧边栏选择器
  sidebar:
    selectors:
      - ".ant-layout-sider"
      - ".el-aside"
      - "[class*='sidebar']"

  # 菜单选择器
  menu:
    selectors:
      - ".ant-menu"
      - ".el-menu"
      - "[class*='menu']"

  # 菜单项选择器
  menu_item:
    selectors:
      - ".ant-menu-item"
      - ".el-menu-item"
      - "[class*='menu-item']"

  # 子菜单/折叠菜单选择器
  submenu:
    selectors:
      - ".ant-menu-submenu"
      - ".el-submenu"
      - "[class*='submenu']"
    collapsed_indicators:
      - "[aria-expanded='false']"
      - ".ant-menu-submenu-closed"
    expanded_indicators:
      - "[aria-expanded='true']"
      - ".ant-menu-submenu-open"

# 页面元素配置
elements:
  # 表格
  table:
    selectors:
      - ".ant-table"
      - ".el-table"
      - "table"
    header_selectors:
      - ".ant-table-thead"
      - ".el-table__header"
      - "thead"
    body_selectors:
      - ".ant-table-tbody"
      - ".el-table__body"
      - "tbody"

  # 表单
  form:
    selectors:
      - ".ant-form"
      - ".el-form"
      - "form"
    item_selectors:
      - ".ant-form-item"
      - ".el-form-item"
    label_selectors:
      - ".ant-form-item-label"
      - ".el-form-item__label"
      - "label"

  # 分页
  pagination:
    selectors:
      - ".ant-pagination"
      - ".el-pagination"
      - "[class*='pagination']"

  # 按钮
  button:
    selectors:
      - ".ant-btn"
      - ".el-button"
      - "button"
    primary_indicators:
      - ".ant-btn-primary"
      - ".el-button--primary"
    danger_indicators:
      - ".ant-btn-danger"
      - ".el-button--danger"

# 页面类型识别
page_types:
  list:
    indicators:
      - "table"
      - "[class*='table']"
      - "[class*='list']"

  detail:
    indicators:
      - "[class*='detail']"
      - "[class*='descriptions']"

  form:
    indicators:
      - "form"
      - "[class*='form']"

  dashboard:
    indicators:
      - "[class*='dashboard']"
      - "[class*='statistic']"
      - "[class*='chart']"

# 登录检测
auth:
  login_indicators:
    - "[class*='login']"
    - "input[type='password']"
    - "[placeholder*='密码']"

  logged_in_indicators:
    - "[class*='avatar']"
    - "[class*='user-info']"
    - "[class*='dropdown']"

# URL 规则
url_rules:
  # 忽略的 URL 模式
  ignore_patterns:
    - "/login"
    - "/register"
    - "/forgot-password"
    - "/403"
    - "/404"
    - "/500"
```

---

## 扩展预设

如需为特定后台系统创建专用预设：

1. 复制 `generic-admin.yaml` 为新文件
2. 修改预设名称和描述
3. 根据目标系统调整选择器
4. 测试验证预设效果

### 示例：为 Ant Design Pro 创建预设

```yaml
name: antd-pro
description: Ant Design Pro 后台模板专用预设
version: "1.0"

framework_detection:
  selectors:
    - ".ant-pro-layout"
    - ".ant-pro-sider-menu"

navigation:
  sidebar:
    selectors:
      - ".ant-pro-sider"
  menu:
    selectors:
      - ".ant-pro-sider-menu"
  # ... 其他配置
```

---

## 预设贡献指南

欢迎为常见后台框架贡献预设配置：

1. 使用真实后台系统测试选择器
2. 确保兼容该框架的多个版本
3. 提供完整的页面元素配置
4. 在 PR 中说明测试覆盖范围
