<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实数据
  3. 无冲突项时写"无"
-->
# 项目审计报告

> 生成日期: {DATE}
> 审计类型: {AUDIT_TYPE}

---

## 来源盘点

| 来源 | 状态 | 内容摘要 |
|------|------|---------|
| README.md | {README_STATUS} | {README_SUMMARY} |
| 项目配置文件 | {CONFIG_STATUS} | {CONFIG_SUMMARY} |
| 代码目录结构 | {CODE_STRUCTURE_STATUS} | {CODE_STRUCTURE_SUMMARY} |
| git 历史 | {GIT_STATUS} | {GIT_SUMMARY} |
| 现有 AGENTS.md / CLAUDE.md | {AGENTS_STATUS} | {AGENTS_SUMMARY} |
| docs/ 目录 | {DOCS_STATUS} | {DOCS_SUMMARY} |
| TODO / Issue 列表 | {TODO_STATUS} | {TODO_SUMMARY} |

---

## 冲突清单

| 冲突项 | 来源 A | 说法 A | 来源 B | 说法 B | 临时采用 | 理由 | 需用户确认 |
|--------|--------|--------|--------|--------|---------|------|----------|
| {CONFLICT_1} | {SOURCE_A} | {CLAIM_A} | {SOURCE_B} | {CLAIM_B} | {ADOPTED} | {RATIONALE} | {NEEDS_USER_CONFIRMATION} |

如果无冲突，写"无"。

---

## 5 能力缺口

| 能力 | 状态 | 缺口说明 |
|------|------|---------|
| 项目说明 | {PROJECT_DESCRIPTION_CAPABILITY_STATUS} | {PROJECT_DESCRIPTION_GAP} |
| 当前状态 | {CURRENT_STATE_CAPABILITY_STATUS} | {CURRENT_STATE_GAP} |
| 下一步任务 | {NEXT_TASKS_CAPABILITY_STATUS} | {NEXT_TASKS_GAP} |
| 验收标准 | {DOD_CAPABILITY_STATUS} | {DOD_GAP} |
| 红线规则 | {REDLINES_CAPABILITY_STATUS} | {REDLINES_GAP} |

---

## 命名风格检测

- 检测到的命名风格: {NAMING_STYLE}
- 示例: {EXAMPLE_FILENAME}
- 处理策略: {NAMING_STRATEGY}

---

## 待用户确认

以下项目无法从源码自动判断，需要用户确认：

1. {CONFIRMATION_ITEM_1}
2. {CONFIRMATION_ITEM_2}
3. {CONFIRMATION_ITEM_3}

如果没有，写"无"。

---

## 生成计划

将创建/更新的文件：

| 操作 | 文件 | 内容来源 |
|------|------|---------|
| {CREATE/UPDATE} | {FILE_PATH} | {CONTENT_SOURCE} |
| {CREATE/UPDATE} | {FILE_PATH} | {CONTENT_SOURCE} |

**原则**：
- 不静默覆盖已有文件；需要修改时先出示 diff 草案
- 保留已有命名风格
- 从真实内容抽取，不套空模板

<!-- TEMPLATE META START —— 变量和枚举规则，不进入最终文件
状态变量允许值：有效、可能过期、不存在、混乱、无 git 仓库、待用户确认。
能力状态允许值：完备、部分完备、缺失。
`{AUDIT_TYPE}` 允许值：快速初始化、代码无文档、老项目升级、文档重建。
`{NAMING_STYLE}` 允许值：普通式、编号式、混合式、自定义、待用户确认。
`{NAMING_STRATEGY}` 允许值：保留已有、建议迁移、待用户确认。
`{NEEDS_USER_CONFIRMATION}` 允许值：需要、不需要。
无冲突、无待确认或无生成计划时，删除表格示例行并写“无”。
所有摘要、缺口和计划必须来自 README、配置、代码结构、git、docs、TODO/Issue、
上层规则或用户确认；无来源时写入待确认项，不猜测。
TEMPLATE META END -->
