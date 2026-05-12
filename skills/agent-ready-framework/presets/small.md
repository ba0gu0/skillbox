# Small Project Preset

## 适用场景

CLI 工具、单文件脚本、POC 验证、学习项目、临时自动化脚本、单一功能小工具、个人博客/笔记

## 判断标准

- 功能数量: 1-3 个
- 系统类型: 单一工具/脚本
- 用户规模: 个人使用
- 预期寿命: 临时/短期
- 协作需求: 单人

## 必选模块

| 能力 | 模板来源 | 生成路径 | 说明 |
|------|---------|---------|------|
| 项目说明 | templates/agents-md/small.md | AGENTS.md（根目录） | < 100 行 |
| 当前状态 | templates/state/current-state.md | `{CURRENT_STATE_PATH}` | 当前状态+任务队列 |
| 验收标准 | templates/security/definition-of-done.md | `{DOD_PATH}` | 验收标准 |
| 安全检查 | templates/security/security-checklist.md | `{SECURITY_PATH}` | 安全检查 |

## 条件必选模块

| 条件 | 模板来源 | 生成路径 | 说明 |
|------|---------|---------|------|
| 快速模式 / 代码无文档 / 老项目升级 | templates/handoff/project-audit.md | `{PROJECT_AUDIT_PATH}` | 记录自动判断、缺失信息和待确认项 |

## 文件结构

```
project/
├── AGENTS.md
└── docs/
    ├── current-state.md
    ├── definition-of-done.md
    ├── security-checklist.md
    └── project-audit.md  # 仅快速模式、代码无文档或升级流程生成
```

**注意**: Small 项目不单独建立 next-tasks.md，任务队列在 current-state.md 中维护。
生成 current-state.md 时必须删除指向 `{TASKS_PATH}` 独立任务卡目录的句子。

## 快速模式默认填充策略

- 技术栈表：从配置文件、入口文件和 README 抽取；无来源写「待用户确认」。
- 常用命令：只填写项目已存在脚本、Makefile/Taskfile 或用户确认命令。
- 代码风格：从现有代码和格式化配置抽取；无来源写「待用户确认」。
- 红线规则：使用用户已选规则；未选择时只保留上层规范中明确存在的规则。

## 红线推荐选项

**注意**：以下为 Small 项目的推荐子集，由用户选择，不预设。完整选项以 `scripts/generation-steps.md` 的红线偏好为准。

**Never 推荐选项**：
- 提交 .env
- 硬编码敏感信息
- 跳过测试

**AskFirst 推荐选项**：
- 删除文件
- 添加新依赖

**Always 推荐选项**：
- 运行测试后提交
- 更新 current-state.md

## 典型项目

my-cli-tool、poc-oauth、learn-react、backup-script
