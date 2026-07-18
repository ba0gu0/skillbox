# Go Standards

本文件用于 Go 项目或包含 Go 后端的项目。已有项目以 `go.mod`、CI、
现有 formatter/linter/test 约定为准。

## 初始化

- 用 `go mod init module/path` 初始化，不手写 `go.mod` 凑结果。
- 依赖用 `go get` 管理，完成后 `go mod tidy`。
- 工具安装使用 `go install module/path@version`。
- 新项目优先标准库，只有明确收益时引入框架。
- 记录项目中实际可运行的命令；常见验证包括 `go test ./...` 和 `go vet ./...`，
  运行入口必须按具体 `cmd` 包确认。

## 格式与检查

- 所有 `.go` 文件必须 `gofmt`。
- 改 imports 时使用 `goimports`。
- 常规验证：`go test ./...`。
- 非平凡后端改动：`go vet ./...`。
- 依赖或安全相关改动：`govulncheck ./...`。
- 数据竞争风险改动：`go test -race ./...`，若太慢则限定包。
- 模糊测试适合 parser、decoder、协议处理、文件格式、输入校验。

## 包与目录

- 包名短、小写、无下划线，不使用 `common`、`utils`、`helpers` 作为默认包名。
- 目录按业务能力、协议边界或部署边界组织。
- `cmd/<name>` 放可执行入口；业务逻辑不要放在 `main`。
- `internal/` 放不希望外部导入的包。
- 包之间依赖方向清晰，避免循环依赖。
- 接口放在消费者侧；接受接口，返回具体类型，除非项目已有约定不同。
- 小接口优先，避免为了 mock 提前抽象所有实现。

## 命名

- 使用 Go 常见短变量名，但不要牺牲可读性。
- receiver 名称短且一致，避免 `this`、`self`。
- acronym 按 Go 风格保持一致，例如 `HTTPServer`、`userID`。
- 导出标识符必须有 godoc 注释，注释以标识符开头并以句号结束。
- 错误变量使用 `ErrXxx`；自定义错误类型使用 `XxxError`。

## 错误处理

- 不忽略错误；确实可忽略时写明原因。
- 错误信息小写开头，不带句号。
- 跨边界保留原因时用 `fmt.Errorf("context: %w", err)`。
- 需要让调用方判断时，使用 sentinel error、错误类型或 `errors.Is/As`。
- 不用 `panic` 处理正常业务错误。
- API 层不要把内部错误详情直接返回给用户。
- 日志记录错误时带结构化上下文，不重复记录同一个错误多次。

## Context

- `context.Context` 是第一个参数，通常命名为 `ctx`。
- 不把 context 存进 struct。
- 不传 nil context；不知道用什么时使用 `context.Background()` 或
  `context.TODO()`。
- 外部 IO、数据库、HTTP、队列、锁等待应支持取消。
- 不用 context 传普通可选参数；只传请求范围值、取消、deadline。

## 并发

- 每个 goroutine 必须有所有者、退出条件和错误路径。
- 循环中的 goroutine 要正确捕获循环变量。
- `sync.WaitGroup` 使用指针或局部变量，不复制。
- 不复制含 `sync.Mutex`、`sync.Once`、`sync.WaitGroup`、`atomic` 的 struct。
- channel 表示同步、所有权转移或事件，不为普通共享状态滥用 channel。
- 共享状态优先 mutex；需要无锁时必须有性能理由和测试。
- `time.Ticker`、`time.Timer` 用完停止。
- `select` 循环要处理 `ctx.Done()`。
- 并发限制使用 worker pool、semaphore 或 bounded channel。

## HTTP Server

- `http.Server` 按接口类型设置 `ReadHeaderTimeout`、`ReadTimeout` 和
  `IdleTimeout`。
- 普通响应设置 `WriteTimeout`；SSE、WebSocket 等长连接按连接生命周期
  单独设计，不能套用会提前截断流的全局写超时。
