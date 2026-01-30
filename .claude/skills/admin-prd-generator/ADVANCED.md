# Admin PRD Generator - 高级功能指南

本文档包含 admin-prd-generator 的高级功能和详细配置说明。

---

## 多技术栈支持

### 前端框架支持

#### Vue 2.x

**路由检索模式**：

```javascript
// 标准 Vue Router 配置
{
  path: '/clueManagement/myClue',
  name: 'MyClue',
  component: () => import('@/views/clue/MyClue.vue'),
  meta: { title: '我的线索' }
}
```

**检索策略**：
1. 搜索 `src/router/` 目录下的 `.js` 文件
2. 匹配 `path` 字段
3. 解析 `component` 的 `import()` 语句获取组件路径

#### Vue 3.x

**路由检索模式**：

```typescript
// Vue 3 + TypeScript
{
  path: '/clueManagement/myClue',
  name: 'MyClue',
  component: () => import('@/views/clue/MyClue.vue'),
  meta: { title: '我的线索' }
}
```

**额外检索**：
- 支持 TypeScript 路由定义
- 支持 `defineComponent` 组件
- 支持 `<script setup>` 语法

#### React

**路由检索模式**：

```jsx
// React Router
<Route path="/clue/list" element={<ClueList />} />

// 或配置式
{
  path: '/clue/list',
  element: <ClueList />,
}
```

**检索策略**：
1. 搜索 `src/routes/` 或 `src/router/` 目录
2. 匹配 `<Route path=` 或 `path:` 配置
3. 追踪 `element` 或 `component` 引用

### 后端框架支持

#### Spring Boot 2.x / 3.x

**Controller 检索模式**：

```java
@RestController
@RequestMapping("/api/clue")
public class ClueController {

    @GetMapping("/list")
    public Result<Page<ClueVO>> list(ClueQueryDTO query) {
        return Result.success(clueService.list(query));
    }
}
```

**检索策略**：
1. 搜索 `@RestController` 或 `@Controller` 注解的类
2. 匹配 `@RequestMapping` 类级注解
3. 匹配 `@GetMapping` / `@PostMapping` 等方法级注解
4. 追踪 `@Autowired` 或构造器注入的 Service

#### Express (Node.js)

**路由检索模式**：

```javascript
// Express 路由
router.get('/api/clue/list', clueController.list);
router.post('/api/clue', clueController.create);
```

**检索策略**：
1. 搜索 `router.get` / `router.post` 等调用
2. 匹配路由路径
3. 追踪 Controller 方法

#### FastAPI (Python)

**路由检索模式**：

```python
@router.get("/api/clue/list")
async def list_clues(query: ClueQuery = Depends()):
    return await clue_service.list(query)
```

**检索策略**：
1. 搜索 `@router.get` / `@app.post` 等装饰器
2. 匹配路由路径
3. 追踪 Service 调用

---

## 自定义检索规则

### 非标准项目结构

如果项目结构不符合标准约定，可以通过配置指定路径：

```yaml
# .prd-config.yaml
frontend:
  framework: vue
  version: "2.x"
  paths:
    router: "src/config/routes"      # 自定义路由目录
    views: "src/pages"               # 自定义页面目录
    api: "src/services/api"          # 自定义 API 目录
    components: "src/components"     # 组件目录

backend:
  framework: spring-boot
  version: "2.x"
  paths:
    controller: "src/main/java/**/web"    # 自定义 Controller 目录
    service: "src/main/java/**/service"   # 自定义 Service 目录
    entity: "src/main/java/**/domain"     # 自定义实体目录
    dto: "src/main/java/**/dto"           # DTO 目录
```

### 自定义路由匹配规则

```yaml
# 路由匹配配置
routing:
  # URL 前缀映射
  url_prefix_mapping:
    "/#/": ""                    # 去除 hash 前缀
    "/admin/": ""                # 去除 admin 前缀

  # 路由路径到组件路径的转换规则
  path_to_component:
    pattern: "/{module}/{page}"
    component: "src/views/{module}/{Page}.vue"
    # {Page} 表示首字母大写
```

### 自定义 API 匹配规则

