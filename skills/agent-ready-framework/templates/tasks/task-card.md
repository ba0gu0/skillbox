<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块及所有 TEMPLATE META 标记块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
  3. 替换所有 [待填充: ...] 标记为真实内容
  4. 最终文件不得残留任何 {VAR}、[待填充: ...] 标记或 HTML 注释
-->
# {TASK_ID}: {TASK_TITLE}

## 元信息

| 属性 | 值 |
|------|-----|
| 状态 | {STATUS} |
| 优先级 | {PRIORITY} |
| 依赖 | {DEPENDENCIES} |
| 预估 | {ESTIMATION} |
| 规格 | [{SPECS_PATH}/{FEATURE}/]({SPECS_PATH}/{FEATURE}/) |

---

<!-- TEMPLATE META START —— 本段为模板说明，不进入最终文件
## 使用说明

本文档由 Agent 生成并维护。内容必须从真实来源抽取：

| 部分 | 抽取来源 |
|------|---------|
| 目标 | 规格文档或用户需求 |
| 涉及文件 | 代码分析 |
| 实现步骤 | 技术设计 |
| 验收标准 | 规格文档 |
| 验证命令 | 项目脚本、Makefile/Taskfile、CI、README 或用户确认 |

**禁止**：生成空泛的占位符内容。
命令变量只允许写已验证命令；待确认命令放入正文“待确认事项”，不得进入 bash 代码块。
未启用 specs 时，删除元信息中的“规格”行和 spec tasks 写回行。
TEMPLATE META END -->

---

## 目标

{TASK_GOAL}

## 背景

{TASK_CONTEXT}

## 涉及文件

<!-- 可变行：有几个文件写几个 -->
| 文件 | 操作 | 说明 |
|------|------|------|
| `{FILE_PATH_1}` | {OPERATION_1} | {DESCRIPTION_1} |

## 实现步骤

<!-- 可变行：有几个步骤写几个 -->
1. {STEP_1}

## 范围边界

### 做什么

<!-- 可变行：有真实内容才生成 -->
- {IN_SCOPE_1}

### 不做什么

<!-- 可变行：有真实内容才生成，无则写「无明确排除项」 -->
- {OUT_OF_SCOPE_1}

## 验收标准

<!-- 可变行：有可验证标准才生成 -->
- [ ] {ACCEPTANCE_CRITERION_1}
- [ ] 运行 `{TEST_CMD}` 通过

## 验证命令

```bash
# 测试
{TEST_CMD}

# 构建
{BUILD_CMD}

# 代码检查
{LINT_CMD}
```

## 安全检查

- [ ] 无敏感信息泄露
- [ ] 无安全漏洞引入
- [ ] 符合 `{SECURITY_PATH}`

---

## 状态写回位置

完成任务后，必须更新以下位置：

| 位置 | 更新内容 | 路径 |
|------|---------|------|
| 任务卡 | 本任务状态 → Done | `{TASKS_PATH}/{TASK_ID}-*.md` |
| current-state | 已完成列表、进行中→移除 | `{CURRENT_STATE_PATH}` |
| next-tasks | 如存在独立任务队列，任务状态 → Done | `{NEXT_TASKS_PATH}` |
| spec tasks | 如存在规格任务，checklist 标记完成 | `{SPECS_PATH}/{FEATURE}/tasks.md` |

**可选更新**（如有相关内容）：

| 条件 | 更新位置 |
|------|---------|
| 有新错误 | `{LESSONS_PATH}` |
| 有成功模式 | `{PATTERNS_PATH}` |
| 有架构决策 | `{ADR_PATH}/000X-*.md` |
| 有新术语 | `{GLOSSARY_PATH}` |

## 完成后检查清单

必做：
- [ ] 本任务卡状态更新为 Done
- [ ] `{CURRENT_STATE_PATH}` 已完成列表已更新
- [ ] 如存在 `{NEXT_TASKS_PATH}`，任务状态已更新

可选（如有）：
- [ ] `{LESSONS_PATH}` 新错误已记录
- [ ] `{PATTERNS_PATH}` 成功模式已记录
- [ ] `{ADR_PATH}` 新 ADR 已创建
- [ ] `{HANDOFF_PATH}` 交接报告已生成（按 preset 和用户选择）

<!-- TEMPLATE META START —— 模块裁剪规则，不进入最终文件
Small 项目默认不生成任务卡；如用户启用任务卡，删除 handoff 检查项。
Medium 项目只有用户选择 handoff 时才保留 handoff 检查项。
Large 项目默认保留 handoff 检查项。
未启用 ADR、lessons、patterns、glossary、handoff 时，删除对应可选更新行。
ADR 路径模式是文本说明，不得生成成 Markdown 链接；真实 ADR 必须使用具体文件名。
TEMPLATE META END -->

---

## 阻塞记录

如果状态为 Blocked，记录阻塞原因：

| 日期 | 阻塞原因 | 解决方案 | 预计解除 |
|------|---------|---------|---------|
| {BLOCK_DATE} | {BLOCK_REASON} | {BLOCK_SOLUTION} | {BLOCK_ETA} |

---

## 备注

{NOTES}
