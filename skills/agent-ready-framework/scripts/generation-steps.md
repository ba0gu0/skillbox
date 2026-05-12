# 生成步骤清单

> 本文档指导 Agent 如何生成项目接手系统。

---

## 核心原则

**用户确认优先**：Agent 可以根据项目现状和架构推荐，但最终规则必须由用户确认。

**推荐必须有依据**：不要脱离项目现状假设用户使用任何工具。

工具链推荐优先级：

1. 现有项目约定（lockfile、脚本、CI、文档）
2. 用户全局规范或项目上层 AGENTS.md / CLAUDE.md
3. 项目架构需求
4. skill 默认推荐

---

## 能力驱动的生成流程

### Step 1: 建立 5 能力映射

```
检查项目是否具备以下能力：

| 能力 | 检查项 | 判断 |
|------|--------|------|
| 项目说明 | README.md 或 AGENTS.md 有描述？ | ✅ 有 / ❌ 缺 |
| 当前状态 | 有 current-state 或类似文档？ | ✅ 有 / ⚠️ 有但不完整 / ❌ 缺 |
| 下一步任务 | 有 next-tasks 或 TODO？ | ✅ 有 / ⚠️ 有但不完整 / ❌ 缺 |
| 验收标准 | 有 DoD 或测试命令？ | ✅ 有 / ❌ 缺 |
| 红线规则 | AGENTS.md 有红线部分？ | ✅ 有 / ❌ 缺 |
```

状态定义见 `scripts/rules-reference.md` 的「统一状态机」。

### Step 2: 判断项目类型

```
新项目（目录为空或只有 .git）:
  → 执行「新项目生成流程」

有代码无文档项目:
  → 执行「代码项目生成流程」（也可由 /agent-ready-framework --code-only 直接触发）

有文档项目:
  → 执行「老项目升级流程」
```

---

## 新项目生成流程

### Step 1: 询问项目信息

#### 快速模式

如果用户要求快速初始化，只问 3 项：

1. 项目名称和一句话描述
2. 技术栈
3. 项目类型或规模判断

快速模式只生成可确认的最小骨架，并在 `{PROJECT_AUDIT_PATH}` 记录「自动生成，请确认」。
技术栈、命令、代码风格等缺少来源时留空或写入待确认事项。
补齐前，快速模式生成的任务状态只能标为 Draft，不得标为 Ready；`{PHASE}` 维持初始化阶段。
快速模式仍必须完成最终验证，不得留下占位符。

快速模式不允许生编命令或规则：能从源码、配置、CI、README 抽取的才填写；
缺少来源时写「待用户确认」，并在 `{PROJECT_AUDIT_PATH}` 列为待确认项。

#### 标准模式

```
请告诉我：

1. 项目名称和一句话描述
   例：backup-cli - 本地备份命令行工具
   例：TodoAPI - 轻量级任务管理 REST API 服务
   例：date-utils - 日期处理工具库

2. 技术栈（语言、框架、数据库）
   例：Go + chi, TypeScript + Preact, PostgreSQL + Redis

3. 项目类型
   - CLI 工具 / 脚本
   - 单体 Web 应用 / API
   - 管理后台 / 内部系统
   - 微服务 / 分布式平台
   - 企业级系统

4. 目标用户和预期寿命
   例：小团队使用，长期维护
```

### Step 2: 判断项目规模

根据系统复杂度判断（不是代码行数）：

| 规模 | 判断信号 | 默认文档复杂度 |
|------|----------|----------------|
| Small | 单一命令/脚本/POC，1-3 个功能，单人维护，无长期协作预期 | AGENTS.md + current-state + DoD + security-checklist |
| Medium | 单体应用/API/管理后台，3-10 个功能，1-3 人协作，有中长期维护预期 | + next-tasks；lessons/patterns/ADR/任务卡按用户选择 |
| Large | 多服务/多租户/企业级/合规敏感系统，10+ 功能，多人或多 Agent 协作 | + charter + working-principle + technical-architecture + glossary |

库/SDK 按复杂度选 Small 或 Medium；纯文档项目默认 Small，并跳过代码、构建、API、数据库相关模板。

如果无法判断，按 Medium 生成最小可执行系统，并把规模判断写入 `{PROJECT_AUDIT_PATH}` 的待确认项。

### Step 3: 询问用户偏好（核心）

**重要**：所有偏好都由用户选择，Agent 只提供推荐。

#### 3.1 询问工具链偏好

**前置检查**：如果上层全局规范或 CLAUDE.md 禁用了某工具，该工具不列入选项。只有「项目已有且用户显式确认保留」时才能作为例外。

过滤逻辑：

```text
读取上层 AGENTS.md / CLAUDE.md / 全局规范
如果禁止 npm 或 npx，则从候选项移除 npx，并标注「已被上层规范禁用」
如果禁止 pip，则从候选项移除 pip + venv，并标注「已被上层规范禁用」
如果禁止 poetry，则从候选项移除 poetry，并标注「已被上层规范禁用」
只有项目已有对应 lockfile/配置且用户确认保留时，才允许作为例外
如无上层规范，按项目已有 lockfile/配置推荐；也不存在时默认推荐 bun/uv
```