```yaml
# API 匹配配置
api:
  # API 前缀
  base_path: "/api/v1"

  # Controller 类名模式
  controller_pattern: "{Module}Controller"

  # 方法名映射
  method_mapping:
    "GET /list": "list"
    "GET /{id}": "getById"
    "POST /": "create"
    "PUT /{id}": "update"
    "DELETE /{id}": "delete"
```

---

## 增量更新机制

### 增量检测

当代码仓库有更新时，支持只更新变化的部分：

```
增量更新流程：

1. 检测代码变更
   - 对比 Git commit hash
   - 获取变更文件列表

2. 识别影响范围
   - 变更的组件 → 影响的模块
   - 变更的 API → 影响的接口文档

3. 增量生成
   - 只重新生成受影响的文档
   - 保留未变更的文档
```

### 增量更新命令

```
请执行增量更新，只更新以下变更：
- 前端：src/views/clue/MyClue.vue 修改
- 后端：ClueController.java 新增方法
```

### 变更追踪

状态文件会记录文档与代码的对应关系：

```json
{
  "document_sources": {
    "05_产品需求/线索管理/功能清单.md": {
      "frontend_files": [
        "src/views/clue/MyClue.vue",
        "src/api/clue.js"
      ],
      "backend_files": [
        "ClueController.java",
        "ClueService.java"
      ],
      "last_updated": "2024-01-15T10:30:00Z"
    }
  }
}
```

---

## 微服务架构支持

### 多仓库配置

```yaml
# 微服务配置
repositories:
  frontend:
    - name: "admin-web"
      url: "https://github.com/xxx/admin-web.git"
      modules: ["用户管理", "权限管理"]
    - name: "clue-web"
      url: "https://github.com/xxx/clue-web.git"
      modules: ["线索管理", "订单管理"]

  backend:
    - name: "user-service"
      url: "https://github.com/xxx/user-service.git"
      api_prefix: "/api/user"
      modules: ["用户管理"]
    - name: "clue-service"
      url: "https://github.com/xxx/clue-service.git"
      api_prefix: "/api/clue"
      modules: ["线索管理"]
    - name: "order-service"
      url: "https://github.com/xxx/order-service.git"
      api_prefix: "/api/order"
      modules: ["订单管理"]
```

### 服务映射

```
API 端点          →  后端服务        →  代码位置
/api/user/*      →  user-service   →  UserController
/api/clue/*      →  clue-service   →  ClueController
/api/order/*     →  order-service  →  OrderController
```

### 网关路由识别

支持从 API 网关配置中提取路由规则：

```yaml
# Spring Cloud Gateway 配置
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/user/**
        - id: clue-service
          uri: lb://clue-service
          predicates:
            - Path=/api/clue/**
```

---

## 交互式确认模式

### 启用确认模式

对于关键推断，支持交互式确认：

```
⚠️ 需要确认的映射关系：

1. 路由映射确认
   UI 路由: /#/clueManagement/myClue
   推断组件: src/views/clue/MyClue.vue
   是否正确？ [Y/n]

2. API 映射确认
   API 端点: GET /api/clue/list
   推断 Controller: ClueController.list()
   是否正确？ [Y/n]

3. 业务规则确认
   发现业务规则: "线索状态为已转化时不允许编辑"
   代码位置: ClueService.java:125
   是否添加到文档？ [Y/n]
```

### 确认结果记录

确认结果会记录在状态文件中，下次生成时直接使用：

```json
{
  "confirmations": {
    "route_mappings": {
      "/#/clueManagement/myClue": {
        "confirmed": true,
        "component": "src/views/clue/MyClue.vue"
      }
    },
    "api_mappings": {
      "GET /api/clue/list": {
        "confirmed": true,
        "controller": "ClueController.list()"
      }
    }
  }
}
```

---

## 代码审计模式

### 一致性检查

检查 UI 定义与代码实现的一致性：

```
🔍 一致性审计报告

字段一致性检查:
├─ ✅ 线索名称: UI(必填) = 前端(required) = 后端(@NotBlank)
├─ ⚠️ 手机号: UI(必填) ≠ 前端(可选) - 建议前端添加必填校验
├─ ⚠️ 备注: 前端(max=200) ≠ 后端(max=500) - 建议统一长度限制
└─ ❌ 创建时间: UI(显示) ≠ 后端(不返回) - 接口未返回该字段

API 一致性检查:
├─ ✅ GET /api/clue/list: 文档定义 = 代码实现
├─ ⚠️ POST /api/clue: 文档参数 3 个 ≠ 代码参数 5 个
└─ ❌ GET /api/clue/export: 文档定义存在，代码实现未找到
```

