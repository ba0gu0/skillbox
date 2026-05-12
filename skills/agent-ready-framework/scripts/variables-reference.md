# 变量处理参考

> `generation-steps.md` 负责流程；本文维护跨模板共享变量和输出规则。

## 全局变量与派生变量表

目录变量默认不带尾部 `/`；使用时写成 `{DIR_VAR}/file.md`。
本表只维护跨模板共享变量；单个模板内部变量由该模板的 `TEMPLATE META` 说明。

| 变量 | 适用规模 | 说明 | 默认值 |
|------|---------|------|--------|
| `{PROJECT_ROOT}` | 全部 | 项目根目录 | 当前工作目录 |
| `{MODULE_ROOT}` | monorepo | 子模块根目录 | workspace/package/module 目录 |
| `{DATE}` | 全部 | 文档日期 | `YYYY-MM-DD`，使用生成当天日期 |
| `{PROJECT_NAME}` | 全部 | 项目名称 | package.json name / go.mod module / README 标题 / 用户回答 |
| `{ONE_LINE_DESCRIPTION}` | 全部 | 一句话描述 | README 摘要 / package metadata / 用户回答 |
| `{CODE_STYLE_DESCRIPTION}` | Medium/Large | 代码风格说明 | lint/formatter 配置、代表性代码、用户确认 |
| `{CODE_SNIPPET_EXAMPLE}` | Medium/Large | 简短代码风格示例 | 代表性代码片段，建议 10-20 行 |
| `{LANGUAGE}` | Medium/Large | 代码块语言标识 | 从 AGENTS 所在模块的主要语言抽取；纯文档项目删除代码块 |
| `{PROJECT_STRUCTURE}` | Medium/Large | 项目结构摘要 | 最多 4 层，排除依赖、构建产物、缓存和 VCS 目录 |
| `{KEY_FILES_TABLE}` | Large | 关键文件表格行 | 只列真实关键文件 |
| `{CURRENT_STATE_TITLE}` | 全部 | 当前状态文档标题 | 当前状态 |
| `{PHASE}` | 全部 | 当前阶段 | 初始化阶段 / 开发阶段 / 迭代阶段 / 维护阶段，可附加活跃/低频标签 |
| `{STATUS_RULES_SUMMARY}` | Medium/Large | 派生变量：状态表 + 流转规则 | 从 rules-reference.md 抽取 |
| `{AGENT_ROLE_TABLE}` | Large | 派生变量：角色、主要职责、读写范围三列表格行 | 从 large preset 抽取 |
| `{FORBIDDEN_FILES}` | 全部 | 工具链约束：禁止创建的文件 | 从上层规范和项目约定抽取 |
| `{FORBIDDEN_OPERATIONS}` | 全部 | 工具链约束：禁止执行的操作 | 从上层规范和用户红线抽取 |
| `{RECOMMENDED_ALTERNATIVES}` | 全部 | 工具链约束：推荐替代方式 | 从上层规范和项目工具链抽取 |
| `{TECH_STACK_TABLE}` | 全部 | 技术栈表格行，3 列：层级、技术、版本 | 从配置、依赖、源码和 README 抽取 |
| `{TECH_STACK_TABLE_WITH_NOTE}` | Large | 技术栈表格行，4 列：层级、技术、版本、说明 | 从配置、依赖、源码和 README 抽取 |
| `{DOCS_INDEX_TABLE}` | 全部 | 文档索引表格行 | 只列出实际存在或本次生成的文档 |
| `{NEVER_RULES}` | 全部 | Never 红线列表 | 从用户选择、上层规范和项目规则抽取 |
| `{ASK_FIRST_RULES}` | 全部 | Ask First 红线列表 | 从用户选择、上层规范和项目规则抽取 |
| `{ALWAYS_RULES}` | 全部 | Always 规则列表 | 从用户选择、上层规范和项目规则抽取 |
| `{INSTALL_CMD}` | Medium/Large | 安装命令 | 从项目脚本、文档、CI 或用户确认抽取 |
| `{DEV_CMD}` | 全部 | 开发命令 | 从项目脚本、文档、CI 或用户确认抽取 |
| `{TEST_CMD}` | 全部 | 测试命令 | 从项目脚本、文档、CI 或用户确认抽取 |
| `{BUILD_CMD}` | Medium/Large | 构建命令 | 从项目脚本、文档、CI 或用户确认抽取 |
| `{LINT_CMD}` | 全部 | 检查命令 | 从项目脚本、文档、CI 或用户确认抽取 |
| `{TYPECHECK_CMD}` | Medium/Large | 类型检查命令 | 从项目脚本、文档、CI 或用户确认抽取 |
| `{CURRENT_STATE_PATH}` | 全部 | 当前状态文档 | docs/current-state.md |
| `{NEXT_TASKS_PATH}` | Medium/Large | 任务队列文档 | docs/next-tasks.md |
| `{DOD_PATH}` | 全部 | 验收标准文档 | docs/definition-of-done.md |
| `{SECURITY_PATH}` | 全部 | 安全检查文档 | docs/security-checklist.md |
| `{TASKS_PATH}` | Medium/Large 可选 | 任务卡目录 | docs/tasks |
| `{SPECS_PATH}` | Medium 可选/Large | 规格文档目录 | docs/specs |
| `{ADR_PATH}` | Medium 可选/Large | ADR 目录 | docs/adr |
| `{LESSONS_PATH}` | Medium/Large 可选 | 错误日志 | docs/lessons.md |
| `{PATTERNS_PATH}` | Medium/Large 可选 | 成功模式 | docs/patterns.md |
| `{GLOSSARY_PATH}` | Large 可选 | 术语表 | docs/glossary.md |
| `{HANDOFF_PATH}` | Medium 可选/Large | 交接报告目录 | docs/handoff |
| `{PROJECT_AUDIT_PATH}` | 全部 | 项目审计报告；快速模式、代码无文档和升级流程使用 | docs/project-audit.md |
| `{CHARTER_PATH}` | Large | 项目章程 | docs/project-charter.md |
| `{WORKING_PRINCIPLE_PATH}` | Large | 工作原理 | docs/working-principle.md |
| `{TECH_ARCHITECTURE_PATH}` | Large | 技术架构 | docs/technical-architecture.md |

