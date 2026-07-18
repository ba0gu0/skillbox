<!--
TEMPLATE:
  仅在换执行者且现有任务记录不足以恢复上下文时使用。
  内容必须来自实际 diff、验证和权威任务记录；
  最终文件删除本注释和变量。
-->
# 任务交接：{TASK_REFERENCE}

> 时间：{HANDOFF_AT}
> 当前状态：{TASK_STATUS}

## 已完成

{COMPLETED_SUMMARY}

## 实际变更

| 文件 | 操作 | 说明 |
|------|------|------|
{CHANGED_FILE_ROWS}

## 验证结果

| 命令或检查 | 结果 | 证据或说明 |
|------------|------|------------|
{VALIDATION_ROWS}

未运行的验证必须单独列出原因，不得省略。

## 未完成与下一步

{REMAINING_WORK}

## 风险与阻塞

{RISKS_AND_BLOCKERS}

## 接手入口

{READ_NEXT_LINKS}

## 写回状态

{WRITE_BACK_STATUS}
