# 规则参考

> 本文件承载生成流程的公共规则。`generation-steps.md` 负责执行顺序，本文件负责状态、验证、模板裁剪和覆盖边界。

## 统一状态机

所有任务、规格和状态文档使用同一套状态：

| 状态 | 说明 | 进入条件 |
|------|------|---------|
| Draft | 规划中 | 刚创建，需要细化 |
| Ready | 可执行 | 规格和验收标准已完备，依赖已满足 |
| In Progress | 执行中 | 已有人或 Agent 开始执行 |
| Blocked | 被阻塞 | 缺少外部条件或依赖 |
| Done | 已完成 | 实现、验证、文档/状态写回都已完成 |

- 非 Done 状态都可以进入 Blocked。
- 阻塞解除后回到进入 Blocked 前的状态；如无法判断，回到 Ready。
- Done 不能只表示代码完成，必须包含验证和写回。

### STATUS_RULES_SUMMARY 输出格式

派生 `{STATUS_RULES_SUMMARY}` 时必须使用以下结构：

```markdown
| 状态 | 说明 | 进入条件 |
|------|------|---------|
| Draft | 规划中 | 刚创建，需要细化 |
| Ready | 可执行 | 规格和验收标准已完备，依赖已满足 |
| In Progress | 执行中 | 已有人或 Agent 开始执行 |
| Blocked | 被阻塞 | 缺少外部条件或依赖 |
| Done | 已完成 | 实现、验证、文档/状态写回都已完成 |

- 非 Done 状态都可以进入 Blocked。
- 阻塞解除后回到进入 Blocked 前的状态；如无法判断，回到 Ready。
- Done 不能只表示代码完成，必须包含验证和写回。
```

## 项目阶段

`{PHASE}` 描述项目生命周期，不等同于任务状态。

| 阶段 | 进入条件 | 退出条件 |
|------|---------|---------|
| 初始化阶段 | 项目刚创建，核心边界和验证方式未稳定 | 最小可运行路径和基础验收命令明确 |
| 开发阶段 | 核心功能仍在建设 | 核心功能可用并进入持续优化 |
| 迭代阶段 | 核心功能可用，主要做功能增强和体验优化 | 主要工作转为修复、适配、低频变更 |
| 维护阶段 | 功能稳定，主要做修复、安全、依赖更新 | 项目重新进入大规模功能建设 |

可附加节奏标签，例如「迭代阶段（活跃）」或「维护阶段（低频）」。

## ADR 状态

ADR 状态独立于任务状态机，因为架构决策的生命周期不同于开发任务。
ADR 使用 Proposed / Accepted / Deprecated / Superseded。

## 最终验证

每次生成完成后，必须先记录本次实际写入的文件清单 `FILES`，再扫描。
`FILES` 不得为空，不得包含本次没有写入的文件，不得漏掉本次写入的文件。
示例仅作格式参考：

```bash
FILES=(AGENTS.md docs/current-state.md docs/project-audit.md)
scan() {
  PATTERN="$1" perl -Mopen=:std,:encoding\(UTF-8\) -ne '
    print "$ARGV:$.:$_" if /$ENV{PATTERN}/;
    close ARGV if eof;
  ' "${FILES[@]}"
}
scan '\{[A-Z][A-Z0-9_-]*\}'
scan '\{[^}]*\p{Han}[^}]*\}'
scan '\[待填充'
scan '\b(?:xxx|XXX)\b'
scan '<!--\s*TEMPLATE\b'
scan '<!--\s*TEMPLATE\s+META\b'
scan '<!--\s*REFERENCE\b'
scan '<!--'
scan '\]\([^)]*\*[^)]*\)'
scan '\{[a-z][^}]*\}'
scan '<[A-Za-z][^>[:space:]]*>'
```

以上扫描全部无输出才算通过；如有输出，清理后重新扫描。
如项目明确需要保留 HTML 注释，必须在生成计划中列出白名单和理由；默认最终文档不保留
任何 HTML 注释。

### 命令与链接验证

生成后还必须验证内容可执行性：

1. 对最终文档中写入的测试、构建、lint 命令，先确认对应 runner 或二进制存在。
   例如 `bun test` 检查 `command -v bun`，`uv run pytest` 检查 `command -v uv`。
2. 再验证具体脚本入口真实存在：
   - `bun run test` / `npm run test`：检查 package.json scripts 中有 `test`
   - `pnpm test` / `yarn test`：检查 package.json scripts 中有 `test`
   - `make test`：检查 Makefile 中有 `test:` 目标
   - `just test`：检查 justfile 中有 `test` recipe
   - `task test`：检查 Taskfile 中有 `test` 任务
   - `uv run pytest`：检查项目有 pytest 配置、测试目录，或用户确认该命令有效
   - `go test ./...`：检查 go.mod 存在
   - `cargo test`：检查 Cargo.toml 存在
   - `zig build test`：检查 build.zig 存在
3. 无法验证的命令必须写「待用户确认」，不得放进 DoD 或任务卡的必跑命令块。
4. 如项目声明 engines/toolchain 版本，检查本地工具版本是否满足要求。
5. 扫描内部 Markdown 链接，确认指向仓库内的目标文件或目录真实存在。
6. 复核 5 个能力都能被新 Agent 直接找到，不能只满足文件存在。
7. Markdown 链接不得使用 `*` 通配符作为最终目标；需要表达模式时写成纯文本说明。
8. 代码块中的每一行命令都必须能执行或明确注释为示例，不得写「待用户确认」。
9. 对照项目类型复核 DoD 和 security-checklist：
   - 无数据库时不得保留 SQL 注入、数据库访问、迁移回滚等必选项。
   - 无 HTML/浏览器输出时不得保留 XSS 必选项。
   - 无认证/权限模型时不得保留认证授权、会话、Token、权限检查必选项。
   - 纯文档项目不得保留构建、lint、测试、API、数据库等代码项目必选项。
