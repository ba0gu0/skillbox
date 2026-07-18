# Project AGENTS Template

复制前必须裁剪。删除所有不适用章节，替换所有占位符。

````markdown
# {Project Name} Agent Guide

This repository is agent-executable. Treat this file as the entry point for
development rules, project context, verification, and write-back duties.

## Non-negotiable Rules

- {Security/data/compatibility rule}
- {Do-not-touch rule}
- {Secret/logging rule}
- {Deployment or API compatibility rule}

If a task appears to require breaking one of these rules, stop and report it as
blocked.

## Project Identity

- Name: {project name}
- Stage: {POC / MVP / production / maintenance}
- Purpose: {one sentence}
- Primary users: {users}
- Core architecture: {short architecture}

## Read First

Read in this order:

1. `README.md`
2. `{docs/current-state.md}`
3. `{docs/architecture.md}`
4. `{docs/next-tasks.md}`
5. `{docs/definition-of-done.md}`

For feature work, also read:

- `{docs/specs/<feature>/requirements.md}`
- `{docs/specs/<feature>/design.md}`
- `{docs/specs/<feature>/tasks.md}`
- `{docs/tasks/<task>.md}`

## Operating Model

1. Inspect local status before editing.
2. Confirm task scope and dependencies.
3. Implement only the requested scope.
4. Run the relevant verification commands.
5. Update docs/tasks/ADR when behavior, architecture, config, or workflow changes.
6. Report changed files, verification, and remaining risk.

## Current Stack

- Backend: {language/framework}
- Frontend: {language/framework}
- Database: {database}
- Queue/cache: {queue/cache}
- Build: {build tooling}
- Deploy: {deploy target}
- Observability: {logs/metrics/tracing/errors}

## Common Commands

```bash
{test command}
```

```bash
{build command}
```

```bash
{run command}
```

```bash
{lint/typecheck command}
```

## Language And Framework Rules

### {Primary Language}

- Follow the project runtime/version from `{manifest file}`.
- Format with `{formatter}`.
- Test with `{test command}`.
- {language-specific hard rule}
- {language-specific hard rule}

### {Secondary Language}

- {only rules needed for this project}

## Dependency Policy

- Use the package manager and lockfile already present in the repo.
- Do not add dependencies without a clear project need.
- Do not generate package manager artifacts for another ecosystem in this repo.
- Security or dependency changes require `{audit command}` when available.

## Configuration And Secrets

- `.env.example` documents required variables with safe example values.
- `.env`, secrets, tokens, cookies, private keys, database dumps, and credential files
  must stay ignored by Git.
- Logs and test artifacts must not contain raw secrets.

## Verification Matrix

| Change Area | Required Verification |
|-------------|-----------------------|
| {backend} | `{command}` |
| {frontend} | `{command}` |
| {database/schema} | `{command}` |
| {deployment/config} | `{command}` |
| {security/auth} | `{command}` |

## Before Finishing

- Run relevant verification commands.
- Update docs if behavior, API, config, deployment, or workflow changed.
- Add or update ADR when a long-term architecture decision is made.
- Update task/status files when task state changes.
- Report changed files, verification results, and residual risks.
````

## Go Service Example Additions

Use only for Go backend/API/service projects:

```markdown
### Go

- Follow the `go` and `toolchain` versions in `go.mod`.
- Run `gofmt`; use `goimports` when imports change.
- Regular verification: `go test ./...`.
- Non-trivial backend changes: `go vet ./...`.
- Dependency/security changes: `govulncheck ./...`.
- `context.Context` is the first parameter; do not store context in structs.
- Do not ignore errors; wrap with `%w` when callers need the cause.
- Goroutines must have ownership, cancellation, and an error path.
- HTTP servers and clients must set timeouts.
- Go has no TypeScript `unknown`; use `any` only for Go 1.18+ projects,
  and use `interface{}` for older modules.
```

## TypeScript Frontend Example Additions

```markdown
### TypeScript / Frontend

- Follow the installed TypeScript, framework, bundler, and browser targets.
- Do not use `any` to bypass type checking; use `unknown`, schema validation, or type guards.
- Do not introduce a new package manager; follow the existing lockfile.
- UI changes require desktop and mobile verification when a browser is available.
- User-visible strings must follow the project i18n policy.
```

## Backend/API Example Additions

```markdown
### Backend/API

- Authentication and authorization must be checked server-side.
- Do not log raw credentials, cookies, tokens, OAuth secrets, or encryption keys.
- External HTTP calls require timeout and cancellation.
- File upload/download paths must prevent traversal and avoid storing upstream files
  unless specified.
- Streamed APIs should stay streamed unless a spec requires buffering.
```

## Deployment Example Additions

```markdown
### Deployment

- Config changes must update `.env.example` or deployment docs.
- Docker/Compose changes require `docker compose config` or the project equivalent.
- Database migrations must include verification and rollback or forward-compatible notes.
- Production-affecting changes must document health checks and rollback risk.
```
