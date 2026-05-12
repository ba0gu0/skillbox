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

| 层级 | 技术 | 版本 |
|------|------|------|
{TECH_STACK_TABLE}

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

## 文档索引

| 文档 | 说明 |
|------|------|
{DOCS_INDEX_TABLE}

---

## Agent 工作流

1. 读 AGENTS.md 了解项目
2. 读 `{CURRENT_STATE_PATH}` 了解当前状态
3. 读 `{NEXT_TASKS_PATH}` 选择 Ready 任务
4. 如有独立任务卡，读对应任务卡执行；否则按 `{NEXT_TASKS_PATH}` 中的任务详情执行
5. 如有规格文档，读 `{SPECS_PATH}`
6. 按 `{DOD_PATH}` 验收
7. 按 `{SECURITY_PATH}` 安全检查
8. 更新状态文档

<!-- TEMPLATE META START —— 模块裁剪规则，不进入最终文件
第 4、5 步使用“如有”条件句，可保留作为安全降级；但最终路径必须指向真实存在的模块。
如果保留条件句会产生不存在路径，则删除对应步骤。
命令块只写已验证命令；缺失的安装、开发、测试、构建、lint、类型检查命令整段删除。
代码风格示例必须来自真实代码；无代表性代码时删除代码块，只写待确认事项。
TEMPLATE META END -->

**注意**: 路径根据项目实际命名调整

---

## 一句话入口

**项目是什么**: {ONE_LINE_DESCRIPTION}

**现在在哪**: {PHASE}，见 `{CURRENT_STATE_PATH}`

**下一步做什么**: 见 `{NEXT_TASKS_PATH}`

**怎么验收**: 见 `{DOD_PATH}`

**红线不能碰**: 见上方红线部分 + `{SECURITY_PATH}`
