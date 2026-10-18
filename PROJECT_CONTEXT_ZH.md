# 项目上下文管理协议 (PCMP)

**版本：** 1.0  
**文件：** `PROJECT_CONTEXT_ZH.md` / `PROJECT_CONTEXT.md`  
**定位：** AI 辅助项目上下文管理协议（AI-Agnostic / IDE-Agnostic）  
**规范入口：** 本文档定义**管理规则**，实际项目状态统一维护在 **`ai/`** 目录中。

---

## 1. 核心原则

1. **当前状态优先 (Current State First)**：AI 必须优先阅读当前状态（`STATE.md`、`TASK.md`），严禁通过通读全部历史会话记录来反推当前状态。
2. **代码即最终真理 (Code as Ground Truth)**：当文档与实际代码不一致时，以源码和测试为准，并及时修正过时文档。
3. **最小有效上下文 (Minimal Context)**：仅记录决策和开发必需的信息。历史会话定期压缩摘要，杜绝上下文无限膨胀。
4. **AI 与平台无关 (AI-Agnostic)**：不绑定任何特定模型、IDE、Prompt 或平台，仅依赖文件系统与 Markdown 运作。
5. **阶段技术文档独立性与追踪规范 (Phase-Independent Architecture & Traceability)**：每个演进阶段都必须在 `docs/S{N}-{short_name}/`（如 `docs/S1-minimal-core/`）维护该阶段专属的：
   * **需求-功能-方法追踪矩阵说明书 (`requirements_traceability.md`)**：建立清晰的「需求 ➔ 功能 ➔ 代码落地方法」全链路映射表，支持后续追加需求驱动 AI 自动化设计与开发；
   * **独立 4+1 架构视图 (`4_plus_1_view.md`)** 与 **核心时序图 (`sequence_diagrams.md`)**：精准刻画该阶段的代码物理实现、组件依赖与调用边界。
6. **管理协议与产品代码严格解耦 (Decoupling Protocol from Product Code)**：PCMP 仅是指导人类与 AI 协作管理本仓库的工程规范，严禁将其作为业务逻辑或运行依赖硬编码进产品源码（如 `backend/`、`frontend/`）中。被开发的产品必须保持高度通用性，能够独立运行于任意用户工作区。
7. **双轨工程目录管理与标准命名 (Dual-Track: S & S1~Sx)**：
   * **分阶段工程 (`phases/S{N}-{short_name}/` ➔ 如 `phases/S1-minimal-core/`)**：统一采用 `S` + 阶段序号 + 阶段简称命名，每个阶段独立建目录开发，代码自包含，专一实现该阶段目标，便于代码回溯与独立分析。
   * **持续演进主工程 (`continuous/` ➔ S)**：作为最终集成的完整形态项目，当各阶段完成并通过验证后，按需将稳定成果合入主工程。

---

## 2. 上下文目录结构 (`ai/`)

```text
ai/
├── PROJECT.md          # 项目定位、目标与边界范围 (长期稳定)
├── ARCHITECTURE.md     # 系统架构、模块设计与技术约束 (长期稳定)
├── STATE.md            # 项目当前整体状态快照 (动态更新)
├── TASK.md             # 当前活动任务与验收标准 (动态更新)
├── PLAN.md             # 高阶路线图与里程碑规划 (动态更新)
├── DECISIONS.md        # 架构与技术决策记录 (ADR, 长期累积)
├── ISSUES.md           # 已知问题与技术风险追踪 (动态更新)
├── sessions/           # 开发会话记录 (追加模式, 定期压缩)
└── proposals/          # 协议改进提案 (追加模式)
```

### 文件职责与性质

| 文件 / 目录 | 核心职责 | 性质 |
| :--- | :--- | :--- |
| `PROJECT.md` | 项目名称、宗旨、目标用户、核心目标、Scope 与 Non-Goals | 长期稳定 |
| `ARCHITECTURE.md` | 技术栈、系统架构图、核心组件、数据流、外部依赖与技术约定 | 长期稳定 |
| `STATE.md` | 当前状态快照：已完成、进行中、阻塞、风险、当前焦点、下一步动作 | 动态更新 |
| `TASK.md` | 当前活动任务：目标、背景、范围、验收标准、当前进度、即时动作 | 动态更新 |
| `PLAN.md` | 当前阶段、里程碑、近期计划 (Next Steps)、中远期规划 | 动态更新 |
| `DECISIONS.md` | 架构决策记录 (ADR)：背景、决策、理由、备选方案、影响 | 长期累积 |
| `ISSUES.md` | 问题追踪：ID、状态、描述、影响、规避方案、关联组件 | 动态更新 |
| `sessions/` | 每次有意义的开发会话记录 (`SESSION-YYYY-MM-DD-NNN.md`) | 追加模式 |
| `proposals/` | 针对 PCMP 协议本身的改进提案 | 追加模式 |

---

## 3. 标准文件 Schema 规范

### 3.1 `STATE.md` (当前状态快照)
必须保持精炼，确保 AI 毫秒级读取：
* **Last Updated**：更新日期
* **Overall Status**：总体状态
* **Completed**：已完成关键项
* **In Progress**：进行中事项
* **Blocked**：阻塞事项
* **Current Risks & Focus**：当前风险与焦点
* **Immediate Next Action**：下一步即时动作

