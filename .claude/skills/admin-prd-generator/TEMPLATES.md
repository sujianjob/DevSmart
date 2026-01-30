# Admin PRD Generator - 输出模板

本文档包含所有输出文件的标准模板，重点是**深度分析代码**后提取的业务规则和数据流转。

---

## 输出目录结构

```
{系统名}_admin_docs/
└── 05_产品需求/
    ├── README.md                    # PRD 总览
    ├── .prd-state.json              # 状态文件（断点续生成）
    │
    ├── {模块名}/
    │   ├── 需求概述.md             # 模块功能概述
    │   ├── 功能清单.md             # 详细功能点
    │   ├── 业务规则.md             # 【核心】深度提取的业务规则
    │   ├── 数据流转.md             # 【新增】数据在系统中的完整流转
    │   └── 接口清单.md             # 完整的接口定义
    │
    ├── _业务逻辑汇总.md            # 【新增】跨模块的业务逻辑汇总
    └── _代码映射.md                 # 代码位置快速索引
```

---

## README.md 总览模板

```markdown
# {系统名} - 产品需求说明文档

> 生成时间：{YYYY-MM-DD HH:mm:ss}
> 基于文档：{admin-reverse-docs 目录路径}
> 前端仓库：{前端仓库地址}
> 后端仓库：{后端仓库地址}

---

## 系统概述

### 系统简介

{从 admin-reverse-docs README 和代码注释中提取的系统描述}

### 技术架构

| 层级 | 技术栈 | 版本 |
|-----|-------|------|
| 前端 | Vue.js | {版本} |
| 后端 | Spring Boot | {版本} |
| 数据库 | MySQL | {版本} |

### 用户角色

| 角色 | 描述 | 主要功能 |
|-----|------|---------|
| {角色1} | {描述} | {功能列表} |
| {角色2} | {描述} | {功能列表} |

---

## 功能模块

| 模块 | 子功能数 | 接口数 | 文档链接 |
|-----|---------|-------|---------|
| {模块1} | {N} | {M} | [{模块1}](./{模块1}/) |
| {模块2} | {N} | {M} | [{模块2}](./{模块2}/) |

---

## 目录索引

### 模块需求文档

- [{模块1}](./{模块1}/需求概述.md)
  - [功能清单](./{模块1}/功能清单.md)
  - [业务规则](./{模块1}/业务规则.md)
  - [接口清单](./{模块1}/接口清单.md)
- [{模块2}](./{模块2}/需求概述.md)
  - ...

### 附录

- [代码映射表](./_代码映射.md) - 路由、API 与代码位置的完整映射

---

## 生成统计

```
📊 文档生成统计

模块数量: {N}
功能点数: {M}
API 接口: {K}
代码映射: {L}

映射覆盖率:
├─ 路由映射: {X}% ({mapped}/{total})
├─ API 映射: {Y}% ({mapped}/{total})
└─ 字段校验: {Z}% ({matched}/{total})
```

---

## 版本历史

| 版本 | 日期 | 说明 |
|-----|------|------|
| 1.0 | {日期} | 初始版本 |
```

---

## 需求概述模板

```markdown
# {模块名} - 需求概述

> 文档版本：1.0
> 更新时间：{YYYY-MM-DD}
> 关联文档：
> - UI 原型：[01_原始记录/{模块名}](../../01_原始记录/{模块名}/)
> - 数据模型：[02_数据模型/实体关系.md](../../02_数据模型/实体关系.md)
> - API 文档：[03_API文档/接口列表.md](../../03_API文档/接口列表.md)

---

## 1. 功能目标

### 1.1 业务背景

{从代码注释和业务分析中提取的背景描述}

### 1.2 功能目标

{模块的核心功能目标}

### 1.3 功能范围

**包含**：
- {功能点1}
- {功能点2}

**不包含**：
- {排除项1}
- {排除项2}

---

## 2. 用户角色

| 角色 | 权限范围 | 主要操作 |
|-----|---------|---------|
| {角色1} | {权限描述} | {操作列表} |
| {角色2} | {权限描述} | {操作列表} |

---

## 3. 功能架构

```
{模块名}
├── {子功能1}
│   ├── 列表查询
│   ├── 新增
│   ├── 编辑
│   └── 删除
├── {子功能2}
│   └── ...
└── {子功能3}
    └── ...
