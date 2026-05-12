# Large Project Preset

## 适用场景

微服务架构、多租户 SaaS 平台、大型电商平台、企业级系统、金融/支付系统、社交平台、多团队协作项目、长期维护的核心产品

## 判断标准

- 功能数量: 10+ 个
- 系统类型: 多服务/平台
- 用户规模: 大团队/大用户群
- 预期寿命: 长期维护
- 协作需求: 多人/多Agent

## 必选模块

| 能力 | 模板来源 | 生成路径 | 说明 |
|------|---------|---------|------|
| 项目说明 | templates/agents-md/large.md | AGENTS.md（根目录） | < 150 行。Large 通过链接路由到章程、架构等独立文档 |
| 项目章程 | templates/charter/project-charter.md | `{CHARTER_PATH}` | 项目章程 |
| 工作原理 | templates/architecture/working-principle.md | `{WORKING_PRINCIPLE_PATH}` | 工作原理 |
| 技术架构 | templates/architecture/technical-architecture.md | `{TECH_ARCHITECTURE_PATH}` | 技术架构 |
| 当前状态 | templates/state/current-state.md | `{CURRENT_STATE_PATH}` | 当前状态 |
| 下一步任务 | templates/state/next-tasks.md | `{NEXT_TASKS_PATH}` | 任务队列 |
| 验收标准 | templates/security/definition-of-done.md | `{DOD_PATH}` | 验收标准 |
| 安全检查 | templates/security/security-checklist.md | `{SECURITY_PATH}` | 安全检查 |
| 错误日志 | templates/learning/lessons.md | `{LESSONS_PATH}` | 错误日志 |
| 成功模式 | templates/learning/patterns.md | `{PATTERNS_PATH}` | 成功模式 |
| 术语表 | templates/learning/glossary.md | `{GLOSSARY_PATH}` | 术语表 |
| 架构决策索引 | templates/adr/adr-readme.md | `{ADR_PATH}/README.md` | ADR 索引和使用说明 |
| ADR 模板 | templates/adr/adr-template.md | `{ADR_PATH}/000X-*.md` | 单个架构决策记录 |
| 任务卡 | templates/tasks/task-card.md | `{TASKS_PATH}` | 任务卡 |
| 功能规格 | templates/specs/*.md | `{SPECS_PATH}/{feature}/` | 功能规格 |
| 交接报告 | templates/handoff/handoff-template.md | `{HANDOFF_PATH}/{TASK_ID}-handoff.md` | 复杂任务完成后生成 |
| 项目审计 | templates/handoff/project-audit.md | `{PROJECT_AUDIT_PATH}` | 初始化、代码无文档和升级流程都生成 |

## 文件结构

```
project/
├── AGENTS.md
└── docs/
    ├── project-charter.md
    ├── working-principle.md
    ├── technical-architecture.md
    ├── current-state.md
    ├── next-tasks.md
    ├── definition-of-done.md
    ├── security-checklist.md
    ├── lessons.md
    ├── patterns.md
    ├── glossary.md
    ├── adr/
    ├── specs/
    ├── tasks/
    └── handoff/
```

**注意**：
- 新建 Large 项目默认使用普通式命名，避免部分编号、部分不编号的混合风格
- 老项目升级必须沿用已有命名风格，并把命名判断写入 `{PROJECT_AUDIT_PATH}`
- 如已有风格混合，建议统一，但必须先给出迁移计划并由用户确认
- 如果用户选择编号式命名，必须整体编号所有核心文档，并同步替换全部路径变量
- 空目录只有在对应模块实际启用后才添加 `.gitkeep`，不得创建无用途空壳
- 用户明确关闭 handoff 或多 Agent 协作时，删除 handoff 目录和角色权限节，并在审计中记录原因
- 技术架构必须先选择主体分支：web-api、cli、library-sdk、data-pipeline 或 docs-only；
  非 Web/API 项目不得保留 API、数据库、认证、部署域名等默认章节

## 快速模式默认填充策略

- 技术栈表：从各服务配置、lockfile、CI、部署配置和现有文档抽取。
- 常用命令：按服务或工作区列出真实命令；无法验证的命令写「待用户确认」。
- 架构内容：只记录可从代码、配置、部署文件或现有文档证明的事实。
- Agent 角色：使用下方角色建议生成 `{AGENT_ROLE_TABLE}`，读写范围按目录裁剪。
- 红线规则：以用户选择和上层规范为准；影响架构、安全、部署的规则必须待确认。

## 红线推荐选项

**注意**：以下为 Large 项目的推荐子集，由用户选择，不预设。完整选项以 `scripts/generation-steps.md` 的红线偏好为准。

**Never 推荐选项**：
- 提交 .env 或 secrets/
- 硬编码敏感信息
- 跳过安全检查
- 修改已确认的 ADR
- 绕过 DoD 验收
- 在无 ADR 的情况下修改架构

**AskFirst 推荐选项**：
- 删除文件
- 添加新依赖
- 修改数据库 schema
- 修改 API 接口
- 修改部署配置
- 修改安全相关代码

**Always 推荐选项**：
- 运行完整测试套件后提交
- 完成任务后更新状态文档
- 安全检查通过后标记 Done
- 新错误记录到 lessons.md
- 成功模式记录到 patterns.md
- 架构决策记录到 ADR
- 新术语添加到 glossary.md

## Agent 角色建议

| 角色 | 负责内容 |
|------|---------|
| Planner | 需求分析、任务拆分、优先级 |
| Architect | 系统设计、技术决策、ADR |
| Developer | 代码实现、测试、修复 |
| Reviewer | 代码审查、安全检查、验收 |
| Documenter | 文档更新、知识沉淀 |

生成 Large 版 AGENTS.md 时，必须把角色与读写范围写入「Agent 角色与权限」节。

## 典型项目

payment-platform、social-network、enterprise-erp、multi-tenant-saas、ecommerce-platform
