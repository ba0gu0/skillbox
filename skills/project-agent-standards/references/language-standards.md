# Language Standards Matrix

只把项目实际使用的语言规则写进项目 `AGENTS.md`。已有项目优先遵循本地
版本、formatter、linter、lockfile 和 CI。

## Go

详细规则见 `go.md`。项目 AGENTS 至少写：

- 按 `go.mod` 的 `go`/`toolchain` 版本开发。
- 所有 Go 文件 `gofmt`；imports 改动用 `goimports`。
- 常规验证：`go test ./...`；非平凡后端改动加 `go vet ./...`。
- 安全/依赖变更加 `govulncheck ./...`。
- `context.Context` 第一个参数，不存入 struct。
- 不忽略错误；需要保留原因时用 `%w` 包装。
- goroutine 必须有取消、所有者和退出路径。
- HTTP server/client 必须有 timeout。
- Go 没有 TypeScript 的 `unknown`。Go 1.18+ 可用 `any`，更早版本使用
  `interface{}`；两者都只应用于真实边界层。

## JavaScript / TypeScript

- 已有项目遵循当前 Node/Bun/Deno 版本、tsconfig、lockfile 和 bundler。
- 新项目优先 TypeScript strict；已有项目不降低 strictness。
- TypeScript 禁止用 `any` 逃避检查；未知输入使用 `unknown`、
  schema 校验或类型守卫。
- 现代语法以目标 runtime 和浏览器矩阵为准，不为追求新语法破坏兼容性。
- 包管理器按 lockfile 选择，不混用 npm/yarn/pnpm/bun。
- 新项目测试优先 Vitest；已有项目遵循现有测试栈。
- ESLint 新项目使用 flat config；已有项目迁移前不要强行替换。
- 网络请求、订阅、计时器、effect 要有取消/清理路径。
- 运行时输入用 Zod、Valibot、TypeBox、io-ts 或项目已有 schema 方案。

## React

- 已有项目遵循已安装 React 版本。
- 新项目可优先 React 19+，但不要在 React 18 项目硬写 React 19 API。
- Server Components/App Router 仅在框架支持时使用。
- 状态优先本地 state/reducer；跨页面或复杂状态再引入 Zustand、Jotai 等。
- effect 只处理同步外部系统；不要把可派生状态塞进 effect。
- 组件要有 loading、empty、error、disabled、success 状态。
- 可访问性覆盖 label、focus、键盘操作、aria、颜色对比。

## Vue

- 新项目优先 Vue 3 + Composition API + `<script setup lang="ts">`。
- 已有 Options API 项目不要无关迁移。
- 状态管理使用 Pinia 或项目已有方案。
- `v-model`、props、emits 要有类型；复杂表单使用 schema 校验。

## Next.js / Nuxt / Meta Frameworks

- 新 Next.js 项目优先 App Router；已有 Pages Router 项目不要无关迁移。
- 明确 server/client 边界，不把 secret 放进 client bundle。
- 数据获取、缓存、revalidate、route handlers 要按框架版本确认。
- 部署目标影响 runtime：Node、Edge、serverless、static export 不能混淆。

## Python

- 已有项目按 `pyproject.toml`、runtime、CI 版本开发；新项目目标 Python 3.12+。
- 新代码必须有 type hints；复杂边界使用 `dataclass`、`TypedDict`、
  Pydantic 或 attrs。
- 路径优先 `pathlib.Path`；新代码避免 `os.path`。
- 新项目 formatter/linter 优先 Ruff；已有项目遵循现有配置。
- 测试使用 pytest 或项目已有栈。
- 一次性依赖优先 `uv run --with`；CLI 优先 `uvx`。
- 不写裸 `except` 或空 `except`；异常带上下文。
- Web 项目要写清配置、迁移、健康检查、安全 header 和 async/sync 边界。

## Java

- 遵循项目 Java target/source compatibility，不擅自使用更高版本语法。
- 使用 Maven/Gradle wrapper，不要求全局安装构建工具。
- 新代码使用现代 Java 语法时必须兼容目标 runtime。
- Controller 只做协议边界，业务逻辑放 service。
- 事务边界放 service 层；避免在事务中做外部网络调用。
- SQL 使用参数化、JPA Criteria、MyBatis 绑定或项目安全方式。
- 异常映射集中处理，不把堆栈直接返回用户。
- 测试遵循项目已安装的 JUnit 版本、Testcontainers、MockMvc/WebTestClient
  或项目现有栈。

## Kotlin

- 遵循项目 Kotlin/JVM/Android 版本。
- 空安全优先；避免 `!!`，除非有可证明不变量。
- 协程使用结构化并发，明确 dispatcher、scope、取消和异常传播。
- Android UI 遵循项目 Compose/XML 体系，不混写无关技术栈。
- Multiplatform 项目明确 commonMain/platformMain 边界。

## C#

- 遵循项目 `.csproj` target framework 和 nullable 配置。
- 新项目启用 nullable reference types；已有项目不无关扩大范围。
- async 方法使用 `CancellationToken`；不要 sync-over-async。
- ASP.NET Core 项目明确 DI lifetime、middleware 顺序、authn/authz、配置来源。
- Entity Framework 查询注意 N+1、tracking、迁移和事务边界。
- 测试遵循 xUnit/NUnit/MSTest 或项目现有栈。

## Rust