```

---

## 4. 页面清单

| 页面名称 | 路由 | 页面类型 | 说明 |
|---------|------|---------|------|
| {页面1} | `{路由}` | 列表页 | {说明} |
| {页面2} | `{路由}` | 表单页 | {说明} |
| {页面3} | `{路由}` | 详情页 | {说明} |

---

## 5. 代码位置

### 前端

| 功能 | 组件路径 | API 文件 |
|-----|---------|---------|
| 列表页 | `{组件路径}` | `{API文件}` |
| 新增/编辑 | `{组件路径}` | `{API文件}` |

### 后端

| 功能 | Controller | Service |
|-----|-----------|---------|
| 列表查询 | `{Controller}.list()` | `{Service}.list()` |
| 新增 | `{Controller}.create()` | `{Service}.create()` |
| 编辑 | `{Controller}.update()` | `{Service}.update()` |
| 删除 | `{Controller}.delete()` | `{Service}.delete()` |

---

## 6. 相关文档

- [功能清单](./功能清单.md) - 详细功能点定义
- [业务规则](./业务规则.md) - 业务规则和约束
- [接口清单](./接口清单.md) - API 接口定义
```

---

## 功能清单模板

```markdown
# {模块名} - 功能清单

> 文档版本：1.0
> 更新时间：{YYYY-MM-DD}

---

## 1. {页面名称}

**页面路径**：`{URL路径}`
**页面类型**：列表页 / 表单页 / 详情页
**前端组件**：`{组件路径}`

### 1.1 筛选条件

| 字段名 | 字段标识 | 控件类型 | 必填 | 默认值 | 说明 |
|-------|---------|---------|------|--------|------|
| {字段1} | `{fieldName}` | 输入框 | 否 | - | {说明} |
| {字段2} | `{fieldName}` | 下拉选择 | 否 | 全部 | {说明} |
| {字段3} | `{fieldName}` | 日期范围 | 否 | - | {说明} |

**数据来源**：
- UI 定义：`01_原始记录/{模块名}/README.md`
- 前端实现：`{组件路径}` 第 XX 行
- 后端接口：`GET {API路径}` 的 Query 参数

### 1.2 列表字段

| 序号 | 列名 | 字段标识 | 数据类型 | 可排序 | 说明 |
|-----|-----|---------|---------|--------|------|
| 1 | {列1} | `{fieldName}` | String | 是 | {说明} |
| 2 | {列2} | `{fieldName}` | Number | 否 | {说明} |
| 3 | {列3} | `{fieldName}` | Enum | 否 | {说明} |
| 4 | {列4} | `{fieldName}` | DateTime | 是 | {说明} |

**数据来源**：
- UI 定义：`01_原始记录/{模块名}/README.md`
- 前端实现：`{组件路径}` columns 配置
- 后端响应：`{DTO/VO}.java` 字段定义

### 1.3 操作按钮

#### 页面级操作

| 按钮名称 | 触发动作 | 权限标识 | 说明 |
|---------|---------|---------|------|
| 新增 | 打开新增弹窗/跳转新增页 | `{module}:create` | {说明} |
| 批量删除 | 删除选中项 | `{module}:delete` | 需选中数据 |
| 导出 | 导出 Excel | `{module}:export` | {说明} |

#### 行级操作

| 按钮名称 | 触发动作 | 权限标识 | 说明 |
|---------|---------|---------|------|
| 查看 | 打开详情弹窗 | `{module}:read` | - |
| 编辑 | 打开编辑弹窗 | `{module}:update` | - |
| 删除 | 弹出确认框后删除 | `{module}:delete` | 需二次确认 |

---

## 2. {表单名称}

**触发方式**：点击"新增"/"编辑"按钮
**表单类型**：弹窗 / 独立页面
**前端组件**：`{组件路径}`

### 2.1 表单字段

| 字段名 | 字段标识 | 控件类型 | 必填 | 验证规则 | 说明 |
|-------|---------|---------|------|---------|------|
| {字段1} | `{fieldName}` | 输入框 | 是 | 2-50字符 | {说明} |
| {字段2} | `{fieldName}` | 下拉选择 | 是 | - | 数据源：{接口/枚举} |
| {字段3} | `{fieldName}` | 日期选择 | 否 | - | {说明} |
| {字段4} | `{fieldName}` | 文本域 | 否 | 最多500字符 | {说明} |

### 2.2 字段详细说明

#### {字段名}

- **UI 显示**：{UI 展示方式}
- **前端校验**：
  ```javascript
  // 位置：{组件路径} 第 XX 行
  {
    required: true,
    message: '{错误提示}',
    trigger: 'blur'
  }
  ```
- **后端校验**：
  ```java
  // 位置：{DTO}.java 第 XX 行
  @NotBlank(message = "{错误提示}")
  @Size(max = 50)
  private String {fieldName};
  ```
- **数据库**：`{表名}.{字段名}` VARCHAR(50) NOT NULL

### 2.3 表单操作

| 操作 | 触发条件 | 处理逻辑 | API |
|-----|---------|---------|-----|
| 保存 | 点击保存按钮 | 校验→提交→关闭 | `POST/PUT {API}` |
| 取消 | 点击取消按钮 | 关闭弹窗/返回列表 | - |
| 重置 | 点击重置按钮 | 清空所有输入 | - |

---

## 3. 数据字典

### 3.1 枚举值定义

#### {枚举名称}

| 值 | 显示文本 | 说明 |
|---|---------|------|
| `0` | {文本1} | {说明} |
| `1` | {文本2} | {说明} |
| `2` | {文本3} | {说明} |

**数据来源**：
- 前端：`{常量文件路径}`
- 后端：`{枚举类路径}`
- 数据库：字典表 `{表名}`
```

