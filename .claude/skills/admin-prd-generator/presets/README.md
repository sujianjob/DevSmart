# Admin PRD Generator - 预设配置

本目录包含预定义的配置文件，用于快速适配不同技术栈的项目。

---

## 可用预设

| 预设文件 | 适用场景 | 说明 |
|---------|---------|------|
| `standard-vue-springboot.yaml` | Vue + Spring Boot 单体应用 | 最常见的企业后台技术栈 |
| `microservices.yaml` | 微服务架构 | 多仓库、多服务场景 |

---

## 预设使用方式

### 自动检测

默认情况下，会根据代码仓库自动检测技术栈：

```
检测前端框架：
├─ package.json 中包含 "vue" → Vue
├─ package.json 中包含 "react" → React
└─ package.json 中包含 "angular" → Angular

检测后端框架：
├─ pom.xml 中包含 "spring-boot" → Spring Boot
├─ package.json 中包含 "express" → Express
└─ requirements.txt 中包含 "fastapi" → FastAPI
```

### 手动指定

如果自动检测不准确，可以手动指定预设：

```
请使用 standard-vue-springboot 预设生成 PRD 文档
```

---

## 预设文件格式

### 基本结构

```yaml
# 预设元信息
name: preset-name
description: 预设描述
version: "1.0"

# 前端配置
frontend:
  framework: vue
  version: "2.x"
  paths:
    router: "src/router"
    views: "src/views"
    api: "src/api"

# 后端配置
backend:
  framework: spring-boot
  version: "2.x"
  base_package: "com.example"
  paths:
    controller: "src/main/java/**/controller"
    service: "src/main/java/**/service"

# 输出配置
output:
  language: "zh-CN"
  detail_level: "standard"
```

---

## 扩展预设

### 创建新预设

1. 复制现有预设文件
2. 修改配置项
3. 保存为新的 YAML 文件

### 预设继承

可以基于现有预设进行扩展：

```yaml
extends: standard-vue-springboot

# 覆盖特定配置
frontend:
  paths:
    views: "src/pages"  # 覆盖组件目录

# 添加新配置
custom:
  extra_option: value
```

---

## 贡献预设

如果你的项目使用了特殊的技术栈组合，欢迎贡献新的预设配置：

1. 创建 YAML 配置文件
2. 添加完整的注释说明
3. 提交到 presets/ 目录
