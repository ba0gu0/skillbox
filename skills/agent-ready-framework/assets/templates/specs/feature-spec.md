<!--
TEMPLATE:
  用于跨模块或需异步评审的功能。简单任务使用任务卡即可。
  最终文件删除本注释、变量和不适用设计节。
-->
# {FEATURE_NAME} 功能规格

- 状态：{SPEC_STATUS}
- 负责人：{OWNER}
- 最后更新：{UPDATED_AT}

## 问题与目标

{PROBLEM_AND_GOAL}

## 用户与场景

{USERS_AND_SCENARIOS}

## 范围

### 包含

{IN_SCOPE_ITEMS}

### 不包含

{OUT_OF_SCOPE_ITEMS}

## 验收标准

{ACCEPTANCE_CRITERIA}

每条标准必须可观察或可测试，并说明必要的失败路径。

## 技术设计

{TECHNICAL_DESIGN}

把当前实现与提议设计分开标注：
当前组件、接口和数据来自项目证据；新设计可以来自用户需求、
架构推理或 ADR，但必须标为 proposed，并说明验证或确认方式。

## 实施切片

| 切片 | 目标 | 依赖 | 验证 | 任务入口 |
|------|------|------|------|----------|
{IMPLEMENTATION_ROWS}

## 未决问题与风险

{OPEN_QUESTIONS_AND_RISKS}

## 相关文档

{RELATED_LINKS}