---

## 业务规则模板

```markdown
# {模块名} - 业务规则

> 文档版本：1.0
> 更新时间：{YYYY-MM-DD}

---

## 1. 数据校验规则

### 1.1 字段校验

| 字段 | 规则类型 | 规则描述 | 错误提示 | 校验位置 |
|-----|---------|---------|---------|---------|
| {字段1} | 必填 | 不能为空 | 请输入{字段1} | 前端+后端 |
| {字段1} | 长度 | 2-50 字符 | {字段1}长度为2-50字符 | 前端+后端 |
| {字段2} | 格式 | 11位手机号 | 请输入正确的手机号 | 前端+后端 |
| {字段3} | 唯一性 | 不能重复 | {字段3}已存在 | 后端 |

### 1.2 校验代码位置

**前端校验**：
```javascript
// 位置：{组件路径}
const rules = {
  {fieldName}: [
    { required: true, message: '{提示}', trigger: 'blur' },
    { min: 2, max: 50, message: '{提示}', trigger: 'blur' }
  ]
}
```

**后端校验**：
```java
// 位置：{DTO}.java
@NotBlank(message = "{提示}")
@Size(min = 2, max = 50, message = "{提示}")
private String {fieldName};
```

---

## 2. 业务约束规则

### BR-001: {规则名称}

**规则描述**：{详细描述}

**触发场景**：{什么情况下触发此规则}

**处理逻辑**：
```
1. {步骤1}
2. {步骤2}
3. {步骤3}
```

**代码位置**：
- Service：`{Service}.java` 第 XX 行
- 方法：`{methodName}()`

**代码片段**：
```java
// {Service}.java
public void {methodName}({参数}) {
    // 业务规则实现
    {代码片段}
}
```

---

## 3. 状态流转规则

### {实体名}状态机

```
[初始状态] ──{动作1}──> [状态A]
    │                    │
    │               {动作2}
    │                    ↓
    └──{动作3}────> [状态B] ──{动作4}──> [终态]
```

### 状态定义

| 状态值 | 状态名称 | 说明 |
|-------|---------|------|
| `0` | {状态1} | {说明} |
| `1` | {状态2} | {说明} |
| `2` | {状态3} | {说明} |

### 状态转移规则

| 当前状态 | 触发动作 | 目标状态 | 前置条件 | 后置动作 |
|---------|---------|---------|---------|---------|
| {状态1} | {动作} | {状态2} | {条件} | {动作} |
| {状态2} | {动作} | {状态3} | {条件} | {动作} |

**代码位置**：`{Service}.java` 的 `{方法名}()` 方法

---

## 4. 权限控制规则

### 4.1 功能权限

| 功能 | 权限标识 | 说明 |
|-----|---------|------|
| 查看列表 | `{module}:list` | 查看{模块}列表 |
| 查看详情 | `{module}:read` | 查看{模块}详情 |
| 新增 | `{module}:create` | 新增{模块} |
| 编辑 | `{module}:update` | 编辑{模块} |
| 删除 | `{module}:delete` | 删除{模块} |
| 导出 | `{module}:export` | 导出{模块}数据 |

### 4.2 数据权限

| 角色 | 数据范围 | 说明 |
|-----|---------|------|
| 管理员 | 全部数据 | 可查看所有数据 |
| 普通用户 | 本人数据 | 只能查看自己创建的数据 |
| 部门主管 | 部门数据 | 可查看本部门所有数据 |

---

## 5. 异常处理规则

| 异常场景 | 错误码 | 错误提示 | 处理方式 |
|---------|-------|---------|---------|
| {字段}为空 | 400 | {提示} | 前端校验拦截 |
| {字段}已存在 | 400 | {提示} | 后端校验返回 |
| 数据不存在 | 404 | {提示} | 后端校验返回 |
| 无操作权限 | 403 | {提示} | 后端权限拦截 |
```

