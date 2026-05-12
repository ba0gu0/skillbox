<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
-->
# 工作原理

> 最后更新: {DATE}

<!-- TEMPLATE META START —— 文档分工，不进入最终文件
本文件只描述动态行为：核心流程、关键机制、数据如何流转、边界条件如何处理。
静态结构、组件清单、技术栈和部署拓扑写入 technical-architecture.md，不在本文件重复。
`{OVERVIEW}`、流程、机制、数据流、边界条件、外部系统和注意事项必须来自源码、
配置、运行流程、现有文档或用户确认。
无真实来源的流程、机制、外部系统或注意事项整节删除；不得用示例步骤补齐。
纯文档项目改写为信息生产、审核、发布和回滚流程；不得保留代码运行假设。
TEMPLATE META END -->

## 概述

{OVERVIEW}

这个系统是如何工作的？核心流程是什么？

## 核心流程

### 主流程

```
{MAIN_FLOW_DIAGRAM}
```

### 流程说明

1. **{STEP_1_NAME}**
   - 输入: {STEP_1_INPUT}
   - 处理: {STEP_1_PROCESS}
   - 输出: {STEP_1_OUTPUT}

2. **{STEP_2_NAME}**
   - 输入: {STEP_2_INPUT}
   - 处理: {STEP_2_PROCESS}
   - 输出: {STEP_2_OUTPUT}

## 关键机制

### {MECHANISM_1_NAME}

{DESCRIPTION_1}

```
{CODE_OR_DIAGRAM_1}
```

### {MECHANISM_2_NAME}

{DESCRIPTION_2}

## 数据流

```
{DATA_FLOW}
```

## 边界条件

| 条件 | 处理方式 |
|------|---------|
| {CONDITION_1} | {HANDLING_1} |
| {CONDITION_2} | {HANDLING_2} |

## 与外部系统交互

| 系统 | 交互方式 | 说明 |
|------|---------|------|
| {EXTERNAL_SYSTEM_1} | {INTERACTION_METHOD_1} | {INTERACTION_DESCRIPTION_1} |

## 注意事项

- {NOTE_1}
- {NOTE_2}

## 相关文档

- [技术架构]({TECH_ARCHITECTURE_PATH})
- [项目章程]({CHARTER_PATH})
