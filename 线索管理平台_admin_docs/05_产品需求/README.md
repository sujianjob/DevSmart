# 线索管理平台 - 产品需求文档 (PRD)

> 基于 admin-reverse-docs 输出和代码仓库深度分析自动生成

## 概述

本文档是线索管理平台的完整产品需求说明，通过分析前后端代码实现逻辑提取。

### 技术栈

| 层次 | 技术 | 版本 |
|-----|------|------|
| 前端 | Vue 2 | 2.7.13 |
| UI 框架 | Element UI | 2.15.6 |
| 后端 | Spring Boot | 2.0.3 |
| 数据库 | MySQL | - |
| 缓存 | Redis | - |
| 构建 | Gradle | - |

### 代码仓库

| 仓库 | 类型 | 说明 |
|-----|------|------|
| clue-operate | 全栈 | 运营后台（前端+Web层） |
| clue-service | 后端 | 业务服务层 |
| clue-vendor | 全栈 | 商户后台 |
| clue-web | 后端 | API 网关 |
| converter-clue | 后端 | 核心服务（112个实体） |

---

## 模块概览

### 1. 人员管理

| 功能 | 路由 | 说明 |
|-----|------|------|
| 外部人员列表 | `/userManagement/outUserLIst` | BPO人员账号管理 |
| 内部人员管理 | `/userManagement/inUserLIst` | 内部员工账号管理 |
| 排班管理 | 子页面 | 员工班次排班 |

**核心实体**: AuthVendorUserDO、AuthInnerUserDO

### 2. 线索管理

| 功能 | 路由 | 说明 |
|-----|------|------|
| 我的线索 | `/clueManagement/myClue` | 线索全生命周期管理 |
| 线索转化 | `/clueManagement/orderClue` | 线索转订单管理 |

**核心实体**: ClueDataDO、ClueOrderDO、ClueFollowRecordDO

### 3. 系统管理

| 功能 | 路由 | 说明 |
|-----|------|------|
| 参数配置 | `/systemConfiguration` | 系统参数键值对 |
| 字典配置 | `/dictionaryManagement` | 数据字典管理 |
| 字典项配置 | 子页面 | 字典选项配置 |

**核心实体**: SysConfigDO、DictDO、DictItemDO

---

## 业务规则汇总

### 校验规则统计

| 模块 | 规则数 | 关键规则 |
|-----|-------|---------|
| 人员管理 | 9 | 账号唯一性、密码加密、主次加微号不重复 |
| 线索管理 | 15+ | 分发数量校验、状态流转、数据脱敏 |
| 系统管理 | 8 | 字典编码唯一、配置Key唯一、缓存同步 |

### 状态枚举统计

| 枚举类型 | 值 |
|---------|---|
| EnableEnum | ENABLE(1), DISABLE(0) |
| ClueDataEnum | ENABLE(正常), DISABLE(已回收) |
| DictItemStatusEnum | ENABLE(true), DISABLE(false) |
| VendorUserRoleEnum | BPO, BPO_ADMIN |

---

## 文档目录

```
05_产品需求/
├── README.md                    # 本文件
├── .prd-state.json              # 状态文件
│
├── 人员管理/
│   ├── 需求概述.md
│   ├── 功能清单.md
│   ├── 业务规则.md
│   ├── 数据流转.md
│   └── 接口清单.md
│
├── 线索管理/
│   ├── 需求概述.md
│   ├── 功能清单.md
│   ├── 业务规则.md
│   ├── 数据流转.md
│   └── 接口清单.md
│
├── 系统管理/
│   ├── 需求概述.md
│   ├── 功能清单.md
│   ├── 业务规则.md
│   ├── 数据流转.md
│   └── 接口清单.md
│
├── _业务逻辑汇总.md
└── _代码映射.md
```

---

## 生成信息

- **生成时间**: 2026-02-03
- **分析工具**: admin-prd-generator
- **前端分析**: clue-operate-frontend
- **后端分析**: clue-service, converter-clue