---

## 接口清单模板

```markdown
# {模块名} - 接口清单

> 文档版本：1.0
> 更新时间：{YYYY-MM-DD}

---

## 接口概览

| 接口名称 | 方法 | 路径 | 说明 |
|---------|------|------|------|
| 获取列表 | GET | `/api/{module}/list` | 分页查询{模块}列表 |
| 获取详情 | GET | `/api/{module}/{id}` | 获取{模块}详情 |
| 新增 | POST | `/api/{module}` | 新增{模块} |
| 编辑 | PUT | `/api/{module}/{id}` | 编辑{模块} |
| 删除 | DELETE | `/api/{module}/{id}` | 删除{模块} |
| 批量删除 | DELETE | `/api/{module}/batch` | 批量删除{模块} |
| 导出 | GET | `/api/{module}/export` | 导出{模块}数据 |

---

## 接口详情

### 1. 获取{模块}列表

**基本信息**

| 属性 | 值 |
|-----|---|
| 接口路径 | `GET /api/{module}/list` |
| 接口说明 | 分页查询{模块}列表 |
| 权限标识 | `{module}:list` |

**代码位置**

| 层级 | 位置 |
|-----|------|
| Controller | `{Controller}.java` → `list()` |
| Service | `{Service}.java` → `list()` |
| Repository | `{Repository}.java` → `findByCondition()` |

**请求参数**

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|-------|------|------|------|------|
| pageNum | Integer | 否 | 页码，默认 1 | 1 |
| pageSize | Integer | 否 | 每页条数，默认 10 | 10 |
| {param1} | String | 否 | {说明} | {示例} |
| {param2} | Integer | 否 | {说明} | {示例} |

**请求示例**

```http
GET /api/{module}/list?pageNum=1&pageSize=10&{param1}={value}
```

**响应参数**

| 参数名 | 类型 | 说明 |
|-------|------|------|
| code | Integer | 状态码，200 表示成功 |
| message | String | 提示信息 |
| data | Object | 响应数据 |
| data.total | Long | 总条数 |
| data.list | Array | 数据列表 |
| data.list[].{field1} | String | {说明} |
| data.list[].{field2} | Integer | {说明} |

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "list": [
      {
        "{field1}": "{value}",
        "{field2}": 1
      }
    ]
  }
}
```

**前端调用**

```javascript
// 位置：{API文件路径}
export function get{Module}List(params) {
  return request({
    url: '/api/{module}/list',
    method: 'get',
    params
  })
}
```

---

### 2. 新增{模块}

**基本信息**

| 属性 | 值 |
|-----|---|
| 接口路径 | `POST /api/{module}` |
| 接口说明 | 新增{模块} |
| 权限标识 | `{module}:create` |

**代码位置**

| 层级 | 位置 |
|-----|------|
| Controller | `{Controller}.java` → `create()` |
| Service | `{Service}.java` → `create()` |
| DTO | `{CreateDTO}.java` |

**请求参数**

| 参数名 | 类型 | 必填 | 校验规则 | 说明 |
|-------|------|------|---------|------|
| {field1} | String | 是 | 2-50字符 | {说明} |
| {field2} | Integer | 是 | - | {说明} |
| {field3} | String | 否 | 最多500字符 | {说明} |

**请求示例**

```json
{
  "{field1}": "{value}",
  "{field2}": 1,
  "{field3}": "{value}"
}
```

**响应参数**

