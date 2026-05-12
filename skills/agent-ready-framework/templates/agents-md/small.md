<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
-->
# AGENTS.md - {PROJECT_NAME}

> 最后更新: {DATE} | 当前阶段: {PHASE}

<!-- TEMPLATE META START —— Small 裁剪规则，不进入最终文件
命令块只写已验证命令；缺失的测试、开发或检查命令整段删除。
Small 不生成 next-tasks、任务卡、specs、handoff 链接，任务队列只指向 current-state。
纯文档项目删除代码/开发命令，保留来源校验、链接校验和发布检查。
TEMPLATE META END -->

## 项目概述

{PROJECT_NAME} - {ONE_LINE_DESCRIPTION}

## 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
{TECH_STACK_TABLE}

---

## 常用命令

```bash
# 测试
{TEST_CMD}

# 开发
{DEV_CMD}

# 代码检查
{LINT_CMD}
```

---

## 红线

> 以下红线由用户选择生成，非预设

### 🚫 Never（绝对禁止）

{NEVER_RULES}

### ⚠️ Ask First（需确认）

{ASK_FIRST_RULES}

### ✅ Always（必须执行）

{ALWAYS_RULES}

---

## 文档索引

| 文档 | 说明 |
|------|------|
{DOCS_INDEX_TABLE}

---

## Agent 工作流

1. 读 AGENTS.md 了解项目
2. 读 `{CURRENT_STATE_PATH}` 了解当前状态和任务队列
3. 选择 Ready 状态的任务执行
4. 按 `{DOD_PATH}` 验收
5. 按 `{SECURITY_PATH}` 安全检查
6. 更新 `{CURRENT_STATE_PATH}`

**注意**: Small 项目不单独建立 next-tasks.md，任务队列在 current-state.md 中维护

---

## 一句话入口

**项目是什么**: {ONE_LINE_DESCRIPTION}

**现在在哪**: {PHASE}，见 `{CURRENT_STATE_PATH}`

**下一步做什么**: 见 `{CURRENT_STATE_PATH}` 中的未完成任务

**怎么验收**: 见 `{DOD_PATH}`

**红线不能碰**: 见上方红线部分 + `{SECURITY_PATH}`
