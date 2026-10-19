---
name: pcmp
description: >
  PCMP（Project Context Management Protocol，项目上下文管理协议）智能体技能。
  当用户输入 /pcmp、要求初始化项目上下文、接管工作流、会话收尾沉淀、架构决策 (ADR) 登记、代码文档一致性诊断，或查询本地 SQLite 派生索引时使用。
---

# PCMP 智能体工程上下文管理技能

本 Skill 为 AI 智能体提供按照 PCMP v2.1 规范管理工程上下文的标准动作集。它将原本冗长的人类提示词转化为简洁的自动化命令流程。

---

## 核心原则速查

1. **当前状态优先**：AI 接管必读顺序 = `PROJECT_CONTEXT_ZH.md` ➔ `ai/PROJECT.md`（硬约束） ➔ `ai/STATE.md` ➔ `ai/TASK.md`。严禁仅凭摘要猜测约束，严禁通读全部历史会话反推现状。
2. **冲突分级核实**：代码证明“当前物理实现”，但不自动推翻需求或已确认决策。发现脱节时：标记差异 ➔ 核实依据（需求/ADR/测试） ➔ 决定修代码还是修文档。
3. **最小有效上下文**：仅记录决策和推进必需的信息；会话定期压缩。
4. **信息分层标注**：显式使用 `[事实]`、`[假设]`、`[提议]`、`[已确认]`、`[未决]`。AI 的建议未经确认一律不得记为已决定。
5. **Markdown 权威，派生可全量重建**：Markdown 是唯一法定权威。派生索引（SQLite）为可随时删除重建的缓存。
6. **材料审阅授权（推荐准则）**：审阅、审计或样式检查的材料由人类指定或显式授权挑选；未获许可前，AI 不得擅自扫描全工程扩大审阅范围。

---

## 指令集与工作流

当用户输入以下命令或表达对应意图时，执行对应标准工作流：

### 1. `/pcmp init` (初始化项目上下文体系)
- **目标**：为新项目或未启用 PCMP 的项目建立标准 `ai/` 状态目录。
- **执行动作**：
  1. 检查根目录是否存在 `PROJECT_CONTEXT_ZH.md`（或 `PROJECT_CONTEXT.md`），若不存在则提示用户或从官方模板获取；
  2. 检查并创建 `ai/` 目录结构：
     - `PROJECT.md`：记录项目定位、核心目标、硬约束与边界；
     - `ARCHITECTURE.md`：记录系统架构、模块分层与技术约定；
     - `STATE.md`：生成初始状态快照（带有 `pcmp_version: "2.1"`, `revision: 1`）；
     - `TASK.md`：建立当前唯一活动任务单；
     - `PLAN.md`：规划高阶路线图与里程碑；
     - `DECISIONS.md`：初始化 ADR 决策日志；
     - `ISSUES.md`：初始化缺陷与风险跟踪表；
     - `sessions/` 与 `proposals/`：建立追加目录及 `.gitkeep` 占位；
  3. 检查 `.gitignore`，确保包含 `ai/.cache/`；
  4. 评估当前工程现状并向用户汇报初始化总结。

### 2. `/pcmp takeover` (换新会话 / 跨 AI 接管项目)
- **目标**：新会话或新智能体接手任务，快速建立上下文基准。
- **执行动作**：
  1. **必读第一步**：通读 `PROJECT_CONTEXT_ZH.md`（若存在 `ai/PROJECT_CONTEXT_ZH.md` 则以其为准）；
  2. **必读第二步**：阅读 `ai/PROJECT.md`，明确系统宗旨与不可违反的硬约束；
  3. **必读第三步**：阅读 `ai/STATE.md` 与 `ai/TASK.md`，掌握当前位置与当前唯一焦点；
  4. **决策检索**：检索 `ai/DECISIONS.md` 中与当前活动任务相关的 Accepted 决策；
  5. **按需查阅**：查阅 `ai/ARCHITECTURE.md` 或 `ai/PLAN.md`；需要历史审计证据时再查阅 `ai/sessions/`；
  6. **产物核验**：查验相关源码与测试，确认与文档状态吻合；
  7. **接管确认**：向人类明确 Immediate Next Action 并列出未决问题 (`[未决]`)，等待或直接推进。

### 3. `/pcmp finalize` (会话收尾与上下文沉淀)
- **目标**：完成一次实质性开发后，沉淀审计记录并更新状态快照。
- **执行动作**：
  1. **产物验证**：运行项目自动化测试与代码检查，确保符合任务验收标准；
  2. **变更审查**：执行 `git status` 与 `git diff`，确认改动范围严格受控于当前任务；
  3. **沉淀会话**：在 `ai/sessions/` 下生成 `SESSION-YYYY-MM-DD-NNN.md`，记录元数据、目标、变更清单、验证结果与下一步建议；
  4. **更新状态**：
     - 刷新 `ai/STATE.md`：更新 Last Updated、Completed、In Progress、Immediate Next Action，并将 `revision + 1`；
     - 刷新 `ai/TASK.md`：更新进度、验收结果或结项状态，并将 `revision + 1`；
  5. **登记决策**：若会话涉及架构、依赖或数据结构变更，在 `ai/DECISIONS.md` 追加 ADR（未经确认标 `Proposed`，已确认附 `- 确认来源:`）；
  6. **刷新派生索引**：若项目中存在 `scripts/pcmp_index.py`，自动执行：
     ```bash
     python3 scripts/pcmp_index.py --update
     ```
  7. **完成报告**：向用户汇报修改清单与提交就绪状态。

### 4. `/pcmp adr <决策标题>` (登记架构决策)
- **目标**：记录重要的技术选型、架构调整或规范决策。
- **执行动作**：
  在 `ai/DECISIONS.md` 追加标准 ADR 区块：
  ```markdown
  ## DEC-NNN — 决策标题
  日期: YYYY-MM-DD | 状态: Proposed / Accepted
  - 确认来源: <谁在何时确认,附会话/审批链接> (缺失此字段一律视为 Proposed)
  - 背景 (Context): 现状与痛点
  - 决策 (Decision): 采纳的方案
  - 理由 (Reason): 选择原因
  - 备选方案 (Alternatives): 放弃的方案及原因
  - 影响 (Consequences): 收益、约束与代价
  ```

### 5. `/pcmp assess` (只读状态与一致性诊断)
- **目标**：评估当前实现与文档是否脱节，发现潜在上下文漂移。
- **执行动作**：
  1. 只读比对源代码实现与 `ARCHITECTURE.md`、`DECISIONS.md` 中的设计约定；
  2. 检查 `STATE.md` 与实际文件修改历史的吻合度；
  3. 输出一致性诊断报告，列出代码超前（需补文档）或文档滞后（上下文缺陷）项；
  4. **严禁在诊断阶段修改任何业务代码**。

### 6. `/pcmp index [args]` (派生索引维护与查询)
- **目标**：调用本地 SQLite 派生加速层进行结构化查询或全文搜索。
- **执行动作**：
  若存在 `scripts/pcmp_index.py`，智能体可按需运行：
  - 查询未决提议：`python3 scripts/pcmp_index.py --query-decisions --status-filter Proposed`
  - 检索分层标签：`python3 scripts/pcmp_index.py --query-tags --tag-filter proposal`
  - 全文搜索关键词：`python3 scripts/pcmp_index.py --search "<关键词>"`
  - 全量重建缓存：`python3 scripts/pcmp_index.py --rebuild`
  - 查看索引统计：`python3 scripts/pcmp_index.py --status`