| 参数名 | 类型 | 说明 |
|-------|------|------|
| code | Integer | 状态码 |
| message | String | 提示信息 |
| data | Long | 新增记录 ID |

**错误响应**

| 错误码 | 错误信息 | 说明 |
|-------|---------|------|
| 400 | {field1}不能为空 | 必填字段为空 |
| 400 | {field1}已存在 | 唯一性校验失败 |
```

---

## 代码映射表模板

```markdown
# 代码映射表

> 生成时间：{YYYY-MM-DD HH:mm:ss}

本文档记录 UI 路由、API 端点与代码位置的完整映射关系。

---

## 1. 路由 → 组件映射

| UI 路由 | 菜单路径 | 前端组件 | API 文件 |
|--------|---------|---------|---------|
| `/#/{path1}` | {菜单1} > {菜单2} | `src/views/{path}/{Component}.vue` | `src/api/{module}.js` |
| `/#/{path2}` | {菜单1} > {菜单3} | `src/views/{path}/{Component}.vue` | `src/api/{module}.js` |

---

## 2. API → 后端映射

| API 端点 | Controller | 方法 | Service | 方法 |
|---------|-----------|------|---------|------|
| `GET /api/{m}/list` | `{M}Controller` | `list()` | `{M}Service` | `list()` |
| `GET /api/{m}/{id}` | `{M}Controller` | `getById()` | `{M}Service` | `getById()` |
| `POST /api/{m}` | `{M}Controller` | `create()` | `{M}Service` | `create()` |
| `PUT /api/{m}/{id}` | `{M}Controller` | `update()` | `{M}Service` | `update()` |
| `DELETE /api/{m}/{id}` | `{M}Controller` | `delete()` | `{M}Service` | `delete()` |

---

## 3. 实体 → 数据表映射

| 实体类 | 数据表 | 主要字段 |
|-------|-------|---------|
| `{Entity}.java` | `{table_name}` | id, {field1}, {field2}, ... |

---

## 4. 未映射项

### 4.1 未找到前端组件的路由

| UI 路由 | 可能原因 |
|--------|---------|
| `{路由}` | {原因} |

### 4.2 未找到后端实现的 API

| API 端点 | 可能原因 |
|---------|---------|
| `{API}` | {原因} |
```

---

## 状态文件格式

`.prd-state.json`

```json
{
  "version": "1.0",
  "created_at": "{YYYY-MM-DDTHH:mm:ssZ}",
  "updated_at": "{YYYY-MM-DDTHH:mm:ssZ}",

  "admin_docs_path": "./{系统名}_admin_docs",
  "output_path": "./{系统名}_admin_docs/05_产品需求",

  "repositories": {
    "frontend": {
      "type": "git|local",
      "url": "{Git仓库地址}",
      "local_path": "{本地路径}",
      "branch": "main",
      "framework": "vue",
      "version": "2.x",
      "paths": {
        "router": "src/router",
        "views": "src/views",
        "api": "src/api"
      }
    },
    "backend": {
      "type": "git|local",
      "url": "{Git仓库地址}",
      "local_path": "{本地路径}",
      "branch": "main",
      "framework": "spring-boot",
      "version": "2.x",
      "base_package": "com.example.{module}"
    }
  },

  "progress": {
    "phase": "init|parse|mapping|integrate|generate|verify",
    "started_at": "{YYYY-MM-DDTHH:mm:ssZ}",
    "total_modules": 6,
    "completed_modules": 3,
    "pending_modules": 3
  },

  "parsed_data": {
    "modules": [
      {
        "name": "{模块名}",
        "path": "{路径}",
        "routes": ["{路由1}", "{路由2}"],
        "apis": ["{API1}", "{API2}"]
      }
    ],
    "total_routes": 15,
    "total_apis": 28
  },

  "mappings": {
    "routes": [
      {
        "ui_path": "{UI路由}",
        "menu_path": ["{菜单1}", "{菜单2}"],
        "frontend_component": "{组件路径}",
        "api_file": "{API文件}",
        "status": "mapped|not_found|error"
      }
    ],
    "apis": [
      {
        "endpoint": "{HTTP方法} {路径}",
        "controller": "{Controller}.{method}()",
        "service": "{Service}.{method}()",
        "status": "mapped|not_found|error"
      }
    ]
  },

  "modules_status": [
    {
      "name": "{模块名}",
      "status": "completed|in_progress|pending|error",
      "files_generated": [
        "需求概述.md",
        "功能清单.md",
        "业务规则.md",
        "接口清单.md"
      ],
      "error_message": null
    }
  ],

  "statistics": {
    "routes_mapped": 15,
    "routes_total": 15,
    "apis_mapped": 26,
    "apis_total": 28,
    "fields_matched": 45,
    "fields_total": 52
  }
}
```

---

## 进度显示格式

```
📊 PRD 生成进度: [████████░░░░░░░░] 3/6 模块 (50%)

