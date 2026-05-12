<!--
TEMPLATE:
  本文件为模板。生成最终项目文档时必须：
  1. 移除本注释块
  2. 替换所有 {UPPER_CASE_VAR} 变量为真实内容
  3. ADR 列表从项目实际 ADR 文件生成
-->
# ADR 索引

> Architecture Decision Records - 架构决策记录

## 什么是 ADR

ADR 用于记录架构级或流程级决策。Agent 在修改架构、技术栈、安全边界、部署方式前，必须先检查这里。

## 使用规则

1. 修改技术栈、部署拓扑、安全边界、凭证处理、数据模型前先查 ADR
2. 重大新决策必须新增 ADR，不能只写在聊天记录里
3. 推翻旧决策时新增 ADR，并把旧 ADR 状态标为 `Superseded`
4. ADR 只记录为什么这样做，不替代 spec 和任务卡

---

## ADR 列表

| ADR | 状态 | 说明 |
|------|------|------|
| [0001-{TITLE_1}](0001-{TITLE_1}.md) | {STATUS_1} | {SUMMARY_1} |
| [0002-{TITLE_2}](0002-{TITLE_2}.md) | {STATUS_2} | {SUMMARY_2} |
| [0003-{TITLE_3}](0003-{TITLE_3}.md) | {STATUS_3} | {SUMMARY_3} |

---

## 状态定义

| 状态 | 说明 |
|------|------|
| Proposed | 提议中，待讨论确认 |
| Accepted | 已确认，当前有效 |
| Deprecated | 已过时，不再推荐 |
| Superseded | 已被替代，参考新 ADR |

---

## 新增 ADR 流程

1. 确定决策确实需要 ADR（架构级、技术栈、安全边界等）
2. 复制模板 `adr-template.md`
3. 扫描 `{ADR_PATH}` 中已有 `NNNN-*.md` 文件，取最大编号 +1，左侧补零到 4 位
4. 命名为 `NNNN-short-title.md`，例如 `0002-select-runtime.md`
5. 填写各字段
6. 更新本索引
7. 提交审核

---

## 常见决策类型

| 类型 | 示例 |
|------|------|
| 技术栈选择 | 使用 Go + chi 而非 Gin |
| 数据库选择 | 使用 PostgreSQL 而非 MySQL |
| API 设计 | REST vs GraphQL |
| 安全边界 | 凭证只存服务端 |
| 部署方式 | Docker vs Kubernetes |
| 代码风格 | 命名约定、文件结构 |

<!-- TEMPLATE META START —— 链接生成规则，不进入最终文件
ADR 列表只能链接到真实存在的 ADR 文件，不得在最终 Markdown 链接中使用 `*` 通配符。
如果还没有 ADR，ADR 列表写“暂无已记录 ADR”，并删除示例行。
新增流程中的 `NNNN-*.md` 是纯文本模式说明，不作为链接。
不要在最终文档中保留 `<short-title>` 或 `{short-title}` 这类伪占位。
TEMPLATE META END -->
