<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
-->
# 技术架构

> 最后更新: {DATE}

<!-- TEMPLATE META START —— 文档分工，不进入最终文件
本文件只描述静态结构：组件、技术栈、数据模型、API 边界和部署拓扑。
动态流程、关键机制、边界条件处理写入 working-principle.md，不在本文件重复。
TEMPLATE META END -->

## 架构概述

{ARCHITECTURE_OVERVIEW}

## 架构主体分支

{ARCHITECTURE_BRANCH_SUMMARY}

<!-- TEMPLATE META START —— 主体分支规则，不进入最终文件
生成前必须选择一个主体分支，并按该分支重写后续章节：
- web-api：保留组件、API、数据模型、认证、部署、监控。
- cli：改写为命令/子命令、输入输出、配置文件、文件系统边界、外部命令依赖。
- library-sdk：改写为公开 API、核心类型、扩展点、兼容性边界、发布产物。
- data-pipeline：改写为输入源、处理阶段、输出目标、调度方式、失败重试。
- docs-only：改写为信息架构、来源、生成/发布流程、权限和链接校验。
非 web-api 分支不得保留下方 API、数据库、认证、部署域名等 Web/API 章节标题。
`{ARCHITECTURE_BRANCH_SUMMARY}` 写 1-2 句说明选择依据，来源为代码结构、配置或用户确认。
TEMPLATE META END -->

## 系统架构图

```
{ARCHITECTURE_DIAGRAM}
```

## 核心组件

### {COMPONENT_1_NAME}

- **职责**: {COMPONENT_1_RESPONSIBILITY}
- **技术**: {COMPONENT_1_TECH}
- **文件**: `{COMPONENT_1_FILE}`

### {COMPONENT_2_NAME}

- **职责**: {COMPONENT_2_RESPONSIBILITY}
- **技术**: {COMPONENT_2_TECH}
- **文件**: `{COMPONENT_2_FILE}`

## 技术栈

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
{TECH_STACK_TABLE_WITH_NOTE}

<!-- TEMPLATE META START —— 技术栈裁剪规则，不进入最终文件
`{TECH_STACK_TABLE_WITH_NOTE}` 使用 `层级 | 技术 | 版本 | 说明` 四列。
只写项目真实存在的层级；CLI、库、数据管道等项目不得保留前端/后端/数据库/缓存假设。

非 Web 项目替代结构：
- CLI：命令/子命令表、输入输出、配置文件、文件系统交互、外部命令依赖。
- 库/SDK：公开 API、核心类型、扩展点、兼容性边界、发布产物。
- 数据管道：输入源、处理阶段、输出目标、调度方式、失败重试。
- 纯文档：信息架构、生成/发布流程、来源和校验规则。
生成前必须选择一个主体分支：
- web-api：保留 API、数据模型、认证、部署、监控。
- cli：删除 API、数据库、认证授权；改写为命令、输入输出、配置和文件边界。
- library-sdk：删除部署环境；改写为公开 API、核心类型、兼容性和发布产物。
- data-pipeline：改写为输入源、处理阶段、输出、调度和失败重试。
- docs-only：改写为信息架构、来源、生成流程、发布权限和链接校验。
TEMPLATE META END -->

## 数据流

```
{DATA_FLOW_DIAGRAM}
```

## API 设计

### 内部 API

| 端点 | 方法 | 说明 |
|------|------|------|
| `{ENDPOINT_1}` | {METHOD_1} | {ENDPOINT_1_DESCRIPTION} |
| `{ENDPOINT_2}` | {METHOD_2} | {ENDPOINT_2_DESCRIPTION} |

### 外部 API 依赖

| 服务 | 用途 | 文档 |
|------|------|------|
| {EXTERNAL_SERVICE_1} | {EXTERNAL_SERVICE_1_USAGE} | {EXTERNAL_SERVICE_1_DOC} |

## 数据模型

### 核心实体

```
{ENTITY_DIAGRAM}
```

### 数据库表

| 表名 | 说明 | 主要字段 |
|------|------|---------|
| {TABLE_1} | {TABLE_1_DESCRIPTION} | {TABLE_1_FIELDS} |

## 安全架构

### 认证授权

- **认证方式**: {AUTH_METHOD}
- **授权模型**: {AUTHZ_MODEL}

### 数据安全

- 敏感数据加密: {ENCRYPTION}
- 传输安全: {TLS}

## 部署架构

```
{DEPLOYMENT_DIAGRAM}
```

### 环境

| 环境 | 域名 | 说明 |
|------|------|------|
| 开发 | {DEV_DOMAIN} | 开发环境 |
| 测试 | {TEST_DOMAIN} | 测试环境 |
| 生产 | {PROD_DOMAIN} | 生产环境 |

## 监控与告警

| 指标 | 阈值 | 告警方式 |
|------|------|---------|
| {METRIC_1} | {THRESHOLD_1} | {ALERT_METHOD_1} |

## 相关 ADR

- 0001: {ADR_TITLE} - `{ADR_PATH}/0001-select-runtime.md`

<!-- TEMPLATE META START —— ADR 链接规则，不进入最终文件
未启用 ADR 时删除本节。
启用 ADR 时只链接真实文件，例如 `{ADR_PATH}/0001-select-runtime.md`。
不得在最终链接中保留 `*` 通配符或 `<short-title>` 伪占位。
TEMPLATE META END -->

## 相关文档

- [项目章程]({CHARTER_PATH})
- [工作原理]({WORKING_PRINCIPLE_PATH})