阶段进度:
├─ ✅ 阶段一：初始化完成
├─ ✅ 阶段二：文档解析完成 (6 个模块, 28 个 API)
├─ ✅ 阶段三：代码映射完成 (15 路由, 26 API)
├─ ⏳ 阶段四：需求整合中...
│     └─ 当前模块: 人员管理
├─ ○ 阶段五：文档生成
└─ ○ 阶段六：校验完善

模块进度:
├─ ✅ 线索管理 (4/4 文件)
├─ ⏳ 人员管理 (2/4 文件)
├─ ○ 系统管理
├─ ○ 订单管理
├─ ○ 统计报表
└─ ○ 日志管理

映射统计:
├─ 路由映射: 15/15 (100%)
├─ API 映射: 26/28 (93%)
│     └─ ⚠️ 2 个 API 未找到后端实现
└─ 字段校验: 45/52 (87%)
      └─ ⚠️ 7 个字段前后端校验不一致
```

---

## 数据流转文档模板（新增）

```markdown
# {模块名} - 数据流转

> 文档版本：1.0
> 更新时间：{YYYY-MM-DD}

本文档描述数据在系统中的完整流转过程，从用户输入到最终存储。

---

## 1. 新增流程

### 1.1 流程概览

```
用户填写表单
    ↓
前端表单校验
    ↓ 校验通过
调用 API: POST /api/{module}
    ↓
Controller 接收请求
    ↓ Bean Validation
Service 业务处理
    ↓ 业务校验 → 数据补全 → 保存
Repository 持久化
    ↓
数据库存储
    ↓
触发事件（如有）
    ↓
返回响应
```

### 1.2 详细步骤

#### 步骤 1: 前端表单提交

**位置**: `{组件路径}`

**数据处理**:
```javascript
// 提交前的数据处理
const submitData = {
  ...this.form,
  // 日期格式转换
  createTime: this.form.createTime?.format('YYYY-MM-DD'),
  // 关联数据处理
  categoryId: this.form.category?.id
}
```

**校验规则**:
| 字段 | 规则 | 错误提示 |
|-----|------|---------|
| {field1} | required | 请输入{field1} |
| {field2} | pattern | 格式不正确 |

#### 步骤 2: Controller 层处理

**位置**: `{Controller}.java` → `create()`

**处理逻辑**:
```java
@PostMapping
public Result<Long> create(@Valid @RequestBody {CreateDTO} dto) {
    // 1. Bean Validation 自动校验 DTO 字段
    // 2. 调用 Service 处理业务逻辑
    Long id = {service}.create(dto);
    return Result.success(id);
}
```

#### 步骤 3: Service 层处理

**位置**: `{Service}.java` → `create()`

**处理逻辑**:
```java
@Transactional
public Long create({CreateDTO} dto) {
    // 1. 业务校验
    checkBusinessRules(dto);

    // 2. 数据补全
    {Entity} entity = new {Entity}();
    BeanUtils.copyProperties(dto, entity);
    entity.setCreateBy(SecurityUtils.getCurrentUserId());
    entity.setCreateTime(LocalDateTime.now());
    entity.setStatus(InitialStatus);

    // 3. 保存数据
    {repository}.save(entity);

    // 4. 触发事件
    eventPublisher.publish(new {Entity}CreatedEvent(entity));

    return entity.getId();
}
```

**业务校验**:
| 检查项 | 条件 | 错误信息 |
|-------|------|---------|
| 唯一性检查 | 名称已存在 | {名称}已存在 |
| 关联检查 | 关联数据不存在 | {关联}不存在 |

**自动填充字段**:
| 字段 | 填充值 | 说明 |
|-----|-------|------|
| createBy | 当前用户 ID | 创建人 |
| createTime | 当前时间 | 创建时间 |
| status | 初始状态 | 状态初始值 |

#### 步骤 4: 数据持久化