- handler 不直接 `panic`；使用中间件恢复并记录。
- 请求 body 设置大小限制，例如 `http.MaxBytesReader`。
- 解析 JSON 时限制大小并处理 unknown fields 的策略。
- 设置安全 header 时遵循项目部署环境。
- middleware 顺序明确：request id、logging、panic recovery、auth、rate limit、handler。
- graceful shutdown 处理 context、server shutdown、后台任务和连接关闭。

## HTTP Client

- `http.Client` 必须设置 `Timeout` 或每次请求使用带 deadline 的 context。
- response body 必须关闭。
- 非 2xx 状态按协议处理，不假设 body 一定是成功结构。
- 重试只针对幂等请求或有幂等 key 的请求。
- 不默认跟随不可信重定向到内网或 file scheme。
- 代理、TLS、自定义 transport 要集中配置，避免散落。

## JSON 与输入

- 输入结构体字段加 `json` tag。
- 边界层验证 required、范围、枚举、长度、格式。
- Go 1.18+ 的 `map[string]any` 或旧版本的 `map[string]interface{}`
  只用于边界层；进入业务前收窄类型。
- 需要保留未知字段时写清原因。
- 时间使用 `time.Time`；明确时区和格式。
- 金额不要用 float；使用整数最小单位或 decimal 库。

## 数据库

- 使用 context-aware 方法。
- 查询参数化，不拼接用户输入。
- 事务函数保持短，不夹外部网络调用。
- `rows.Close()` 并检查 `rows.Err()`。
- scan 错误要带查询语义上下文。
- migrations 使用项目指定工具；不要手改生产 schema。
- 连接池参数要配置并记录。

## 日志

- 使用 `log/slog` 或项目已有结构化日志。
- 不记录 raw cookie、token、Authorization、密码、密钥。
- request id、user id、tenant id、route、status、latency 使用结构化字段。
- 日志级别清晰：debug 诊断、info 状态、warn 可恢复异常、error 失败。
- 避免在循环中高频打印大日志。

## 配置

- 配置集中加载和校验。
- 环境变量名稳定，有 `.env.example`。
- 配置错误启动时失败，不在运行中隐式使用零值。
- 对日志输出配置摘要时脱敏。
- 默认值只用于安全、明确的本地开发场景。

## 测试

- 优先 table-driven tests。
- 失败信息使用 `got/want`。
- 辅助函数调用 `t.Helper()`。
- 黑盒 API 测试可使用 `_test` 包；需要内部状态时用同包测试。
- HTTP handler 使用 `httptest`。
- 外部服务使用 fake、interface 或 test server，不打生产端点。
- 并发测试避免固定 sleep，使用同步点、context 或 fake clock。
- 测试数据使用 `t.TempDir()`，不要写固定路径。
- 全局环境变量修改使用 `t.Setenv()`。

## CLI

- CLI 参数、环境变量、配置文件优先级要清晰。
- stdout 输出结果，stderr 输出诊断。
- 退出码稳定。
- destructive 命令支持 dry-run 或确认。
- 子命令和 flag 错误给出可行动提示。

## 安全易错点

- SSRF：限制 URL scheme、host、IP 段、重定向、DNS rebinding。
- 路径穿越：清理路径后仍要检查是否留在允许根目录。
- 命令执行：优先不用 shell；必须用时参数分离且白名单。
- 文件上传：限制大小、类型、扩展名、内容探测和存储位置。
- 模板渲染：使用安全模板和上下文转义。
- 加密：使用标准库或成熟库；不自制随机数和协议。

## Go 与 TypeScript 差异提醒

- Go 没有 TypeScript 的 `unknown`。Go 1.18+ 的 `any` 是 `interface{}` 别名；
  更早版本使用 `interface{}`。
- Go 不用 try/catch；错误通过返回值显式处理。
- Go 的 nil 不是 JS null；接口 nil 有动态类型陷阱。
- map 遍历顺序不稳定。
- slice 共享底层数组；append 后别假设旧引用独立。
- defer 在函数返回时执行，不在块级作用域结束时执行。
