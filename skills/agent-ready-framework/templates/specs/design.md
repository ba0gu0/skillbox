<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
-->
# {FEATURE_NAME} - 技术设计

<!-- TEMPLATE META START —— spec 工作流，不进入最终文件
本文件依赖 requirements.md。先确认需求、范围、验收标准，再生成技术设计；
设计完成后才能进入 spec-tasks.md。
局部变量来源：
- 组件、文件、接口：来自代码结构、requirements.md、用户确认。
- API 设计：仅 HTTP/RPC/API 项目保留；CLI、库、纯文档项目删除本节或改为命令/公开接口。
- 数据模型：仅存在真实数据结构、文件格式或数据库模型时保留。
- 测试策略：来自现有测试、CI、DoD 或用户确认；无来源写入待确认事项。
未启用 ADR 时，删除“关联 ADR”节。
TEMPLATE META END -->

## 概述

{DESIGN_OVERVIEW}

## 架构

```
{ARCHITECTURE_DIAGRAM}
```

## 关键组件

### {COMPONENT_1_NAME}

- **职责**: {COMPONENT_1_RESPONSIBILITY}
- **文件**: `{COMPONENT_1_FILE}`
- **接口**: `{COMPONENT_1_INTERFACE}`

### {COMPONENT_2_NAME}

- **职责**: {COMPONENT_2_RESPONSIBILITY}
- **文件**: `{COMPONENT_2_FILE}`
- **接口**: `{COMPONENT_2_INTERFACE}`

## 数据模型

```
{DATA_MODEL}
```

## 接口设计

### {API_1_NAME}

```
{API_1_SPEC}
```

### {API_2_NAME}

```
{API_2_SPEC}
```

## 错误处理

| 错误场景 | 处理方式 | 用户提示 |
|---------|---------|---------|
| {ERROR_SCENARIO_1} | {ERROR_HANDLING_1} | {ERROR_MESSAGE_1} |
| {ERROR_SCENARIO_2} | {ERROR_HANDLING_2} | {ERROR_MESSAGE_2} |

## 安全考虑

- {SECURITY_CONSIDERATION_1}
- {SECURITY_CONSIDERATION_2}
- {SECURITY_CONSIDERATION_3}

## 性能考虑

- {PERFORMANCE_CONSIDERATION_1}
- {PERFORMANCE_CONSIDERATION_2}

## 测试策略

- 单元测试: {UNIT_TEST_STRATEGY}
- 集成测试: {INTEGRATION_TEST_STRATEGY}
- E2E 测试: {E2E_TEST_STRATEGY}

## 关联 ADR

- 000X: {ADR_TITLE} - `{ADR_PATH}/000X-short-title.md`

<!-- TEMPLATE META START —— ADR 链接规则，不进入最终文件
未启用 ADR 或本设计不涉及架构决策时删除本节。
启用 ADR 时只链接真实 ADR 文件；不得在最终链接中保留 `*` 通配符。
真实文件名必须替换 `short-title` 示例文本。
TEMPLATE META END -->
