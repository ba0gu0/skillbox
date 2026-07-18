# skillbox

中文 | [English](README.md)

一组
[Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
技能集合——一条命令即可安装的实用 Agent 能力。

## 安装

全局安装所有技能：

```bash
npx skills add ba0gu0/skillbox -g
```

安装单个技能：

```bash
npx skills add ba0gu0/skillbox --skill cobalt-download -g
npx skills add ba0gu0/skillbox --skill agent-ready-framework -g
npx skills add ba0gu0/skillbox --skill jina-web -g
npx skills add ba0gu0/skillbox --skill project-agent-standards -g
```

## 技能列表

- [agent-ready-framework](skills/agent-ready-framework/)：
  构建基于证据、可由 Coding Agent 直接接手的项目工作系统。
- [cobalt-download](skills/cobalt-download/)：
  通过 cobalt API 从 22 个平台下载视频或音频。
- [jina-web](skills/jina-web/)：
  通过 Jina AI 读取网页和搜索互联网。
- [project-agent-standards](skills/project-agent-standards/)：
  生成项目专属的 Agent 工程规范和验证标准。

## 许可证

[MIT](LICENSE)
