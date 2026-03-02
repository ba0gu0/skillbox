# skillbox

[中文](README_zh.md) | English

A collection of [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) skills — practical agent abilities you can install with one command.

## Install

Install all skills globally:

```bash
npx skills add ba0gu0/skillbox -g
```

Install a specific skill:

```bash
npx skills add ba0gu0/skillbox --skill cobalt-download -g
```

## Skills

| Skill | Description |
|-------|-------------|
| [cobalt-download](skills/cobalt-download/) | Download videos/audio from 22 platforms (YouTube, TikTok, Bilibili, Twitter/X, etc.) via cobalt API |
| [jina-web](skills/jina-web/) | Read web pages and search the internet via Jina AI Reader & Search APIs — supports CSS selectors, screenshots, caching control |

## License

[MIT](LICENSE)
