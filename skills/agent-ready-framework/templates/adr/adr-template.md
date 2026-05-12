<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
-->
# {ADR_NUMBER}: {DECISION_TITLE}

## 状态

{STATUS}

<!-- TEMPLATE META START —— ADR 变量来源，不进入最终文件
`{ADR_NUMBER}` 使用 4 位编号，从 `{ADR_PATH}` 中已有 NNNN-*.md 最大编号 +1 得出。
`{DECISION_TITLE}`、`{CONTEXT}`、`{DECISION}`、`{REASONING}` 来自用户确认、现有设计、
代码/配置约束或项目审计；无来源时不要创建 Accepted ADR。
`{STATUS}` 只能是 Proposed、Accepted、Deprecated、Superseded。
替代方案、影响、风险、实施和相关项无真实内容时删除对应小节或写“待用户确认”。
TEMPLATE META END -->

允许值：
- Proposed：提议中，待讨论确认
- Accepted：已确认，当前有效
- Deprecated：已过时，不再推荐
- Superseded：已被替代，参考新 ADR

## 背景

{CONTEXT}

为什么需要做这个决策？当前面临什么问题？

## 决策

{DECISION}

我们决定采用什么方案？

## 原因

{REASONING}

为什么选择这个方案？

1. {REASON_1}
2. {REASON_2}
3. {REASON_3}

## 替代方案

| 方案 | 优点 | 缺点 | 为何未选 |
|------|------|------|---------|
| {ALT_1} | {ALT_1_PROS} | {ALT_1_CONS} | {ALT_1_WHY_NOT} |
| {ALT_2} | {ALT_2_PROS} | {ALT_2_CONS} | {ALT_2_WHY_NOT} |
| {ALT_3} | {ALT_3_PROS} | {ALT_3_CONS} | {ALT_3_WHY_NOT} |

## 影响

### 正面影响

- {POSITIVE_IMPACT_1}
- {POSITIVE_IMPACT_2}

### 负面影响

- {NEGATIVE_IMPACT_1}
- {NEGATIVE_IMPACT_2}

### 风险

- {RISK_1}
- {RISK_2}

## 实施

- 影响文件: `{FILE_PATHS}`
- 迁移计划: {MIGRATION_PLAN}
- 时间线: {TIMELINE}

## 相关

- 相关 ADR: {RELATED_ADR}
- 相关任务: {RELATED_TASK}
- 相关规格: {RELATED_SPEC}

---

## 参考

- {REFERENCE_1}
- {REFERENCE_2}
