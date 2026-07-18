---
name: agent-ready-framework
description: >-
  把新项目、代码无文档项目、老项目或 monorepo 升级为无需聊天历史即可
  接手的 Agent 工作系统。用于初始化或审计项目文档，建立项目说明、
  当前状态、下一步行动、验收标准和红线规则，
  升级 AGENTS.md 配套交接体系，并按需创建 ADR、规格、任务卡和 handoff。
  仅需语言、工具链或工程规范时，改用 project-agent-standards。
---

# Agent-Ready Framework

把仓库变成可由新 Agent 从文件事实直接接手、执行、验证和写回的
工作系统。
不要用模板数量衡量完成度；
用以下 5 个能力是否可发现、可信且可执行来衡量：

| 能力键 | 新 Agent 必须能回答 |
|--------|---------------------|
| `project_identity` | 项目是什么，边界与技术栈是什么？ |
| `current_state` | 现在处于什么阶段，哪些事实已验证？ |
| `next_actions` | 下一步做什么，优先级、依赖和阻塞是什么？ |
| `acceptance` | 如何验证，什么条件才算完成？ |
| `red_lines` | 哪些操作禁止、受限或必须执行？ |

能力可以由现有文件承载，不要求固定文件名，也不要求每项单独建文档。

## 职责边界

- 本技能负责项目盘点、能力缺口、文档拓扑、状态/任务/DoD/ADR/spec/handoff、
  升级合并和跨文档验证。
- `project-agent-standards` 负责 `AGENTS.md` 中的技术栈、精确命令、
  语言/框架、测试、部署、安全与 CI 规则。
  生成或升级 `AGENTS.md` 时优先组合该技能。
- 不在本技能复制语言规范矩阵。
  配套技能不可用时，只生成基于项目事实的最小入口。
  不猜测工程规则。详见
  `references/project-agent-standards-integration.md`。

## 强制保证

1. 先读适用的上层和项目级指令，再读工作区状态。
   低层项目文档不得覆盖高优先级指令。
2. 保留用户未提交改动和既有命名；不回滚、迁移或格式化无关文件。
3. 每条项目事实、命令和状态都要有来源。
   无法证实的内容不得写成硬规则或已完成事实。
4. 只生成填补能力缺口所需的最小文档集。
   不要按 Small/Medium/Large 套整包模板。
5. `AGENTS.md` 保持为入口路由和硬规则。
   动态状态、任务、设计和历史放到独立文档。
6. 只有真正影响结果且无法从仓库发现的选择才询问用户。
   非阻塞未知项记录在审计中。
7. 不创建项目的包管理器产物、不安装依赖、不修改业务代码，
   除非用户明确把它们纳入范围。

## 工作流

1. **选择模式**：新/空项目用 bootstrap；已有代码缺文档用 onboard；
   已有文档用 upgrade；用户只要报告时用 audit。
2. **盘点事实**：检查指令层级、`git status`、manifest/lockfile、CI、
   runner、README、现有 Agent 入口、docs 和最近提交。
   优先运行只读盘点脚本。
3. **建立证据矩阵**：把结论标为 `verified`、`derived` 或 `unconfirmed`，
   并记录来源路径。
4. **评估 5 能力**：标记为完备、部分完备或缺失；
   验证从入口能否实际找到承载文件。
5. **选择最小文档集**：复用或更新现有文件优先于新增文件；
   仅在单文件明显过载时拆分。
6. **应用改动**：按现有语言与命名写作，移除模板说明和占位符，
   使用相对当前文件的链接。
7. **验证**：校验显式文件集、相对链接和 5 能力映射；
   对写入的必跑命令核对来源，安全且相关时实际运行。
   未运行的命令不得声称通过。
8. **交付**：报告新增/更新文件、能力映射、验证结果、
   未确认事实和剩余风险。

完整步骤见 `references/workflow.md`；证据与指令层级见
`references/evidence-and-authority.md`。

## 渐进读取

只读取当前任务需要的资料：

| 场景 | 必读 |
|------|------|
| 所有模式 | `references/workflow.md`、`references/evidence-and-authority.md` |
| 选择输出文件 | `references/document-selection.md` |
| 升级已有文档 | `references/upgrade.md` |
| 生成或升级 AGENTS.md | `references/project-agent-standards-integration.md` |
| 选择模板 | `references/template-catalog.md`，再读选中的单个模板 |
| 生成任务队列、任务卡或规格任务 | `references/task-state.md` |
| 高风险边界或独立安全清单 | `references/security-selection.md` |

不要预读全部模板。模板是可裁剪的素材，不是最终文档。

## 确定性工具

先把技能目录解析为本 `SKILL.md` 所在目录的绝对路径，
把项目根解析为目标仓库的绝对路径。
脚本要求 Python 3.12+；优先用隔离的 uv runner。
不要发现或使用目标项目环境。
命令中的示例绝对路径必须替换后再执行。

先盘点，不执行项目命令：

```bash
uv run --no-project --python 3.12 \
  /absolute/skill-directory/scripts/project_inventory.py \
  --root /absolute/project-root --format json
```

写入后验证明确的文件与能力映射：

```bash
uv run --no-project --python 3.12 \
  /absolute/skill-directory/scripts/validate_docs.py \
  --root /absolute/project-root \
  --file AGENTS.md \
  --file docs/current-state.md \
  --require project_identity=AGENTS.md \
  --require current_state=docs/current-state.md \
  --require next_actions=docs/current-state.md \
  --require acceptance=AGENTS.md \
  --require red_lines=AGENTS.md
```

把实际生成或修改的文件逐个传给 `--file`。
不要修改技能自身来记录文件列表。
验证器把 `project_identity` 映射文件视为 Agent 入口，
并检查其他四项能力能否通过相对链接到达。
因此该映射应指向 `AGENTS.md` 或项目实际采用的主入口。
禁止从目标项目的当前目录执行相对路径 `scripts/project_inventory.py` 或
`scripts/validate_docs.py`，以免运行项目内同名脚本。

## 模式规则

- **bootstrap**：根据用户已给目标生成可执行的最小入口；
  空项目没有真实命令时不伪造。
- **onboard**：从代码、配置、测试和 CI 反推当前事实；
  不要把推测的 TODO 写成既定任务。
- **upgrade**：先建立现有文件到 5 能力的映射和冲突表，
  再做局部合并；默认不改名。
- **audit**：只输出缺口、冲突和建议，不写入项目文件。

## 完成条件

- 5 个能力均能从 Agent 入口到达；同一事实没有互相冲突的权威副本。
- 最终文件没有模板注释、占位符、假命令、假路径或断开的相对链接。
- 动态状态与任务有更新时间和来源；`Done` 同时意味着实现、相关验证和
  必要写回完成。
- 未确认项与验证未运行项被明确披露，没有伪造成确定事实。
