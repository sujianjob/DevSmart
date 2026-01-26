# Admin Reverse Docs - 高级功能指南

本文档包含 Admin Reverse Docs 的高级功能和详细配置说明。

---

## API 深度分析

### 网络请求监听

在分析后台系统时，启用网络监听可以捕获所有 API 调用：

```bash
# 开始监听（在执行操作前）
agent-browser network start

# 执行触发 API 的操作
agent-browser click "搜索"
agent-browser wait 2000

# 查看捕获的请求
agent-browser network list

# 停止监听
agent-browser network stop
```

### API 请求分析维度

| 分析维度 | 提取信息 | 用途 |
|---------|---------|------|
| **URL 模式** | `/api/v1/users`, `/api/v1/orders` | 识别 RESTful 资源命名 |
| **HTTP 方法** | GET/POST/PUT/DELETE | 确定 CRUD 操作类型 |
| **请求参数** | Query/Body 参数 | 了解接口入参 |
| **请求头** | Authorization, Content-Type | 认证方式识别 |
| **响应结构** | JSON 字段、嵌套层级 | 数据模型推断 |
| **状态码** | 200/400/401/403/500 | 错误处理模式 |

### API 分类策略

```
根据 URL 路径自动分类：

/api/users/*      → 用户管理模块
/api/orders/*     → 订单管理模块
/api/products/*   → 商品管理模块
/api/auth/*       → 认证授权模块
/api/config/*     → 系统配置模块
/api/stats/*      → 统计报表模块
```

### RESTful 风格识别

| 请求模式 | 含义 | 示例 |
|---------|------|------|
| `GET /resource` | 列表查询 | `GET /api/users` |
| `GET /resource/:id` | 单个查询 | `GET /api/users/123` |
| `POST /resource` | 新建 | `POST /api/users` |
| `PUT /resource/:id` | 更新 | `PUT /api/users/123` |
| `DELETE /resource/:id` | 删除 | `DELETE /api/users/123` |
| `POST /resource/:id/action` | 特殊操作 | `POST /api/users/123/disable` |

---

## 权限矩阵生成

### 权限识别方法

#### 1. 按钮状态分析

```bash
agent-browser snapshot -i
# 检查按钮的 disabled 属性
# 记录可点击 vs 不可点击的按钮
```

**权限推断规则**：

| 按钮状态 | 权限推断 |
|---------|---------|
| 可见可点击 | 当前用户有权限 |
| 可见但禁用 | 权限受限或条件不满足 |
| 不可见 | 无查看权限 |

#### 2. 菜单可见性分析

```bash
# 展开所有菜单后
agent-browser snapshot -i
# 记录所有可见菜单项
# 与完整菜单列表对比（如有预设）
```

#### 3. API 响应分析

```
监听 API 响应中的权限字段：
- permissions: ["read", "write", "delete"]
- role: "admin"
- can_edit: true
```

### 权限矩阵模板

```markdown
## 权限矩阵

| 模块 | 查看 | 新增 | 编辑 | 删除 | 特殊操作 |
|-----|------|------|------|------|---------|
| 用户管理 | ✓ | ✓ | ✓ | ✗ | 禁用用户 |
| 订单管理 | ✓ | ✗ | ✓ | ✗ | 取消订单 |
| 系统设置 | ✓ | - | ✓ | - | - |

图例：✓ 有权限 | ✗ 无权限 | - 不适用
```

---

## 数据模型推导

### 从表格推导实体

```bash
agent-browser snapshot -i
# 提取表格列名
```

**推导规则**：

| 表格列 | 推导字段类型 |
|-------|------------|
| ID、编号 | `string/number`, 主键 |
| 名称、标题 | `string` |
| 创建时间、更新时间 | `datetime` |
| 状态 | `enum` |
| 金额、价格 | `decimal` |
| 是否xxx | `boolean` |
| 头像、图片 | `url/file` |

### 从表单推导实体

```bash
agent-browser click "新增"
agent-browser wait 2000
agent-browser snapshot -i
# 提取表单字段
```

**推导规则**：

| 表单控件 | 推导字段类型 |
|---------|------------|
| Input | `string` |
| InputNumber | `number` |
| Select | `enum` |
| DatePicker | `date/datetime` |
| Switch | `boolean` |
| Upload | `file` |
| Cascader | `tree/relation` |

### 实体关系推导

```
关系识别模式：

1. 外键关系
   - 表单中的"选择xxx"下拉框
   - 列表中的"关联xxx"列

2. 一对多关系
   - 详情页中的子表格
   - Tab 页签中的关联数据

3. 多对多关系
   - 多选标签
   - 权限分配等场景
```

### 实体关系图生成

```markdown
## 实体关系图

\`\`\`
┌─────────────┐     ┌─────────────┐
│    User     │     │    Order    │
├─────────────┤     ├─────────────┤
│ id          │◄────│ user_id     │
│ name        │     │ id          │
│ email       │     │ total       │
│ status      │     │ status      │
│ created_at  │     │ created_at  │
└─────────────┘     └─────────────┘
        │                  │
        │                  │
        ▼                  ▼
┌─────────────┐     ┌─────────────┐
│    Role     │     │ OrderItem   │
├─────────────┤     ├─────────────┤
│ id          │     │ order_id    │
│ name        │     │ product_id  │
│ permissions │     │ quantity    │
└─────────────┘     └─────────────┘
\`\`\`
```

---

## 业务流程分析

### 流程识别方法

#### 1. 状态字段追踪

```
订单状态流转：
待支付 → 已支付 → 待发货 → 已发货 → 已完成
              ↘ 已取消 ←↙
```