```
请选择你的工具链偏好：

JavaScript/TypeScript 运行时：
  [1] bun（推荐，更快）
  [2] node（项目已有 npm 体系且未被上层禁用时可选）
  [3] deno
  [4] 其他：___

包执行器：
  [1] bunx（推荐）
  [2] npx（仅项目已有 npm 体系且未被上层禁用时可选）
  [3] 其他：___

Python 环境：
  [1] uv/uvx（推荐，更快）
  [2] pip + venv（仅项目已有 pip 体系且未被上层禁用时可选）
  [3] poetry（仅项目已有 poetry 体系且未被上层禁用时可选）
  [4] 其他：___

Go 环境：
  [1] 标准 go 命令
  [2] 其他：___

你的选择：___
```

#### 3.2 询问红线偏好

```
请选择你的红线偏好：

🚫 Never（绝对禁止）- 推荐选项：
  [ ] 提交 .env 或 secrets/
  [ ] 硬编码敏感信息
  [ ] 跳过安全检查
  [ ] 跳过测试提交
  [ ] 在日志中记录敏感信息
  [ ] 其他：___

请选择要启用的 Never 规则（可多选）：___

⚠️ Ask First（需确认）- 推荐选项：
  [ ] 删除文件
  [ ] 添加新依赖
  [ ] 修改数据库 schema
  [ ] 修改 API 接口
  [ ] 修改部署配置
  [ ] 修改安全相关代码
  [ ] 其他：___

请选择要启用的 Ask First 规则（可多选）：___

✅ Always（必须执行）- 推荐选项：
  [ ] 运行测试后提交
  [ ] 完成任务后更新状态文档
  [ ] 安全检查通过后标记 Done
  [ ] 新错误记录到 lessons.md
  [ ] 成功模式记录到 patterns.md
  [ ] 架构决策记录到 ADR
  [ ] 其他：___

请选择要启用的 Always 规则（可多选）：___
```

#### 3.3 询问文档偏好

```
请选择你的文档偏好：

文档命名风格：
  [1] 普通式（current-state.md, next-tasks.md）
  [2] 编号式（01-*.md, 02-*.md）
  [3] 自定义：___

是否需要交接报告（handoff）：
  [1] 不需要
  [2] 可选
  [3] 必须

是否需要 ADR（架构决策记录）：
  [1] 不需要
  [2] 需要

是否需要 lessons/patterns：
  [1] 不需要
  [2] 需要

是否启用独立任务卡：
  [1] 不需要，任务在 next-tasks.md 或 current-state.md 中维护
  [2] 需要，生成 `{TASKS_PATH}` 目录和任务卡

是否生成功能规格（specs）：
  [1] 不需要
  [2] 按需生成
  [3] 必须生成（Large 默认）

是否生成术语表（glossary）：
  [1] 不需要
  [2] 需要（Large 默认）

是否启用多 Agent 协作：
  [1] 不启用，单人/单 Agent 维护
  [2] 启用，需要角色、权限和分支协作规则

你的选择：___
```

### Step 4: 生成最小可执行文档

按规模和用户选择生成文档。模块清单以对应 preset 为准：`presets/small.md`、`presets/medium.md` 或 `presets/large.md`。
快速模式必须额外生成 `{PROJECT_AUDIT_PATH}`，用于记录自动判断、缺失信息和待确认项。

**生成规则**：
- 内容必须从用户回答和用户选择中抽取
- 模板中的 `<!-- TEMPLATE: ... -->` 和 `<!-- TEMPLATE META ... -->` 块必须移除
- 所有 `{UPPER_CASE_VAR}` 变量必须替换为真实内容
- 红线使用用户选择的规则，不预设

---

## 代码项目生成流程

### Step 1: 扫描项目

```
列出项目根目录:
ls {PROJECT_ROOT}

检查文件:
- README.md
- AGENTS.md / CLAUDE.md
- go.mod / package.json / pyproject.toml / Cargo.toml
- Cargo.toml / Package.swift / pom.xml / build.gradle / *.csproj
- docs/
- Makefile / Taskfile
```

### Step 1.1: 检测 monorepo

如出现以下信号，先按 monorepo 处理：
- 不同子目录发现多个包或模块根：package.json、go.mod、pyproject.toml、Cargo.toml
- 根 package.json 存在 workspaces 字段
- 存在 go.work、pnpm-workspace.yaml、lerna.json、nx.json、turbo.json
- 根目录有 package.json，同时 services/、packages/、apps/ 下存在其他语言模块

1. 按仓库统一生成一套文档
2. 按 package/module 分别生成文档
3. 根目录生成总入口，子目录生成局部文档

未确认前不要直接生成多套文档。

#### Monorepo 生成规则

用户确认 monorepo 策略后，按以下边界生成：