10. 对照启用模块复核路径引用：
   - 未启用任务卡时，不得出现 `{TASKS_PATH}` 的最终路径或“先读任务卡”。
   - 未启用 specs 时，不得出现 `{SPECS_PATH}` 的最终路径或“先读规格”。
   - Small 项目的下一步任务入口必须指向 current-state，不得指向 next-tasks。
   - 所有保留路径必须在 `FILES` 或既有仓库文件中真实存在。
11. 扫描表格枚举占位，确认最终文件没有同时保留多个候选值，例如
    `✅/⚠️/❌`、`有效 / 过期 / 不存在`、`是/否`、`高/中/低`。

## 完备性检查

本节是 5 能力是否合格的唯一权威定义。SKILL.md 与 generation-steps.md 只做入口说明。

- 项目说明：AGENTS.md 存在且内容真实无占位符。
- 当前状态：`{CURRENT_STATE_PATH}` 存在且阶段描述准确。
- 下一步任务：任务列表真实可执行；Small 可在 current-state 中承载。
- 验收标准：`{DOD_PATH}` 存在且测试命令可用。
- 红线规则：AGENTS.md 红线部分完整且来自用户选择。
- 内容真实性：已完成列表、技术栈、常用命令、工具链偏好必须能追溯来源。

## 任务状态一致性

- 启用任务卡时，任务卡是单任务状态的权威来源。
- `{NEXT_TASKS_PATH}` 是队列视图，状态必须与任务卡同步。
- 任务状态变更时，必须同步任务卡、next-tasks、current-state 中的对应记录。
- 发现不一致时，以任务卡为准，并生成 P1 修复任务同步其他视图。

## 规则提升流程

每次任务完成、状态文档更新或生成 handoff 时，都必须扫描 `{LESSONS_PATH}` 和
`{PATTERNS_PATH}` 的「待提升规则」。当存在待提升规则时，P2 清理任务必须执行：

1. 审查待提升规则是否仍然有效。
2. 草拟 AGENTS.md 补充条目和放置位置。
3. 请求用户确认。
4. 用户确认后更新 AGENTS.md。
5. 清理 lessons/patterns 中对应待提升项，并记录提升日期。

## TEMPLATE META 使用规则

- 当模板包含 2 个以上需要说明抽取来源的变量组时，必须有 `TEMPLATE META` 块说明来源、裁剪规则或路径变量。
- 简单索引类模板可以只保留顶部 `TEMPLATE` 注释，但仍必须遵守通用裁剪规则。
- 生成最终文件时，顶部 `TEMPLATE` 注释和所有 `TEMPLATE META` 块都必须删除。

## 模板裁剪规则

1. 有真实来源的节保留并填写，无来源的节整节删除。
2. 不确定是否需要保留的节，写入待确认事项，而非填入猜测内容。
3. 不为“让文档看起来完整”而生编硬造任何内容。
4. 列表行、表格行、步骤项不是固定数量；有真实数据才生成行。
5. `scripts/security-reference.md` 是生成 `security-checklist.md` 的参考材料，不直接复制为最终文件。
6. 未启用任务卡模块时，删除任务卡路径列和“先读任务卡”类句子。
7. 未启用 handoff 模块时，删除交接报告检查项；Medium 按用户选择，Large 默认保留。
8. DoD 的任务类型节按项目类型裁剪；Small 默认只保留通用、CLI/脚本、文档相关项。
9. DoD 的通用标准和安全标准也必须按项目类型裁剪；纯文档项目只保留来源、格式、链接、
   敏感信息和发布权限相关项。
10. 未启用 specs 模块时，删除规格路径、规格任务和“先读规格”类句子。
11. 启用 specs 但未启用任务卡时，规格任务必须内联执行信息或链接到 next-tasks 锚点。
12. 目录结构示例只列已启用模块；未启用的目录不得用 `.gitkeep` 创建空壳。
13. 保留“如有/若存在”条件句时，句中路径仍必须指向真实存在的可选模块；否则删除该句。

## Handoff 决策表

| 规模 | 用户选择 | 是否生成 handoff | 任务卡检查项 |
|------|---------|------------------|-------------|
| Small | 任意 | 不生成 | 删除 |
| Medium | 不需要 | 不生成 | 删除 |
| Medium | 可选 | 复杂或跨模块任务生成 | 按任务保留 |
| Medium | 必须 | 每个任务生成 | 保留 |
| Large | 未特别说明 | 默认生成 | 保留 |
| Large | 用户明确不需要 | 不生成并记录原因 | 删除 |

handoff 的来源规则：

- 启用任务卡时，handoff 从任务卡、diff、验证结果和剩余风险生成。
- 未启用任务卡时，handoff 从 `{NEXT_TASKS_PATH}` 或 `{CURRENT_STATE_PATH}` 的任务记录、
  diff、验证结果和剩余风险生成，不得引用 `{TASKS_PATH}`。
- 未启用 specs、ADR、lessons、patterns 时，handoff 必须删除对应写回项。

## 不静默覆盖原则

以下操作禁止：

1. 静默覆盖已有文件。
2. 创建包管理器文件：package.json、pyproject.toml、go.mod。
3. 安装依赖，除非用户明确要求。
4. 修改代码文件。
5. 预设用户偏好。