#### 2. 操作按钮分析

```
根据不同状态下可用的操作按钮推断流程：

状态=待支付 → 可用按钮：[取消, 支付]
状态=已支付 → 可用按钮：[发货, 退款]
状态=待发货 → 可用按钮：[发货, 退款]
```

#### 3. 操作日志分析

```bash
# 如果系统有操作日志功能
agent-browser click "操作日志"
agent-browser wait 2000
agent-browser snapshot
# 分析日志中的操作类型和顺序
```

### 流程图生成

```markdown
## 业务流程：订单处理

\`\`\`
[用户下单] → [待支付]
              ↓
         用户支付
              ↓
          [已支付]
         ╱        ╲
    商家发货    申请退款
        ↓          ↓
    [已发货]    [退款中]
        ↓          ↓
    用户确认    退款完成
        ↓          ↓
    [已完成]    [已退款]
\`\`\`
```

---

## 系统架构推断

### 技术栈识别

```bash
agent-browser snapshot
# 分析 HTML 结构识别前端框架

# 常见识别特征：
# Vue + Element UI: el-*, v-if, :data
# React + Ant Design: ant-*, className, data-*
# Angular: ng-*, [ngIf], (click)
```

### 架构特征推断

| 观察点 | 推断内容 |
|-------|---------|
| API URL 结构 | 后端框架风格 |
| 认证头格式 | JWT/Session/OAuth |
| 分页参数 | 后端分页实现 |
| 文件上传方式 | OSS/本地存储 |
| 实时更新 | WebSocket/轮询 |

---

## 多账号权限对比

### 对比分析流程

```bash
# 1. 使用管理员账号分析
agent-browser state load admin-auth.json
# ... 执行完整分析 ...
# 保存结果到 admin_analysis/

# 2. 使用普通用户账号分析
agent-browser state load user-auth.json
# ... 执行完整分析 ...
# 保存结果到 user_analysis/

# 3. 对比两个结果
# - 可见菜单差异
# - 可用按钮差异
# - API 权限差异
```

### 差异报告模板

```markdown
## 权限差异分析

### 菜单可见性差异

| 菜单项 | 管理员 | 普通用户 |
|-------|--------|---------|
| 用户管理 | ✓ | ✗ |
| 订单管理 | ✓ | ✓ |
| 系统设置 | ✓ | ✗ |

### 操作权限差异

| 模块 | 操作 | 管理员 | 普通用户 |
|-----|------|--------|---------|
| 订单管理 | 删除订单 | ✓ | ✗ |
| 订单管理 | 编辑订单 | ✓ | ✓ |
```

---

## 增量更新分析

### 增量分析模式

```bash
# 首次完整分析
# ... 生成完整文档 ...

# 后续增量更新
# 1. 加载上次状态
# 2. 只分析有变化的模块
# 3. 合并更新文档
```

### 变化检测

| 检测项 | 方法 |
|-------|------|
| 菜单变化 | 对比菜单树结构 |
| 字段变化 | 对比表格列/表单字段 |
| API 变化 | 对比接口列表 |

---

## 常见问题 Q&A

### Q: 登录状态频繁失效怎么办？

```
可能原因：
1. Session 超时时间短
2. Token 过期
3. 单点登录限制

解决方案：
1. 调整分析频率，减少等待时间
2. 在每个主要阶段开始前检查登录状态
3. 设置自动检测并提示重新登录
```

### Q: 菜单展开后又自动收起？

```bash
# 部分系统菜单有自动收起逻辑
# 解决方案：快速操作

agent-browser click "一级菜单"
agent-browser wait 300  # 减少等待时间
agent-browser click "二级菜单"
agent-browser wait 300
agent-browser click "目标页面"
```

### Q: 如何处理弹窗/Modal？

```bash
# 检测弹窗
agent-browser snapshot -i
# 查找 modal, dialog, drawer 元素

# 弹窗内操作
agent-browser get text @modal-content
agent-browser screenshot modal.png

# 关闭弹窗
agent-browser click @close-button
# 或
agent-browser press Escape
```

### Q: 表格数据量大如何处理？

```bash
# 只提取表头结构，不获取全部数据
agent-browser get text @table-header

# 获取第一页数据作为样本
agent-browser get text @table-body

# 记录分页信息
agent-browser get text @pagination
```

### Q: 如何处理动态加载的内容？

```bash
# 触发加载
agent-browser scroll down 500
agent-browser wait 2000

# 或点击"加载更多"
agent-browser click "加载更多"
agent-browser wait 2000

# 确认加载完成
agent-browser snapshot -i
```

### Q: 如何分析多语言系统？

```
建议方案：
1. 优先使用中文界面分析
2. 记录字段的 key（如有）和显示名称
3. 在输出文档中标注语言版本
```

---

## 最佳实践

### 分析前准备

- [ ] 确认有足够权限的账号
- [ ] 准备好登录状态文件
- [ ] 了解系统基本模块结构
- [ ] 创建输出目录

### 分析策略

- **先广后深**：先遍历所有模块，再深入分析
- **及时保存**：每完成一个模块立即保存
- **状态检查**：定期验证登录状态
- **截图记录**：关键页面保留截图

### 文档整理

- **保持原结构**：原样记录部分严格按后台结构
- **智能归类**：分析部分按功能领域组织
- **交叉引用**：建立模块间的关联链接
- **版本标注**：记录分析时间和系统版本

### 质量检查

- 检查导航结构完整性
- 验证 API 列表覆盖度
- 确认权限矩阵准确性
- 核实数据模型合理性
