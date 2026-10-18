---
pcmp_version: "2.1"
revision: 1
updated: 2026-10-19
---

# 项目定位与目标 (PROJECT.md)

## 1. 项目基本信息
- **项目名称**：PCMP (Project Context Management Protocol / 项目上下文管理协议)
- **定位**：面向人类开发者与 AI 编程智能体协同工作的通用工程上下文管理协议（AI-Agnostic / IDE-Agnostic）。
- **目标用户**：使用 AI 编程助手（Claude Code, Cursor, Windsurf, GitHub Copilot, Antigravity 等）进行软件研发与工程交付的开发者和团队。

## 2. 核心宗旨与痛点解决
解决人类与 AI 在长期、复杂、跨模型协作中常见的：
1. **上下文爆炸**：历史记录过多导致模型失忆或注意力涣散；
2. **状态脱节**：每次新开会话丢失工作进度与任务目标；
3. **代码与文档冲突**：AI 幻觉反噬真理，误将缺陷当作设计更新文档；
4. **决策失控**：AI 越权做出重大架构变更而无人类确认记录。

## 3. 边界与硬约束 (Scope & Hard Constraints)
### 范围 (Scope)
- 协议核心规范文档：[PROJECT_CONTEXT.md](../PROJECT_CONTEXT.md) 与 [PROJECT_CONTEXT_ZH.md](../PROJECT_CONTEXT_ZH.md)；
- 项目上下文存储体系：`ai/` 标准目录规范；
- 派生工具链：用于检索与加速的 SQLite 派生索引工具；
- 推荐协作准则与审查实践。

### 非目标 (Non-Goals)
- 本项目不是一个闭源的商业 SaaS 平台；
- 不依赖特定的云端闭源模型或专有 IDE 插件；
- 不在产品源码中强行插入管理协议业务依赖。

### 硬约束 (Hard Constraints)
1. **Markdown 权威原则**：一切核心状态和决策以 Markdown 文件为最终权威，派生索引可随意删除重建；
2. **解耦原则**：管理协议严禁侵入被管理工程的产品业务逻辑代码；
3. **确认来源原则**：所有 Accepted 的架构决策必须具备明确的确认人与会话依据。
