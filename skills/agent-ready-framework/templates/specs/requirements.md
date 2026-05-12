<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块及所有 TEMPLATE META 标记块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
  3. 最终文件不得残留任何 {VAR} 标记或 HTML 注释
-->
# {FEATURE_NAME} - 需求规格

<!-- TEMPLATE META START —— spec 工作流，不进入最终文件
生成顺序：requirements.md 明确需求和验收标准 → design.md 给出技术设计 →
spec-tasks.md 拆分执行任务。不要跳过上游文档直接生成下游任务。
TEMPLATE META END -->

## 状态

{STATUS}

**状态说明**：
{STATUS_RULES_SUMMARY}

<!-- TEMPLATE META START —— 状态定义来源，不进入最终文件
`{STATUS_RULES_SUMMARY}` 必须从 `scripts/rules-reference.md` 的「统一状态机」抽取。
TEMPLATE META END -->

---

<!-- TEMPLATE META START —— 本段为模板说明，不进入最终文件
## 使用说明

本文档由 Agent 生成并维护。内容必须从真实来源抽取：

| 部分 | 抽取来源 |
|------|---------|
| 目标 | 用户需求描述 |
| 用户故事 | 用户确认 |
| 验收标准 | 用户需求 + 技术约束 |
| 范围 | 用户确认 |
| 约束 | 技术栈 + 项目限制 |

**禁止**：生成空泛的占位符内容。
TEMPLATE META END -->

---

## 目标

{FEATURE_GOAL}

## 用户故事

作为 {ROLE}，
我希望 {ACTION}，
以便 {VALUE}。

## 验收标准

<!-- 可变行：有可验证标准才生成 -->
- [ ] {ACCEPTANCE_CRITERION_1}

**验收标准必须**：
- 具体可验证，不能模糊
- 有明确的完成条件
- 可被测试覆盖

## 范围

### 包含

<!-- 可变行：有真实内容才生成 -->
- {IN_SCOPE_1}

### 不包含

- {OUT_OF_SCOPE_1}

## 约束

- {CONSTRAINT_1}
- {CONSTRAINT_2}
- {CONSTRAINT_3}

## 依赖

- 依赖任务: {DEPENDENCY_TASK}
- 依赖 ADR: {DEPENDENCY_ADR}
- 外部依赖: {DEPENDENCY_EXTERNAL}

## 相关文档

- 设计文档: {DESIGN_DOC_LINK}
- 任务清单: {TASKS_DOC_LINK}

---

## 阻塞记录

如果状态为 Blocked，记录阻塞原因：

| 日期 | 阻塞原因 | 解决方案 | 预计解除 |
|------|---------|---------|---------|
| {BLOCK_DATE} | {BLOCK_REASON} | {BLOCK_SOLUTION} | {BLOCK_ETA} |
