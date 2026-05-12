<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块及所有 TEMPLATE META 标记块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
  3. 替换所有 [待填充: ...] 标记为真实内容
  4. 最终文件不得残留任何 {VAR}、[待填充: ...] 标记或 HTML 注释
-->
# {CURRENT_STATE_TITLE}

> 更新时间: {DATE}
> 更新原因: {UPDATE_REASON}

---

<!-- TEMPLATE META START —— 本段为模板说明，不进入最终文件
## 使用说明

本文档由 Agent 生成并维护。内容必须从真实来源抽取：

| 部分 | 抽取来源 |
|------|---------|
| 当前阶段 | README.md 或用户确认 |
| 已完成 | `git log --oneline -10` |
| 进行中 | 用户确认或现有 TODO |
| 未完成 | TODO.md / ISSUE / 用户确认 |
| 风险 | 用户确认或代码分析 |

**禁止**：生成空泛的占位符内容。
TEMPLATE META END -->

---

## 当前阶段

{PHASE_DESCRIPTION}

**判断依据**：{PHASE_EVIDENCE}

<!-- TEMPLATE META START —— 阶段值域，不进入最终文件
`{PHASE}` 只能取 generation-steps.md 中定义的项目阶段值。
`{PHASE_DESCRIPTION}` 用 1-3 句话说明当前生命周期阶段和主要工作状态。
`{PHASE_EVIDENCE}` 必须列出 README、git、代码结构、用户确认或审计报告等依据。
生成最终文档时只保留当前阶段和真实判断依据。
TEMPLATE META END -->

---

## 已完成

{COMPLETED_WORK_LIST}

格式示例：`### 2024-01-15 - 用户认证功能`，下面列出真实完成项和验证结果。

---

## 进行中

{IN_PROGRESS_LIST}

格式示例：`- **用户授权功能** - In Progress - @developer`，下面列出当前进展和预计解除/完成时间。

---

## 未完成

### P0（必须）

{P0_TASKS}

### P1（重要）

{P1_TASKS}

### P2（可选）

{P2_TASKS}

---

## 当前风险

| 风险 | 等级 | 状态 | 说明 |
|------|------|------|------|
| {RISK_ITEM} | 高/中/低 | 待处理/已缓解 | {RISK_DESCRIPTION} |

如无风险，写「当前无明显风险」。

---

## 推荐下一步

{RECOMMENDED_NEXT_STEP}

<!-- TEMPLATE META START —— 推荐下一步生成规则，不进入最终文件
按模块生成本节：
- 无任务卡/无 specs：只写“选择上方 Ready 状态任务，按 `{DOD_PATH}` 验收，完成后更新本文档”。
- 有任务卡：可写任务卡路径 `{TASKS_PATH}/{TASK_FILE}`。
- 有 specs：可写规格路径 `{SPECS_PATH}/{FEATURE_NAME}/`。
- `{RECOMMENDED_NEXT_STEP}` 必须包含完整执行说明；不要在变量后再保留第二套固定步骤。
未启用对应模块时，不得在最终文件中出现其路径。
TEMPLATE META END -->

---

<!-- TEMPLATE META START —— 本段为模板说明，不进入最终文件
## 路径变量

本模板使用以下路径变量，生成时替换为实际路径：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `{TASKS_PATH}` | 任务卡目录 | docs/tasks |
| `{SPECS_PATH}` | 规格文档目录 | docs/specs |
| `{DOD_PATH}` | 验收标准文档 | docs/definition-of-done.md |

局部变量来源：

| 变量 | 来源 | 裁剪规则 |
|------|------|----------|
| `{COMPLETED_WORK_LIST}` | git log、发布记录、用户确认 | 无来源写“暂无可确认完成项” |
| `{IN_PROGRESS_LIST}` | TODO、issue、用户确认 | 无来源写“暂无进行中任务” |
| `{P0_TASKS}`/`{P1_TASKS}`/`{P2_TASKS}` | TODO、issue、代码缺口、用户确认 | 无任务时删除对应优先级小节 |
| `{RECOMMENDED_NEXT_STEP}` | 任务队列和依赖关系 | 无 Ready 任务时写阻塞或待确认原因 |
| `{TASK_FILE}`/`{FEATURE_NAME}` | 启用任务卡/specs 后生成 | 只允许在 `{RECOMMENDED_NEXT_STEP}` 内部使用，未启用对应模块时整句删除 |
TEMPLATE META END -->