- 遵循 `rust-toolchain.toml`、MSRV 和 `Cargo.lock`。
- 提交前跑 `cargo fmt`、`cargo test`；非平凡改动跑 `cargo clippy -- -D warnings`。
- `unsafe` 必须局部、可解释，并写明不变量。
- 库代码优先具体错误类型；应用层可用 `anyhow`。
- 异步项目明确 runtime，不在 async 上下文阻塞线程。
- feature flag 要有默认策略和组合测试。
- 公开 API 变更注意 semver、docs、examples。

## C / C++

- 遵循项目 C/C++ 标准版本、编译器和构建系统。
- 新 C++ 代码优先 RAII、智能指针、标准库容器。
- 明确所有权、生命周期、线程安全和异常策略。
- 不新增裸 `new/delete`、不安全字符串处理、未检查 buffer 长度。
- 打开警告并修复新增警告。
- 安全敏感改动运行 ASan/UBSan/TSan 或项目已有 sanitizer。

## PHP

- 遵循项目 PHP 版本、Composer lockfile 和框架版本。
- 新代码使用 strict types、类型声明、返回类型。
- Laravel/Symfony 项目遵循框架认证、授权、验证、迁移约定。
- SQL 使用 query builder/ORM 参数绑定。
- 用户输出通过模板自动转义或明确上下文转义。
- 测试使用 PHPUnit/Pest 或项目已有栈。

## Ruby

- 遵循 `.ruby-version`、Gemfile.lock 和项目 RuboCop 配置。
- Rails 项目遵循 MVC 边界；复杂业务抽 service/form/query object 要符合项目风格。
- 数据迁移可回滚或写明不可回滚原因。
- ActiveRecord 查询注意 N+1、事务和批处理。
- 测试使用 RSpec/Minitest 或项目已有栈。

## Swift

- 遵循项目 Swift/Xcode/iOS/macOS target。
- 新项目优先 Swift 6 strict concurrency；已有项目按迁移状态推进。
- 并发优先 `async/await`、`Task`、`Actor`，避免无边界 GCD。
- UI 状态更新在主 actor。
- 避免 force unwrap；必须使用时写清不变量。

## Dart / Flutter

- 遵循项目 Flutter/Dart SDK 版本。
- 状态管理按项目既有方案：Riverpod、Bloc、Provider、GetX 等。
- Widget 保持小而可组合；不要把业务逻辑塞进 build。
- 异步操作处理 loading/error/cancel/dispose。
- UI 需要验证不同屏幕尺寸、方向、文字缩放。

## SQL

- 所有动态值参数化。
- 动态表名、列名、排序字段必须白名单。
- schema 变更写迁移。
- 新索引要对应查询路径，并考虑写入成本。
- 大批量更新/删除分批执行，可恢复。
- 时间、时区、货币、精度、NULL 语义必须明确。

## Shell

- Bash 脚本使用 `set -euo pipefail`。
- 变量展开加引号；数组用于参数列表。
- 检查依赖命令存在。
- 删除、覆盖、迁移类命令默认 dry-run 或明确确认。
- 不解析 `ls` 输出；优先 `find -print0`、数组和安全分隔符。

## PowerShell

- 脚本使用 `Set-StrictMode -Version Latest` 和 `$ErrorActionPreference = "Stop"`。
- 使用对象管道，不把结构化数据转成脆弱字符串再解析。
- 路径使用 `Join-Path`。
- secret 使用 SecretManagement、环境变量或平台 secret。

## R

- 遵循项目 renv lockfile。
- 数据处理脚本固定输入输出、随机种子、session info。
- 包导入显式，不依赖交互式全局环境。
- 报告生成记录数据来源、过滤条件和再生成命令。

## Scala

- 遵循项目 Scala/SBT 版本。
- 函数式抽象服务可读性；不要为简单逻辑堆类型体操。
- Future/IO/ZIO/Cats Effect 等 effect 系统不能混用无边界。
- Spark 项目注意 shuffle、partition、schema、checkpoint 和数据倾斜。

## Elixir

- 遵循项目 Elixir/Erlang/OTP 版本。
- OTP 进程要有 supervision tree、restart strategy、timeout。
- Phoenix 项目明确 context、schema、migration、LiveView 边界。
- 并发和消息传递要考虑 backpressure。

## Lua

- 遵循项目 Lua/LuaJIT/Neovim/OpenResty runtime。
- 模块不污染全局变量。
- OpenResty 项目注意 cosocket、共享字典、worker 生命周期和阻塞 IO。

## Terraform / IaC

- 运行 plan 前先确认 workspace、backend、provider version。
- 不提交 state、tfvars secret、云凭证。
- 模块输入输出明确，变量有类型和描述。
- 生产 apply 需要用户确认或受控流水线。
- 资源删除、替换、权限扩大必须高亮。

## YAML / JSON / Config

- 配置文件要保留 schema、注释或示例。
- 不手改机器生成文件，除非该项目约定如此。
- 大型 JSON 优先用结构化工具修改，避免脆弱字符串替换。
- CI YAML 修改后运行本地校验或平台 dry-run。

## Markdown / Docs

- 文档面向可执行使用，不写空泛口号。
- 命令、路径、环境变量必须准确。
- 架构决策写 ADR，任务状态写任务文档，不混在 README。
- 用户可见文档避免泄露内部 token、账号、端口和私有域名。
