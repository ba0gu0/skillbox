<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
-->
# {FEATURE_NAME} - 任务清单

<!-- TEMPLATE META START —— spec 工作流，不进入最终文件
本文件依赖 requirements.md 和 design.md。只有验收标准和技术方案明确后，
才拆分任务并关联任务卡。
状态概览、任务列表、依赖图、验收进度和注意事项必须从 requirements.md、design.md、
现有任务队列或用户确认派生；无来源时不生成 spec-tasks.md。
如果未启用独立任务卡：
- 删除“详细任务卡”节。
- 在“任务列表”中内联范围、涉及文件、验证命令和验收标准。
- 如需链接，只链接到本文件锚点或 next-tasks 中的真实任务详情。
任务卡文件名中的 slug 必须替换为具体短名；不得在最终文件保留 `<slug>`。
TEMPLATE META END -->

## 状态概览

- **总任务数**: {TOTAL_COUNT}
- **已完成**: {DONE_COUNT}
- **进行中**: {IN_PROGRESS_COUNT}
- **待执行**: {READY_COUNT}

## 任务列表

<!-- 可变 Phase：有几个 Phase 写几个；每 Phase 内任务行数也不固定 -->

### Phase 1: {PHASE_1_NAME}

- [ ] T001: {TASK_1_NAME} - {STATUS_1}

## 任务依赖

```
T001 → T002 → T003
         ↓
       T004 → T005
```

## 详细任务卡

每个任务有独立的任务卡文件，位于 `{TASKS_PATH}`:

| 任务 | 任务卡 |
|------|--------|
| T001 | `{TASKS_PATH}/T001-short-name.md` |
| T002 | `{TASKS_PATH}/T002-short-name.md` |
| T003 | `{TASKS_PATH}/T003-short-name.md` |

## 验收进度

| 验收标准 | 状态 | 完成任务 |
|---------|------|---------|
| {ACCEPTANCE_1} | {STATUS_AC1} | {TASK_ID_1} |
| {ACCEPTANCE_2} | {STATUS_AC2} | {TASK_ID_2} |
| {ACCEPTANCE_3} | {STATUS_AC3} | {TASK_ID_3} |

## 注意事项

- {NOTE_1}
- {NOTE_2}
