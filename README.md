# skillbox

[中文](README_zh.md) | English

A collection of
[Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
skills — practical agent abilities you can install with one command.

## Install

Install all skills globally:

```bash
npx skills add ba0gu0/skillbox -g
```

Install a specific skill:

```bash
npx skills add ba0gu0/skillbox --skill cobalt-download -g
npx skills add ba0gu0/skillbox --skill agent-ready-framework -g
npx skills add ba0gu0/skillbox --skill jina-web -g
npx skills add ba0gu0/skillbox --skill project-agent-standards -g
```

## Skills

- [agent-ready-framework](skills/agent-ready-framework/):
  Build an evidence-based project handoff system for coding agents.
- [cobalt-download](skills/cobalt-download/):
  Download videos and audio from 22 platforms through the cobalt API.
- [jina-web](skills/jina-web/):
  Read web pages and search the internet through Jina AI.
- [project-agent-standards](skills/project-agent-standards/):
  Generate project-specific Agent engineering and verification standards.

## License

[MIT](LICENSE)