**实体映射**: `{Entity}.java` → `{table_name}`

**字段映射**:
| 实体字段 | 数据库字段 | 类型 | 说明 |
|---------|-----------|------|------|
| id | id | BIGINT | 主键 |
| name | name | VARCHAR(50) | 名称 |
| createBy | create_by | BIGINT | 创建人 |
| createTime | create_time | DATETIME | 创建时间 |

---

## 2. 编辑流程

### 2.1 流程概览

```
用户点击编辑
    ↓
加载原有数据: GET /api/{module}/{id}
    ↓
用户修改表单
    ↓
前端校验
    ↓
调用 API: PUT /api/{module}/{id}
    ↓
Controller 接收
    ↓
Service 处理
    ↓ 查询原数据 → 业务校验 → 更新字段 → 保存
记录变更日志（如有）
    ↓
返回响应
```

### 2.2 与新增的差异

| 差异点 | 新增 | 编辑 |
|-------|------|------|
| 数据来源 | 空表单 | 加载原数据 |
| 唯一性检查 | 检查是否存在 | 排除自身后检查 |
| 状态检查 | 无 | 检查是否允许编辑 |
| 记录字段 | createBy/createTime | updateBy/updateTime |

---

## 3. 状态变更流程

### 3.1 状态机

```
[{状态1}] ──{操作1}──> [{状态2}]
              │
              └── 前置条件: {条件描述}
              └── 后置动作: {动作描述}
```

### 3.2 状态变更详情

#### {操作名称}: {状态1} → {状态2}

**触发方式**: 点击"{按钮名}"按钮

**前置条件**:
- 条件 1: {描述}
- 条件 2: {描述}

**处理逻辑**:
```java
// {Service}.java → {method}()
public void {method}(Long id) {
    {Entity} entity = findById(id);

    // 前置检查
    if (!{条件}) {
        throw new BusinessException("{错误信息}");
    }

    // 状态变更
    entity.setStatus({新状态});

    // 后置动作
    {后置处理代码}

    save(entity);
}
```

**后置动作**:
- 动作 1: {描述}
- 动作 2: {描述}

---

## 4. 数据关联

### 4.1 实体关联图

```
[{主实体}]
    │
    ├── 1:N ──> [{关联实体1}]  // {关系描述}
    │
    ├── N:1 <── [{关联实体2}]  // {关系描述}
    │
    └── 1:1 ──> [{关联实体3}]  // {关系描述}
```

### 4.2 关联数据处理

| 操作 | 主实体行为 | 关联实体行为 |
|-----|-----------|-------------|
| 新增 | 创建记录 | {处理方式} |
| 编辑 | 更新记录 | {处理方式} |
| 删除 | 删除/软删 | {处理方式} |
| 状态变更 | 状态更新 | {处理方式} |
```

---

## _业务逻辑汇总文档模板（新增）

```markdown
# 业务逻辑汇总

> 生成时间：{YYYY-MM-DD HH:mm:ss}

本文档汇总所有从代码中提取的业务逻辑，包括跨模块的通用规则。

---

## 1. 全局校验规则

### 1.1 通用字段校验

| 字段类型 | 校验规则 | 代码位置 |
|---------|---------|---------|
| 手机号 | 11位数字，1开头 | `ValidatorUtil.java` |
| 邮箱 | 标准邮箱格式 | `ValidatorUtil.java` |
| 身份证 | 18位，校验位验证 | `IdCardValidator.java` |

### 1.2 通用业务校验

| 规则 ID | 规则描述 | 适用模块 | 代码位置 |
|--------|---------|---------|---------|
| GR-001 | 软删除数据不可编辑 | 全部 | `BaseService.java` |
| GR-002 | 数据权限过滤 | 全部 | `DataScopeAspect.java` |

---

## 2. 状态机汇总

### 2.1 {实体1}状态机

```
[新建] ──提交──> [待审核] ──审核通过──> [已生效]
                    │
                    └──审核拒绝──> [已拒绝]
```

**状态定义**: `{StatusEnum}.java`

| 状态值 | 状态名 | 允许操作 |
|-------|-------|---------|
| 0 | 新建 | 编辑、删除、提交 |
| 1 | 待审核 | 审核通过、审核拒绝 |
| 2 | 已生效 | 查看 |
| 3 | 已拒绝 | 编辑、删除、重新提交 |

