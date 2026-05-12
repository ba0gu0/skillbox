<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块及所有 TEMPLATE META 标记块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
-->
# Agent 交接报告

> 任务: {TASK_ID}
> 执行者: {AGENT_ID}
> 时间: {DATE}

---

<!-- TEMPLATE META START —— 本段为模板说明，不进入最终文件
## 使用说明

按项目规模区分：

| 规模 | 交接报告要求 |
|------|-------------|
| Small | 不需要 |
| Medium | 可选 |
| Large | 默认生成，除非用户明确关闭 |

如需生成，创建 `{HANDOFF_PATH}/{TASK_ID}-handoff.md`。
启用任务卡时，内容来自任务卡、实际 diff、验证结果和剩余风险。
未启用任务卡时，内容来自 `{NEXT_TASKS_PATH}` 或 `{CURRENT_STATE_PATH}` 的任务记录、
实际 diff、验证结果和剩余风险，并删除所有 `{TASKS_PATH}` 引用。
TEMPLATE META END -->

---

## 执行摘要

{SUMMARY}

一句话描述本次完成了什么。

---

## 变更文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `{FILE_1}` | {OPERATION_1} | {DESCRIPTION_1} |
| `{FILE_2}` | {OPERATION_2} | {DESCRIPTION_2} |

---

## 验证结果

### 测试命令

| 命令 | 结果 | 说明 |
|------|------|------|
| `{TEST_CMD}` | {TEST_RESULT} | {TEST_NOTE} |
| `{BUILD_CMD}` | {BUILD_RESULT} | {BUILD_NOTE} |

### 安全检查

- [ ] 无敏感信息泄露
- [ ] 无安全漏洞引入
- [ ] 符合 `{SECURITY_PATH}`

---

## 验收标准完成情况

| 标准 | 状态 | 说明 |
|------|------|------|
| {ACCEPTANCE_1} | {STATUS_1} | {NOTE_1} |
| {ACCEPTANCE_2} | {STATUS_2} | {NOTE_2} |

---

## 剩余风险

| 风险 | 影响 | 建议处理 |
|------|------|---------|
| {RISK_1} | {RISK_1_IMPACT} | {RISK_1_SUGGESTION} |

如果无剩余风险，写"无"。

---

## 状态更新

### 任务状态

- 本任务: {TASK_ID} → Done
- 下一个任务: {NEXT_TASK_ID} → {NEXT_TASK_STATUS}

### 已更新文档

- [ ] `{CURRENT_STATE_PATH}`
- [ ] `{NEXT_TASKS_PATH}` (如有)
- [ ] `{TASKS_PATH}/{TASK_ID}.md`
- [ ] `{SPECS_PATH}/{FEATURE}/tasks.md` (如有)
- [ ] `{LESSONS_PATH}` (如有新错误)
- [ ] `{PATTERNS_PATH}` (如有成功模式)

<!-- TEMPLATE META START —— 写回裁剪规则，不进入最终文件
未启用任务卡时删除 `{TASKS_PATH}` 行。
未启用 specs 时删除 `{SPECS_PATH}` 行。
未启用 lessons/patterns 时删除对应行。
Small 项目默认不生成 handoff。
TEMPLATE META END -->

---

## 新增规则建议

以下规则可提升到 AGENTS.md：

1. {RULE_1}
2. {RULE_2}

如果没有，写"无"。

---

## 下一步建议

{NEXT_SUGGESTION}

建议下一个执行者关注什么。

---

## 交接签名

- 执行者: {AGENT_ID}
- 验证者: {VERIFIER_ID}
- 时间: {DATE}
