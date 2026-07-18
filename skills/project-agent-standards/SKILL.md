---
name: project-agent-standards
description: >-
  Initialize or upgrade project AGENTS.md and agent-facing development standards.
  Use when creating or onboarding a project, generating or updating AGENTS.md,
  CLAUDE.md, Cursor rules, or Copilot instructions, selecting language-specific
  coding rules, defining test/build/deploy/security requirements, or translating
  global engineering standards into a project-specific instruction set.
---

# Project Agent Standards

Use this skill to turn broad engineering standards into a project-specific
`AGENTS.md` or equivalent agent instruction file.

Do not copy every reference into a project. Select only the rules that match
the real language, framework, package manager, runtime, deployment target,
security boundary, and verification commands found in the project.

## Workflow

1. Inspect the project before writing rules:
   - `git status --short`
   - top-level files and directories
   - package manifests and lockfiles
   - CI, Docker, compose, deployment, scripts
   - README/docs/current AGENTS files
2. Identify project shape:
   - main languages and secondary languages
   - app type: service, CLI, web app, mobile app, library, monorepo, data job
   - runtime and deployment: local only, Docker, systemd, Kubernetes, serverless
   - security/data boundaries: auth, secrets, user data, external network calls
3. Read the matching references:
   - agent setup and instruction hierarchy: `references/agent-initialization.md`
   - general engineering, testing, security, deployment: `references/engineering-standards.md`
   - language matrix: `references/language-standards.md`
   - detailed Go rules: `references/go.md`
   - project AGENTS template: `references/project-agents-template.md`
   - source links checked for this skill: `references/sources.md`
4. Write a concise project-level instruction file:
   - keep it actionable and project-specific
   - include exact commands that exist or should exist
   - link to longer docs instead of embedding everything
   - mark unknown facts as `待确认` rather than guessing
5. Validate the result:
   - no placeholder text
   - no rules for absent languages/frameworks
   - no contradiction with global or nested instructions
   - no fake commands, fake package names, or fabricated CI steps

## Output Rules

- Prefer `AGENTS.md` as the shared project instruction format.
- Keep global instructions short; put project rules in project `AGENTS.md`.
- Keep project `AGENTS.md` as a router plus hard rules. Put detailed specs,
  ADRs, task lists, and runbooks in `docs/`.
- When updating an existing project, preserve its naming, document structure,
  and user changes unless the user explicitly asks to replace them.
- For old or conflicting rules, explain why they are outdated before changing
  them.

## Recommended Project AGENTS Structure

Use this order unless the project already has a stronger convention:

1. Project identity
2. Non-negotiable rules
3. Read-first documents
4. Operating model
5. Current stack
6. Common commands
7. Language/framework rules
8. Verification matrix
9. Documentation/write-back duties

For a complete copy-ready skeleton, read `references/project-agents-template.md`.

## Interaction With Existing Skills

- Use `agent-ready-framework` when the user needs the full project handoff
  system: project charter, current state, next tasks, DoD, specs, ADRs.
- Use this skill when the user needs coding standards, language-specific
  requirements, AGENTS.md rules, testing/deployment/security defaults, or an
  initialization standard library.
- The two skills can be combined: generate the project operating system with
  `agent-ready-framework`, then use this skill to fill the language and
  engineering standards.
