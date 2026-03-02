# skillbox

中文 | [English](README.md)

一组 [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) 技能集合 — 一条命令即可安装的实用 Agent 能力。

## 安装

全局安装所有技能：

```bash
npx skills add ba0gu0/skillbox -g
```

安装单个技能：

```bash
npx skills add ba0gu0/skillbox --skill cobalt-download -g
```

## 技能列表

| 技能 | 说明 |
|------|------|
| [cobalt-download](skills/cobalt-download/) | 通过 cobalt API 从 22 个平台下载视频/音频（YouTube、TikTok、B站、Twitter/X 等） |
| [jina-web](skills/jina-web/) | 通过 Jina AI Reader & Search API 读取网页和搜索互联网 — 支持 CSS 选择器、截图、缓存控制 |

## 许可证

[MIT](LICENSE)
