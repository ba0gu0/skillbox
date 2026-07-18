<!--
TEMPLATE:
  仅在任务需独立领取、跨会话执行或并行协作时使用。
  生成前读取 references/task-state.md；最终文件删除本注释和变量。
-->
# {TASK_ID}：{TASK_TITLE}

- 状态：{TASK_STATUS}
- 优先级：{PRIORITY}
- 负责人：{OWNER}
- 依赖：{DEPENDENCIES}
- 来源：{SOURCE_LINKS}

## 目标

{GOAL}

## 范围边界

### 做什么

{IN_SCOPE_ITEMS}

### 不做什么

{OUT_OF_SCOPE_ITEMS}

## 预期改动

| 区域或文件 | 计划操作 | 依据 |
|------------|----------|------|
{CHANGE_ROWS}

## 验收标准

{ACCEPTANCE_CRITERIA}

## 验证

| 检查 | 命令或方法 | 来源 | 当前结果 |
|------|------------|------|----------|
{VALIDATION_ROWS}

## 进展与阻塞

{PROGRESS_AND_BLOCKERS}

## 完成写回

{WRITE_BACK_TARGETS}

状态只在本任务权威记录中维护；
其他队列或状态文件只保留索引和必要摘要。