### 覆盖率报告

```
📊 PRD 覆盖率报告

模块覆盖率: 100% (6/6)
├─ 线索管理: 100%
├─ 人员管理: 100%
├─ 系统管理: 100%
└─ ...

功能覆盖率: 95% (38/40)
├─ 列表查询: 100%
├─ 新增: 100%
├─ 编辑: 100%
├─ 删除: 100%
└─ 导出: 0% ⚠️ 代码实现未找到

字段覆盖率: 87% (52/60)
└─ 8 个字段在代码中未找到定义
```

---

## 输出格式配置

### 详细程度

```yaml
output:
  # minimal: 只生成核心需求文档
  # standard: 生成完整需求文档（默认）
  # full: 生成需求文档 + 代码片段 + 详细映射
  detail_level: "standard"
```

### 代码片段包含

```yaml
output:
  include_code_snippets: true
  code_snippet_config:
    max_lines: 20           # 每个代码片段最多行数
    include_comments: true  # 是否包含注释
    syntax_highlight: true  # 是否语法高亮
```

### 自定义模板

支持使用自定义 Markdown 模板：

```yaml
output:
  templates:
    readme: "./templates/prd-readme.md"
    module_overview: "./templates/module-overview.md"
    function_list: "./templates/function-list.md"
```

---

## 常见问题 Q&A

### Q1: 路由无法映射到组件怎么办？

**可能原因**：
1. 路由配置使用了动态导入别名
2. 组件路径不符合标准约定
3. 使用了嵌套路由

**解决方案**：
```yaml
# 在配置中指定路径映射
routing:
  alias_mapping:
    "@": "src"
    "@views": "src/views"
```

### Q2: API 无法映射到 Controller 怎么办？

**可能原因**：
1. 使用了 API 网关转发
2. Controller 使用了非标准注解
3. API 前缀不匹配

**解决方案**：
```yaml
# 配置 API 前缀转换
api:
  prefix_mapping:
    "/api/v1/": "/api/"
    "/gateway/": "/"
```

### Q3: 如何处理复杂的业务规则？

**解决方案**：

1. **启用交互确认模式**：人工确认关键业务规则
2. **标注代码位置**：在文档中标注规则来源代码
3. **添加注释标记**：在代码中使用特殊注释标记业务规则

```java
// @PRD: 线索状态为已转化时不允许编辑
if (clue.getStatus() == ClueStatus.CONVERTED) {
    throw new BusinessException("已转化的线索不允许编辑");
}
```

### Q4: 如何处理前后端校验不一致的情况？

**解决方案**：

生成的文档会标注不一致项：

```markdown
### 字段校验（前后端不一致 ⚠️）

| 字段 | 前端校验 | 后端校验 | 建议 |
|-----|---------|---------|------|
| 手机号 | 可选 | @NotBlank | 建议前端添加必填校验 |
| 备注 | max=200 | max=500 | 建议统一为 200 |
```

### Q5: 如何处理微服务架构？

**解决方案**：

1. 配置多仓库映射
2. 指定每个服务的 API 前缀
3. 生成的文档会标注服务归属

```markdown
### API 端点

| 接口 | 服务 | 路径 |
|-----|------|------|
| 用户列表 | user-service | GET /api/user/list |
| 线索列表 | clue-service | GET /api/clue/list |
```

---

## 最佳实践

### 准备工作

- [ ] 确保 admin-reverse-docs 文档完整
- [ ] 确保代码仓库可访问（权限、网络）
- [ ] 确认技术栈版本

### 执行过程

- [ ] 先运行一次完整生成，检查映射准确性
- [ ] 对映射不准确的项进行手动确认
- [ ] 检查生成的业务规则是否完整

### 维护更新

- [ ] 代码更新后执行增量更新
- [ ] 定期检查一致性审计报告
- [ ] 保持状态文件与代码版本同步
