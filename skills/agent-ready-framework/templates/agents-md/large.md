<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
-->
# AGENTS.md - {PROJECT_NAME}

> 最后更新: {DATE} | 当前阶段: {PHASE}

## 项目概述

{PROJECT_NAME} - {ONE_LINE_DESCRIPTION}

当前阶段: {PHASE}

---

## 技术栈

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
{TECH_STACK_TABLE_WITH_NOTE}

---

## 常用命令

```bash
# 安装依赖
{INSTALL_CMD}

# 开发服务器
{DEV_CMD}

# 测试
{TEST_CMD}

# 构建
{BUILD_CMD}

# 代码检查
{LINT_CMD}

# 类型检查
{TYPECHECK_CMD}
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

## 代码风格

{CODE_STYLE_DESCRIPTION}

```{LANGUAGE}
{CODE_SNIPPET_EXAMPLE}
```

---

## 项目结构

```
{PROJECT_STRUCTURE}
```

---

## 关键文件

| 文件 | 说明 |
|------|------|
{KEY_FILES_TABLE}

---

## 文档索引

| 文档 | 说明 |
|------|------|
{DOCS_INDEX_TABLE}

---

## Agent 工作流

1. 读 AGENTS.md 了解项目
2. 读 `{CURRENT_STATE_PATH}` 了解当前状态
3. 读 `{NEXT_TASKS_PATH}` 选择 Ready 任务
4. 读对应任务卡执行
5. 读 `{SPECS_PATH}` 中的对应功能规格
6. 如涉及架构决策，查阅 `{ADR_PATH}`
7. 按 `{DOD_PATH}` 验收
8. 按 `{SECURITY_PATH}` 安全检查
9. 更新状态文档

**注意**: 路径根据项目实际命名调整

## Agent 角色与权限

| 角色 | 主要职责 | 读写范围 |
|------|---------|---------|
{AGENT_ROLE_TABLE}

<!-- TEMPLATE META START —— Large 角色生成规则，不进入最终文件
`{AGENT_ROLE_TABLE}` 来自 `presets/large.md` 的 Agent 角色建议，并结合项目实际权限裁剪。
如果用户未启用多 Agent 协作，删除本节。
多 Agent 协作由 generation-steps.md 文档偏好询问决定；未询问到明确答案时按未启用处理。
命令块只写已验证命令；未启用任务卡、specs 或 ADR 时，删除对应工作流步骤。
非 Web/API 项目必须裁剪技术栈、关键文件、架构链接和安全检查指向，避免生成 Web/API 假设。
TEMPLATE META END -->

## 一句话入口

**项目是什么**: {ONE_LINE_DESCRIPTION}

**现在在哪**: {PHASE}，见 `{CURRENT_STATE_PATH}`

**下一步做什么**: 见 `{NEXT_TASKS_PATH}`

**怎么验收**: 见 `{DOD_PATH}`

**红线不能碰**: 见上方红线部分 + `{SECURITY_PATH}`
