---
pcmp_version: "2.1"
revision: 1
updated: 2026-10-19
---

# 系统架构与技术约定 (ARCHITECTURE.md)

## 1. 架构总览
PCMP 采用**双层架构设计**：
1. **核心持久层 (Core Authority Layer)**：纯文本 Markdown 结构化文件系统（根目录规范文档与 `ai/` 状态目录），跨平台、人类可读、Git 友好。
2. **派生加速层 (Derivative Acceleration Layer)**：可选的 SQLite 派生索引（`ai/.cache/index.sqlite`），由核心 Markdown 文件解析派生，提供全文检索（FTS5）与结构化 SQL 查询加速能力。

```text
┌────────────────────────────────────────────────────────┐
│               Core Authority (Markdown)                │
│  PROJECT.md | ARCHITECTURE.md | STATE.md | TASK.md ... │
└──────────────────────────┬─────────────────────────────┘
                           │ 提取解析 / Hash 校验
                           ▼
┌────────────────────────────────────────────────────────┐
│         Derivative Cache (ai/.cache/index.sqlite)      │
│  file_meta | decisions | issues | sessions | fts5      │
└────────────────────────────────────────────────────────┘
```

## 2. 核心技术选型
- **协议载体**：Markdown (CommonMark / GFM) + YAML Frontmatter。
- **派生索引实现 (方案 A)**：Python 3 原生标准库（`sqlite3` + FTS5、`hashlib`、`pathlib`、`re`），实现零外部依赖的轻量单脚本 CLI。
- **推荐中文规范工具**：STC (Simplified Technical Chinese)，支持技术中文检查。

## 3. 数据流设计
1. **人类/AI 修改**：修改 `ai/` 下的各 Markdown 文件，递增 `revision`。
2. **状态刷新**：运行 `python3 scripts/pcmp_index.py --update` 或 `--rebuild`。
3. **比对入库**：工具计算文件 SHA-256 哈希，变更文件重新写入 SQLite 表结构。
4. **快速查询**：AI 或开发者通过 CLI 快速过滤未决提议（Proposed）、检索标签（Tags）或全文搜索。

## 4. 约束与隔离策略
- `ai/.cache/` 必须被 `.gitignore` 排除，严禁提交到 Git；
- 索引文件损坏或丢失时，直接重新全量扫描即可 100% 恢复。
