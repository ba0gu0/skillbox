<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
  3. 任务队列中的路径使用 {TASKS_PATH} 变量，根据项目实际路径替换
-->
# 下一步任务

> 更新时间: {DATE}

## 任务队列

<!-- 可变行：有几个任务写几行，无 Ready 任务则本表不生成行，写「暂无 Ready 任务」 -->
| ID | 任务 | 状态 | 优先级 | 任务卡 |
|----|------|------|--------|--------|
| {TASK_1_ID} | {TASK_1_NAME} | {STATUS_1} | {PRIORITY_1} | [{TASKS_PATH}/{TASK_1_FILE}]({TASKS_PATH}/{TASK_1_FILE}) |

## 状态定义

{STATUS_RULES_SUMMARY}

<!-- TEMPLATE META START —— 状态定义来源，不进入最终文件
`{STATUS_RULES_SUMMARY}` 必须从 `scripts/rules-reference.md` 的「统一状态机」抽取。
不要在模板中维护第二套状态机。
未启用任务卡模块时，将「任务卡」列改为「详情」，链接到本文件中的任务详情或规格文档。
TEMPLATE META END -->

## 优先级定义

| 优先级 | 说明 |
|------|------|
| P0 | 必须，影响核心功能 |
| P1 | 重要，影响用户体验 |
| P2 | 可选，优化改进 |

## 执行顺序

```
{EXECUTION_ORDER_DIAGRAM}
```

## 领取规则

1. **优先选择 Ready 状态的 P0 任务**
2. 领取前必须读 AGENTS.md 了解红线
3. 领取后更新状态为 In Progress
4. 完成后更新状态为 Done
5. 完成后同步更新 `{CURRENT_STATE_PATH}`
6. 如 `{LESSONS_PATH}` 或 `{PATTERNS_PATH}` 中有待提升规则，生成 P2 清理任务

<!-- TEMPLATE META START —— lessons/patterns 裁剪规则，不进入最终文件
未启用 lessons/patterns 模块时，删除第 6 条。
启用时，P2 清理任务必须包含：审查待提升规则、草拟 AGENTS.md 补充内容、
请求用户确认、更新 AGENTS.md、清理待提升列表。
TEMPLATE META END -->

## 当前阻塞

| 任务 | 阻塞原因 | 解决方案 | 预计解除时间 |
|------|---------|---------|-------------|
| {BLOCKED_TASK_ID} | {BLOCKER_REASON} | {BLOCKER_SOLUTION} | {BLOCKER_ETA} |

## 推荐执行

**优先**: {RECOMMENDED_TASK_ID} - {RECOMMENDED_TASK_NAME}

**理由**: {RECOMMENDATION_REASON}
