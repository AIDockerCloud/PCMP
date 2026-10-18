# PCMP (Project Context Management Protocol)

[![Version](https://img.shields.io/badge/Version-1.0-blue.svg)](PROJECT_CONTEXT_ZH.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![AI-Agnostic](https://img.shields.io/badge/AI--Agnostic-Universal-purple.svg)](PROJECT_CONTEXT.md)

**PCMP (项目上下文管理协议 / Project Context Management Protocol)** 是一个专为人类开发者与 AI 编程智能体（AI Coding Agents）协同工作而设计的**工程上下文管理协议**。

它不依赖任何特定模型、IDE 或专用插件，完全基于**文件系统与 Markdown**运作，旨在解决长期、复杂、多会话开发过程中常见的“**上下文爆炸、会话遗忘、状态脱节、文档与代码不一致**”等核心痛点。

---

## 📖 核心文档入口

* 🇨🇳 **[PROJECT_CONTEXT_ZH.md](PROJECT_CONTEXT_ZH.md)**：完整中文规范手册（协议标准、Schema、交互指令与治理边界）
* 🌐 **[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)**：Full English Specification Manual

---

## ⚡ 核心原则 (Core Principles)

1. **当前状态优先 (Current State First)**  
   AI 智能体每次接管任务，必须优先读取当前状态快照（`STATE.md` 和 `TASK.md`），严禁依靠逐条回溯海量历史会话来推断当前状态。
2. **代码即最终真理 (Code as Ground Truth)**  
   当文档描述与实际运行代码、测试不一致时，以源码为准，并将文档滞后视为上下文缺陷及时修复。
3. **最小有效上下文 (Minimal Context)**  
   仅维护开发决策和任务推进必需的高信息密度内容，历史会话定期归档与摘要，拒绝无限膨胀。
4. **AI 与平台无关 (AI-Agnostic / IDE-Agnostic)**  
   兼容 Claude Code, Cursor, Windsurf, GitHub Copilot, Antigravity 等任意 AI 助手与开发环境。
5. **阶段技术文档独立性与追踪规范 (Phase-Independent Traceability)**  
   每个演进阶段在 `docs/S{N}-{short_name}/` 维护专属的需求-功能-方法追踪矩阵 (`requirements_traceability.md`) 与 4+1 架构视图，保障全链路可溯。
6. **管理协议与产品代码严格解耦 (Decoupling Protocol from Product Code)**  
   PCMP 仅为协同管理与工程交付协议，严禁作为业务代码逻辑或运行依赖侵入产品源码。
7. **双轨工程目录管理 (Dual-Track Management: S & S1~Sx)**  
   - **分阶段工程 (`phases/S{N}-{short_name}/`)**：阶段代码自包含，目标纯粹，便于回溯与复盘；
   - **持续演进主工程 (`continuous/`)**：集成各阶段已验证成果的完整主干工程。

---

## 📂 上下文目录标准结构 (`ai/`)

在遵循 PCMP 的项目中，AI 协同状态统一维护在工程根目录的 `ai/` 文件夹下：

```text
ai/
├── PROJECT.md          # 项目定位、宗旨、目标用户与范围边界 (长期稳定)
├── ARCHITECTURE.md     # 系统架构、模块关系、数据流与技术约束 (长期稳定)
├── STATE.md            # 项目全局状态实时快照 (动态更新)
├── TASK.md             # 当前唯一活动任务与验收指标 (动态更新)
├── PLAN.md             # 里程碑与阶段路线图 (动态更新)
├── DECISIONS.md        # 架构决策记录 (ADR, 长期累积)
├── ISSUES.md           # 缺陷与技术风险跟踪 (动态更新)
├── sessions/           # 结构化会话沉淀记录 (追加模式)
└── proposals/          # 针对 PCMP 协议本身的改进提案 (追加模式)
```

---

## 🔄 核心工作流程

```text
1. 开发者发出指令 ──► 2. AI 读取 PROJECT_CONTEXT ──► 3. AI 检阅 STATE.md & TASK.md
                                                                │
                                                                ▼
6. 沉淀会话与更新状态 ◄── 5. 代码实现与测试验证 ◄── 4. 查阅架构与源码推进任务
```

### 常用人类交互提示词 (Standard Prompts)

在任何 AI 智能体对话框中，可直接使用以下标准化指令：

* **项目初始化**：
  > `请读取 PROJECT_CONTEXT_ZH.md，初始化本项目的 ai/ 上下文管理体系并评估当前项目状态。`
* **跨会话/换新 AI 接管**：
  > `请读取 PROJECT_CONTEXT_ZH.md 接管项目，查阅 ai/STATE.md 和 ai/TASK.md，继续推进当前任务。`
* **会话收尾与沉淀**：
  > `请按照 PCMP 协议规范收尾当前会话：验证代码并运行测试，在 ai/sessions/ 沉淀会话记录，并更新 ai/STATE.md 和 ai/TASK.md。`

---

## 🏷️ 版本与发布

* **当前版本**：V1.0
* **更新内容**：发布 PCMP 基础核心协议，建立双语规范文档与标准化上下文目录规范。
