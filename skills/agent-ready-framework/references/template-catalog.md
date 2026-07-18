# 模板目录

模板位于 `assets/templates/`。
只读取计划使用的模板，不要把整个目录加载进上下文。

## 使用规则

1. 模板只提供结构候选，不提供项目事实。
2. 先确定承载能力和真实来源，再选择模板。
3. 删除所有 `TEMPLATE`、`TEMPLATE META`、示例行和不适用章节。
4. 替换全部变量；没有来源的章节应删除或留在审计待确认项，
   不写进硬规则。
5. Markdown 链接必须相对最终源文件目录计算，
   不能直接复用仓库根路径变量。
6. 写入后使用本技能绝对路径下的 `scripts/validate_docs.py` 检查显式文件集。

生成任务队列、任务卡或规格任务前，读取 `references/task-state.md`。
不要在模板中维护第二套状态定义。

## 核心模板

- **最小 Agent 入口**
  - 模板：`assets/templates/agents-md/project-router.md`
  - 读取条件：配套规范技能不可用或仅需路由骨架。
- **当前状态**
  - 模板：`assets/templates/state/current-state.md`
  - 读取条件：动态状态不适合继续放在入口文件。
- **下一步行动**
  - 模板：`assets/templates/state/next-tasks.md`
  - 读取条件：多个任务需要排序、领取或记录依赖。
- **完成定义**
  - 模板：`assets/templates/quality/definition-of-done.md`
  - 读取条件：多类任务共享稳定验收标准。
- **项目审计**
  - 模板：`assets/templates/audit/project-audit.md`
  - 读取条件：冲突或迁移决策需要长期追踪。

## 按需模板

- **项目特有安全检查**
  - 模板：`assets/templates/security/security-checklist.md`
  - 读取条件：命中安全选择规则。
- **项目章程**
  - 模板：`assets/templates/charter/project-charter.md`
  - 读取条件：目标、范围和成功标准需长期约束。
- **架构说明**
  - 模板：`assets/templates/architecture/architecture.md`
  - 读取条件：结构或机制复杂且已有证据。
- **ADR**
  - 模板：`assets/templates/adr/decision.md`
  - 读取条件：存在长期架构决策。
- **功能规格**
  - 模板：`assets/templates/specs/feature-spec.md`
  - 读取条件：需求跨模块或需异步评审。
- **任务卡**
  - 模板：`assets/templates/tasks/task-card.md`
  - 读取条件：任务需独立领取或跨会话执行。
- **交接报告**
  - 模板：`assets/templates/handoff/handoff.md`
  - 读取条件：长任务换执行者且现有记录不足。

不要预建空 ADR、spec、task 或 handoff 文件。需要时从模板创建具体实例。
