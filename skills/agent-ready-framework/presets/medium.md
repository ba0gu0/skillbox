# Medium Project Preset

## 适用场景

单体 Web 应用、REST API 服务、小型电商网站、企业内部系统、个人 SaaS 产品、移动 App 后端、博客平台、管理后台

## 判断标准

- 功能数量: 3-10 个
- 系统类型: 单体应用
- 用户规模: 小团队/小用户群
- 预期寿命: 中长期
- 协作需求: 1-3人

## 必选模块

| 能力 | 模板来源 | 生成路径 | 说明 |
|------|---------|---------|------|
| 项目说明 | templates/agents-md/medium.md | AGENTS.md（根目录） | < 150 行 |
| 当前状态 | templates/state/current-state.md | `{CURRENT_STATE_PATH}` | 当前状态 |
| 下一步任务 | templates/state/next-tasks.md | `{NEXT_TASKS_PATH}` | 任务队列 |
| 验收标准 | templates/security/definition-of-done.md | `{DOD_PATH}` | 验收标准 |
| 安全检查 | templates/security/security-checklist.md | `{SECURITY_PATH}` | 安全检查 |

## 默认推荐模块（需用户确认，可关闭）

| 能力 | 模板来源 | 生成路径 | 说明 |
|------|---------|---------|------|
| 错误日志 | templates/learning/lessons.md | `{LESSONS_PATH}` | 用户确认启用后生成 |
| 成功模式 | templates/learning/patterns.md | `{PATTERNS_PATH}` | 用户确认启用后生成 |
| 架构决策索引 | templates/adr/adr-readme.md | `{ADR_PATH}/README.md` | 用户确认启用 ADR 后生成 |
| ADR 模板 | templates/adr/adr-template.md | `{ADR_PATH}/NNNN-short-title.md` | 用户确认启用 ADR 后按需创建 |
| 任务卡 | templates/tasks/task-card.md | `{TASKS_PATH}` | 用户确认独立任务卡后生成 |

## 可选模块

| 能力 | 模板来源 | 生成路径 | 说明 |
|------|---------|---------|------|
| 功能规格 | templates/specs/*.md | `{SPECS_PATH}/{feature}/` | 按需创建 |
| 交接报告 | templates/handoff/handoff-template.md | `{HANDOFF_PATH}/{TASK_ID}-handoff.md` | 用户选择 handoff 时生成 |
| 项目审计 | templates/handoff/project-audit.md | `{PROJECT_AUDIT_PATH}` | 快速模式、代码无文档或升级流程生成 |

## 必选文件结构

```
project/
├── AGENTS.md
└── docs/
    ├── current-state.md
    ├── next-tasks.md
    ├── definition-of-done.md
    └── security-checklist.md
```

## 启用模块后追加结构

| 模块 | 追加路径 | 生成条件 |
|------|----------|----------|
| lessons/patterns | docs/lessons.md, docs/patterns.md | 用户选择启用 |
| ADR | docs/adr/README.md | 用户选择启用 ADR |
| specs | docs/specs/{feature}/ | 按需或必须生成 specs |
| tasks | docs/tasks/ | 用户选择独立任务卡 |
| handoff | docs/handoff/ | 用户选择 handoff |

空目录只有在用户确认启用对应模块后才添加 `.gitkeep`，不得为了结构完整创建未启用模块。

## 快速模式默认填充策略

- 技术栈表：从配置文件、lockfile、CI、入口文件和 README 抽取。
- 常用命令：优先使用项目脚本、Makefile/Taskfile、CI 命令；无来源写「待用户确认」。
- 代码风格：从 lint/formatter/tsconfig/ruff 等配置抽取；无来源写「待用户确认」。
- 文档索引：只列出本次实际生成或项目已存在的文档。
- 红线规则：合并用户选择、上层规范和项目已有规则；冲突项列为待确认。

## 红线推荐选项

**注意**：以下为 Medium 项目的推荐子集，由用户选择，不预设。完整选项以 `scripts/generation-steps.md` 的红线偏好为准。

**Never 推荐选项**：
- 提交 .env 或 secrets/
- 硬编码敏感信息
- 跳过安全检查
- 修改已确认的 ADR

**AskFirst 推荐选项**：
- 删除文件
- 添加新依赖
- 修改数据库 schema
- 修改 API 接口

**Always 推荐选项**：
- 运行测试后提交
- 完成任务后更新状态文档
- 安全检查通过后标记 Done
- 新错误记录到 lessons.md

## 典型项目

blog-platform、todo-api、shop-backend、admin-panel、mobile-backend