## 输出规则

- 默认路径使用 `docs/` 前缀；如项目已有 documentation/、wiki/、spec/ 等目录，
  生成前必须替换所有路径变量，不能混用默认路径和既有路径。
- `{PHASE}` 描述项目生命周期，不描述单个任务状态。
- `{STATUS_RULES_SUMMARY}` 输出一个 Markdown 状态表，后接 2-3 条流转规则。
- `{AGENT_ROLE_TABLE}` 只输出表格行，列顺序必须是：角色、主要职责、读写范围。
- 命令变量必须可追溯到项目脚本、Makefile/Taskfile、CI、README 或用户确认；
  无法验证时写「待用户确认」，不要放进必须执行的命令块。
- 表格行变量不是固定行数；没有真实行时整表删除或写明确的“暂无”文本。
- 复合变量必须说明列顺序、分隔符和是否包含表头。
- 路径变量必须先统一解析，再写入所有模板；不得混用默认路径和项目既有路径。
- `✅/⚠️/❌`、`是/否`、`高/中/低` 等枚举值也视为变量；必须在 META 中定义
  允许值和来源，最终文件只能保留单一真实取值。
- `<short-title>`、`<slug>`、`<...>` 只允许出现在模板说明中；最终文件必须替换成
  具体文本，或改写成不带尖括号的模式说明。

## 保留已有命名

如果项目已有不同命名风格：

```text
docs/12-current-project-state.md -> {CURRENT_STATE_PATH}
docs/13-next-tasks.md -> {NEXT_TASKS_PATH}
CLAUDE.md -> 保留；如需 AGENTS.md，生成路由文件或合并计划
```

CLAUDE.md 与 AGENTS.md 共存策略：

1. 路由模式：AGENTS.md 只做 Agent 入口，详细规则继续指向 CLAUDE.md。
2. 迁移模式：将 CLAUDE.md 内容按 5 能力重组进 AGENTS.md。
3. 多入口模式：如存在 CLINE.md、CURSOR.md 等文件，先盘点用途。

默认先给出方案，不静默迁移或删除任何入口文件。
红线冲突时，优先级为：用户确认的 `{SECURITY_PATH}` > CLAUDE.md > 上层规范；
冲突必须写入 `{PROJECT_AUDIT_PATH}`。