### 3.2 `TASK.md` (当前任务)
仅维护**当前唯一活动任务**，完成后移入会话记录：
* **Current Task & Objective**：任务名称与核心目标
* **Why & Scope**：必要性与范围（包含 / 不包含）
* **Acceptance Criteria**：量化验收标准
* **Current Progress & Blocker**：当前进度与阻塞项
* **Immediate Next Action**：下一步即时动作

### 3.3 `DECISIONS.md` (架构决策记录 - ADR)
涉及架构、API、核心依赖、数据模型与安全边界的重要变更必须登记：
```markdown
## DEC-NNN — 决策标题
日期: YYYY-MM-DD | 状态: Accepted / Proposed / Deprecated / Superseded
- 背景 (Context): 现状与痛点
- 决策 (Decision): 采纳的方案
- 理由 (Reason): 选择原因
- 备选方案 (Alternatives): 权衡与未选原因
- 影响 (Consequences): 正面收益与约束/代价
```
> **规则**：严禁隐式推翻已 Accepted 的决策，新方案必须以新决策替代说明。

### 3.4 `sessions/SESSION-YYYY-MM-DD-NNN.md` (会话记录)
每次实质性开发会话完成后生成：
```markdown
# Session YYYY-MM-DD-NNN
- 元数据: 日期 / 执行 Agent / 关联 Task / 状态
- 目标 (Goal) & 原因 (Why)
- 变更内容 (What): 实际代码与配置修改
- 执行结果 (Result): 测试与项目状态
- 问题与决策 (Issues & Decisions)
- 下一步 (Next)
```

---

## 4. AI 工作流与优先级

### 4.1 AI 接管流程 (Takeover Flow)
```text
1. 读取 PROJECT_CONTEXT.md / ZH 
   ↓
2. 读取 ai/STATE.md 与 ai/TASK.md (掌握当前全局与任务)
   ↓
3. 必要时查阅 ai/ARCHITECTURE.md / PLAN.md / DECISIONS.md
   ↓
4. 查验相关源代码与测试
   ↓
5. 明确 Immediate Next Action 并开始执行
```

### 4.2 会话收尾工作流 (Session Completion Flow)
```text
1. 验证代码与运行测试
   ↓
2. 审查变更文件 (git status / diff)
   ↓
3. 编写 ai/sessions/ 会话记录
   ↓
4. 同步更新 ai/STATE.md 与 ai/TASK.md
   ↓
5. 必要时更新 PLAN.md / DECISIONS.md / ISSUES.md
   ↓
6. 确立下一步即时动作 (Immediate Next Action)
```

### 4.3 信息冲突优先级
```text
实际代码与测试 (最高) > STATE.md > TASK.md > DECISIONS.md > PLAN.md > 历史会话 (最低)
```
> 若发现代码与文档不一致，视为**上下文一致性缺陷**并主动修正文档，严禁忽略。

---

## 5. 人类标准交互指令 (Standard Human Prompts)

人类开发者可直接复制以下标准提示词，驱动任何 AI 智能体执行对应场景的工作：

### 5.1 项目首次初始化 (Initialization)
> `请读取 PROJECT_CONTEXT_ZH.md，初始化本项目的 ai/ 上下文管理体系并评估当前项目状态。`

### 5.2 换新 AI / 跨会话接管 (Takeover & Continue)
> `请读取 PROJECT_CONTEXT_ZH.md 接管项目，查阅 ai/STATE.md 和 ai/TASK.md，继续推进当前任务。`

### 5.3 现状诊断与一致性评估 (Read-Only Assessment)
> `请读取 PROJECT_CONTEXT_ZH.md，评估项目当前状态与架构一致性，分析代码与文档是否存在脱节。不要修改代码。`

### 5.4 方案规划与技术决策 (Planning & ADR Proposal)
> `请读取 PROJECT_CONTEXT_ZH.md，结合 ai/PLAN.md 提出下一步开发计划或架构方案建议。不要修改代码。`

### 5.5 缺陷排障与问题登记 (Issue Tracking & Diagnosis)
> `请读取 PROJECT_CONTEXT_ZH.md，分析该问题并登记到 ai/ISSUES.md，提出修复方案。`

### 5.6 会话收尾与上下文沉淀 (Finalize Session)
> `请按照 PCMP 协议规范收尾当前会话：验证代码并运行测试，在 ai/sessions/ 沉淀会话记录，并更新 ai/STATE.md 和 ai/TASK.md。`

---

## 6. 治理与权限边界

### 6.1 AI 权限
* **允许**：更新 `ai/` 下的状态、任务、计划、会话、问题、已采纳决策；压缩历史会话。
* **禁止**：严禁擅自扩大任务范围；严禁未经授权修改本协议本身。

### 6.2 人类确认边界 (须人工批准)
* 变更项目核心目标与产品定位。
* 变更关键架构原则或推翻已定重大架构决策。
* 修改本协议规则与 Schema 结构。
* 移除核心安全约束与防护机制。

---

## 7. 合规自检清单 (Checklist)

- [ ] **启动前**：已阅读协议，通过 `STATE.md` 和 `TASK.md` 明确当前状态与焦点，已查验相关源码。
- [ ] **过程中**：专注当前任务范围，未盲目引入无关变更；重要架构决策已记录于 `DECISIONS.md`。
- [ ] **收尾前**：实现已测试验证，已创建 `SESSION` 记录，`STATE.md` 和 `TASK.md` 已同步刷新，已明确下一步动作。