### 2.2 {实体2}状态机

...

---

## 3. 事件驱动逻辑

### 3.1 事件清单

| 事件名称 | 触发条件 | 监听器 | 处理逻辑 |
|---------|---------|-------|---------|
| `{Entity}CreatedEvent` | 新增成功后 | `{Entity}EventListener` | {处理描述} |
| `{Entity}UpdatedEvent` | 更新成功后 | `{Entity}EventListener` | {处理描述} |
| `{Entity}StatusChangedEvent` | 状态变更后 | `{Entity}EventListener` | {处理描述} |

### 3.2 事件处理详情

#### {EventName}

**触发点**: `{Service}.java:{line}`

```java
eventPublisher.publish(new {EventName}(entity));
```

**监听处理**: `{Listener}.java`

```java
@EventListener
public void handle{EventName}({EventName} event) {
    // 处理逻辑
    {处理代码}
}
```

**后续动作**:
- 动作 1: {描述}
- 动作 2: {描述}

---

## 4. 定时任务

### 4.1 任务清单

| 任务名称 | 执行周期 | 处理逻辑 | 代码位置 |
|---------|---------|---------|---------|
| {任务1} | 每天 02:00 | {描述} | `{Task}.java` |
| {任务2} | 每小时 | {描述} | `{Task}.java` |

### 4.2 任务详情

#### {任务名称}

**执行周期**: `@Scheduled(cron = "{cron表达式}")`

**代码位置**: `{TaskClass}.java`

**处理逻辑**:
```java
@Scheduled(cron = "{cron}")
public void {method}() {
    // 1. 查询待处理数据
    List<{Entity}> list = {查询逻辑};

    // 2. 批量处理
    for ({Entity} entity : list) {
        {处理逻辑}
    }

    // 3. 记录执行结果
    log.info("{日志信息}");
}
```

**业务规则**:
- 规则 1: {描述}
- 规则 2: {描述}

---

## 5. 权限控制汇总

### 5.1 功能权限

| 权限标识 | 权限名称 | 适用模块 |
|---------|---------|---------|
| `{module}:list` | 查看列表 | {模块} |
| `{module}:create` | 新增 | {模块} |
| `{module}:update` | 编辑 | {模块} |
| `{module}:delete` | 删除 | {模块} |

### 5.2 数据权限

| 权限类型 | 说明 | 实现方式 |
|---------|------|---------|
| 全部数据 | 可查看所有数据 | 无过滤 |
| 部门数据 | 只能查看本部门数据 | `DataScopeAspect` |
| 个人数据 | 只能查看自己的数据 | `createBy = currentUserId` |

### 5.3 权限检查代码

**注解方式**:
```java
@PreAuthorize("hasPermission('{module}', 'create')")
public Result create(...) { }
```

**手动检查**:
```java
if (!SecurityUtils.hasPermission("{permission}")) {
    throw new AccessDeniedException("无操作权限");
}
```

---

## 6. 异常处理汇总

### 6.1 业务异常

| 异常类型 | 错误码 | 错误信息模板 | 触发场景 |
|---------|-------|-------------|---------|
| `BusinessException` | 400 | {动态信息} | 业务规则校验失败 |
| `NotFoundException` | 404 | 数据不存在 | 查询数据为空 |
| `AccessDeniedException` | 403 | 无操作权限 | 权限校验失败 |

### 6.2 全局异常处理

**代码位置**: `GlobalExceptionHandler.java`

```java
@ExceptionHandler(BusinessException.class)
public Result handleBusinessException(BusinessException e) {
    return Result.error(e.getCode(), e.getMessage());
}
```

---

## 7. 业务规则索引

按模块汇总所有业务规则的快速索引。

| 规则 ID | 规则描述 | 所属模块 | 详细位置 |
|--------|---------|---------|---------|
| BR-001 | {描述} | {模块} | [{模块}/业务规则.md#BR-001](./{模块}/业务规则.md#BR-001) |
| BR-002 | {描述} | {模块} | [{模块}/业务规则.md#BR-002](./{模块}/业务规则.md#BR-002) |
| VR-001 | {描述} | {模块} | [{模块}/业务规则.md#VR-001](./{模块}/业务规则.md#VR-001) |
| SR-001 | {描述} | {模块} | [{模块}/业务规则.md#SR-001](./{模块}/业务规则.md#SR-001) |
```
