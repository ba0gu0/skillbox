---
name: agent-ready-framework
description: 项目接手系统生成器。把新项目、代码无文档项目或老项目升级成任何 AI Coding Agent 都能不靠聊天历史直接接手执行的工作系统。核心建立 5 个能力：项目说明、当前状态、下一步任务、验收标准、红线规则。
triggers:
  - 初始化项目文档
  - 生成 AGENTS.md
  - 创建 Agent-Ready 文档
  - 项目文档框架
  - 升级现有文档
  - 让项目可被 agent 接手
---

# Agent-Ready Project Framework

目标：把一个项目变成任何 AI Coding Agent 都能不靠聊天历史直接接手执行的工作系统。

核心原则：skill 可以根据项目现状和架构给出推荐，但最终规则必须由用户确认。

## 5 个能力

| 问题 | 能力 | 说明 |
|------|------|------|
| 项目是什么？ | 项目说明 | 一句话定位、技术栈、核心架构 |
| 现在在哪？ | 当前状态 | 阶段、已完成、进行中、风险 |
| 下一步做什么？ | 下一步任务 | 可领取任务队列、优先级、依赖 |
| 怎么验收？ | 验收标准 | 测试命令、检查清单、完成条件 |
| 哪些红线不能碰？ | 红线规则 | 绝对禁止、需确认、必须执行 |

具体文件名由项目习惯决定，不强求固定命名。关键是这 5 个能力必须存在且真实可执行。

## 使用入口

### 新项目初始化

```
/agent-ready-framework --init
```

适用于空目录或新项目。执行 `scripts/generation-steps.md` 的「新项目生成流程」。

### 代码无文档项目

```
/agent-ready-framework --code-only
```

适用于已有代码、配置文件或脚本，但缺少 README/docs/AGENTS.md 的项目。执行 `scripts/generation-steps.md` 的「代码项目生成流程」。

### 老项目升级

```
/agent-ready-framework --upgrade
```

适用于已有代码和文档的项目。执行 `scripts/generation-steps.md` 的「老项目升级流程」；如果盘点后发现是代码无文档项目，自动切换到 `--code-only` 流程。

### 手动模式

```
/agent-ready-framework --manual
```

完全手动选择所有配置项，但仍必须遵守 `scripts/rules-reference.md` 的验证与不静默覆盖规则。

## 执行规则

- 具体执行流程和偏好选项在 `scripts/generation-steps.md` 中维护。
- 路径变量、复合变量和命令变量在 `scripts/variables-reference.md` 中维护。
- 老项目升级细节在 `scripts/upgrade-reference.md` 中维护。
- 状态机、模板裁剪、最终验证和覆盖边界只在 `scripts/rules-reference.md` 中维护。
- 本文件只定义定位、入口和高层原则，避免与执行清单重复。
- 生成前先读 `scripts/generation-steps.md`、`scripts/variables-reference.md`
  和 `scripts/rules-reference.md`，再根据项目规模读取对应 preset。
- 执行 `--upgrade` 时还必须读取 `scripts/upgrade-reference.md`。
- 升级老项目时不静默覆盖已有文件；需要修改时先出示合并计划或 diff 草案。
- 缺少真实信息时，不填占位符；写入「待用户确认」或删去无来源章节。

## 规模预设

| 规模 | 适用项目 | 预设 |
|------|----------|------|
| Small | CLI、脚本、POC、单一功能工具 | `presets/small.md` |
| Medium | 单体应用、API 服务、管理后台、小型网站 | `presets/medium.md` |
| Large | 微服务、多租户平台、企业级系统 | `presets/large.md` |

## 模板资源

templates/ 目录中的文件是模板或参考材料，不是直接可用的最终文档。生成到项目里的文档必须：

1. 移除所有 `<!-- TEMPLATE ... -->` 和 `<!-- TEMPLATE META ... -->` 注释块。
2. 替换所有 `{UPPER_CASE_VAR}`、中文花括号变量、`[待填充]`、`xxx/XXX`。
3. 根据真实来源裁剪章节，不为了完整感生编内容。
4. 使用 `scripts/rules-reference.md` 中的 `FILES` 规则完成最终扫描。

## 核心红线

1. 用户确认优先：推荐可以给出依据，但最终规则由用户确认。
2. 真实可执行：内容从用户回答、源码、配置、测试、CI、git、现有文档抽取。
3. 保留已有：升级老项目时保留已有命名风格和文档约定。
4. 五个能力：项目说明、当前状态、下一步任务、验收标准、红线规则必须完备。
5. 短而强：AGENTS.md 只做入口路由，具体细节链接到状态、任务、DoD、审计、ADR 等文档。
6. 状态统一：Draft / Ready / In Progress / Blocked / Done。