| 策略 | 根入口 | 子目录入口 | 状态/任务 | 验证命令 |
|------|--------|------------|----------|----------|
| 仓库统一 | 根 AGENTS.md 是唯一入口 | 不生成 | 根文档统一维护 | 按 workspace 汇总 |
| 分模块 | 根 AGENTS.md 只做索引 | 每个模块有局部 AGENTS.md | 模块内维护 | 模块内命令为准 |
| 根入口+局部 | 根 AGENTS.md 定义全局红线 | 子目录补充模块规则 | 根队列列跨模块任务，模块队列列局部任务 | 根命令和模块命令都列出 |

生成 monorepo 文档时必须：

1. 明确 root 与 package/module 的权威边界。
2. 为每个模块记录 `{MODULE_ROOT}`、模块类型、入口文件和验证命令来源。
3. 跨模块任务必须写依赖模块；不能只写单个任务名。
4. 子目录 AGENTS.md 只能补充局部规则，不能覆盖根红线；冲突写入 `{PROJECT_AUDIT_PATH}`。
5. 命令按工作区验证，例如根 `bun test`、模块 `cd packages/foo && go test ./...` 分别验证。
6. 未确认策略前，只生成审计和建议，不创建多套入口。

### Step 2: 抽取技术栈

```
按 manifest 和源码抽取，不认识时不要猜测：

| 信号 | 抽取内容 | 语言/生态 |
|------|----------|-----------|
| go.mod / go.work | module、依赖、workspace | Go |
| package.json | name、scripts、dependencies、workspaces | JS/TS |
| pyproject.toml / uv.lock | project、tool、dependencies | Python |
| Cargo.toml | package、workspace、dependencies | Rust |
| Package.swift | package、products、targets | Swift |
| pom.xml / build.gradle | artifact、tasks、dependencies | Java/JVM |
| *.csproj / *.sln | TargetFramework、项目结构 | .NET |
| Makefile / justfile / Taskfile | 任务命令 | 通用 |
| .github/workflows / .gitlab-ci.yml | CI 验证命令 | 通用 |

若没有 manifest，按文件扩展名、入口脚本、README 和用户确认抽取；
仍无法判断时，在 `{PROJECT_AUDIT_PATH}` 记录“技术栈待确认”。
```

### Step 3: 抽取命令

```
从 package.json scripts 或 Makefile 抽取：

| 命令类型 | 检查项 |
|---------|--------|
| 安装 | 从 scripts 中识别 |
| 开发 | dev / serve / run |
| 测试 | test / check |
| 构建 | build / compile |
| 检查 | lint / fmt / vet |
```

### Step 4: 判断 5 能力缺口

代码无文档项目通常至少缺当前状态、下一步任务、验收标准和红线规则。仍需显式检查：

| 能力 | 检查方式 |
|------|----------|
| 项目说明 | README/package metadata/module name/用户回答 |
| 当前状态 | git log、代码结构、用户确认 |
| 下一步任务 | TODO/Issue/代码缺口/用户确认 |
| 验收标准 | scripts/Makefile/CI/用户确认 |
| 红线规则 | 上层规范/用户选择 |

### Step 5: 判断项目规模

根据新项目流程 Step 2 的规模标准选择 preset。代码项目不得默认按 Medium 处理；
CLI/脚本优先 Small，多服务/monorepo/合规敏感系统优先 Large 或拆分处理。

### Step 6: 抽取代码风格

```
从项目中找一个代表性代码文件：
- 选择核心模块的代码文件
- 抽取一个简短代码片段（10-20行）
- 用于 AGENTS.md 代码风格部分
```

### Step 7: 询问缺失偏好

只询问缺失能力相关偏好（询问流程同新项目 Step 3），不要重复询问已能从项目约定可靠抽取的信息。

### Step 8: 生成文档

按抽取的真实信息和用户选择生成文档：
- 项目描述：从 README/package metadata/module name 或用户回答抽取
- 技术栈：从配置文件抽取
- 命令：从 scripts 抽取
- 代码风格：从代码抽取
- 红线：从用户选择生成

**生成后必须执行最终验证（见本文档末尾）**。

### Step 9: 最终验证

1. 列出本次实际写入的所有文件路径。
2. 将完整路径写入 `rules-reference.md` 示例中的 `FILES` 数组。
3. 确认 `FILES` 非空、无遗漏、无本次未写入文件。
4. 执行最终扫描、命令验证、链接验证和 5 能力完备检查。
5. 有任何输出或失败时，修正后重新执行。

---

## 老项目升级流程

老项目升级执行 `scripts/upgrade-reference.md`。本文件只保留入口，避免升级细节与公共变量、验证规则混在一起。

---

## 变量处理

跨模板共享变量、派生变量、命令变量、路径变量和 CLAUDE.md/AGENTS.md 共存策略见 `scripts/variables-reference.md`。

---

## 公共规则引用

生成过程中必须遵守 `scripts/rules-reference.md`：

- 统一状态机
- 最终验证
- 5 能力完备检查
- 内容真实性检查
- TEMPLATE META 使用规则
- 模板裁剪规则
- 不静默覆盖原则

同时按需读取：

- `scripts/variables-reference.md`：变量、路径、命令和入口共存规则
- `scripts/upgrade-reference.md`：老项目升级细节
