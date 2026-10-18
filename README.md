# PCMP (Project Context Management Protocol)

[![Version](https://img.shields.io/badge/Version-2.1-blue.svg)](PROJECT_CONTEXT_ZH.md)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![AI-Agnostic](https://img.shields.io/badge/AI--Agnostic-Universal-purple.svg)](PROJECT_CONTEXT.md)
[![Recommended: STC](https://img.shields.io/badge/Recommended-STC-orange.svg)](https://github.com/daimonia-ai/STC-Simplified-Technical-Chinese)

**PCMP (项目上下文管理协议 / Project Context Management Protocol)** 是一个专为人类开发者与 AI 编程智能体（AI Coding Agents）协同工作而设计的**通用工程上下文管理协议**。

它不绑定任何特定模型、IDE 或专用插件，完全基于**本地文件系统与 Markdown**运作，旨在解决复杂软件与工程交付中常见的“**上下文爆炸、会话遗忘、状态脱节、文档与代码不一致、AI 幻觉决策**”等核心痛点。

---

## 📖 核心文档入口

* 🇨🇳 **[PROJECT_CONTEXT_ZH.md](PROJECT_CONTEXT_ZH.md)**：完整中文规范手册（协议标准、Schema、交互指令、治理边界与自检清单）
* 🌐 **[PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)**：Full English Specification Manual

---

## ⚡ 核心原则 (Core Principles)

1. **当前状态优先，但必读含定义 (Current State First)**  
   AI 智能体接管必读顺序 = **本协议 + `ai/PROJECT.md`（目标与硬约束） + `ai/STATE.md` + `ai/TASK.md`**。严禁仅凭状态摘要推测系统约束，严禁通读全部历史会话反推现状。
2. **冲突分级核实，不设绝对优先 (Tiered Conflict Verification)**  
   代码与测试证明的是“当前实现”，但不自动推翻用户原始需求、安全约束或已确立的 ADR 决策。发现不一致时：**标记差异 ➔ 核实依据（需求/ADR/测试） ➔ 决定修正实现还是更新文档**。
3. **最小有效上下文 (Minimal Effective Context)**  
   仅维护开发决策和推进任务必需的高价值信息；历史会话记录定期压缩摘要，防止上下文膨胀。
4. **AI 与平台无关 (AI- & Platform-Agnostic)**  
   兼容 Claude Code, Cursor, Windsurf, GitHub Copilot, Antigravity 等任意 AI 助手与开发环境。
5. **信息分层标注 (Information Layering)**  
   关键信息显式标注：`[事实]` / `[假设]` / `[提议]` / `[已确认]` / `[未决]`。AI 的建议未经人类确认不得记为已决定。
6. **协议与产品代码严格解耦 (Decoupling Protocol from Product Code)**  
   PCMP 仅为指导人机协同的工程管理规范，严禁将其作为业务逻辑或运行时依赖硬编码进产品源码。
7. **Markdown 权威，派生可全量重建 (Markdown as Authority)**  
   一切权威事实与决策均存在于 Markdown 文件中；索引与缓存（如 SQLite）均为可随时删除重建的派生工具。即使删除所有派生缓存，人和 AI 仍能完整接管项目。

---

## 📂 上下文目录标准结构 (`ai/`)

在遵循 PCMP 的项目中，AI 协同状态统一维护在工程根目录的 `ai/` 文件夹下：

```text
项目根目录/
├── PROJECT_CONTEXT.md        # 英文完整通用协议 (原版)
├── PROJECT_CONTEXT_ZH.md     # 中文完整通用协议 (原版)
├── AGENTS.md / CLAUDE.md     # 智能体通用工程入口与规则配置
├── .gitignore                # 忽略项: 包含 node_modules/ 与 ai/.cache/
└── ai/
    ├── PROJECT.md            # 项目定位、宗旨、核心目标、边界与硬约束 (长期稳定)
    ├── ARCHITECTURE.md       # 系统架构、模块设计、数据流与技术约定 (长期稳定)
    ├── STATE.md              # 项目全局当前状态快照 (动态更新, 带 revision)
    ├── TASK.md               # 当前唯一活动任务与验收指标 (动态更新, 带 revision)
    ├── PLAN.md               # 高阶路线图与里程碑规划 (动态更新)
    ├── DECISIONS.md          # 架构决策记录 (ADR 强溯源, 长期累积)
    ├── ISSUES.md             # 已知缺陷与技术风险跟踪 (动态更新)
    ├── sessions/             # 结构化会话沉淀记录 (追加模式, 定期压缩)
    ├── proposals/            # 协议改进提案 (追加模式)
    ├── .cache/               # (可选) 派生索引与缓存目录 (git 忽略)
    └── PROJECT_CONTEXT.md / PROJECT_CONTEXT_ZH.md   # (可选) 项目定制使用版
```

---

## 🔄 核心工作流程

```text
1. 开发者发出指令 ──► 2. AI 确定生效协议 ──► 3. 查阅 PROJECT.md & 状态任务快照
                                                                │
                                                                ▼
6. 沉淀会话与更新状态 ◄── 5. 代码实现与测试验证 ◄── 4. 检索 DECISIONS.md 推进任务
```

### 常用人类交互提示词 (Standard Prompts)

在任何 AI 智能体对话框中，可直接使用以下标准化指令：

* **项目初始化**：
  > `请读取 PROJECT_CONTEXT_ZH.md，初始化本项目的 ai/ 上下文管理体系并评估当前项目状态。`
* **跨会话 / 换新 AI 接管**：
  > `请读取 PROJECT_CONTEXT_ZH.md 接管项目，按必读顺序查阅 ai/PROJECT.md、ai/STATE.md 和 ai/TASK.md，列出未决问题后继续推进当前任务。`
* **只读状态与一致性诊断**：
  > `请读取 PROJECT_CONTEXT_ZH.md，评估项目当前状态与架构一致性，分析代码与文档是否存在脱节。不要修改代码。`
* **方案规划与 ADR 决策提议**：
  > `请读取 PROJECT_CONTEXT_ZH.md，结合 ai/PLAN.md 提出下一步开发计划或架构方案建议。不要修改代码。`
* **会话收尾与沉淀**：
  > `请按照 PCMP 协议规范收尾当前会话：验证产物，在 ai/sessions/ 沉淀会话记录，更新 ai/STATE.md 和 ai/TASK.md，新决定登记到 ai/DECISIONS.md（未确认标 Proposed）。`

---

## 🛠️ 推荐搭配工具：STC (Simplified Technical Chinese)

PCMP 推荐搭配 [STC (简体技术中文规范)](https://github.com/daimonia-ai/STC-Simplified-Technical-Chinese) 作为中文工程文档与人机对话的规范工具。

### 安装与使用命令
在项目中按需安装并初始化 STC 规则：
```bash
# 1. 安装 STC 命令行与规则工具
npm install -D @daimonia/stc@latest

# 2. 初始化项目规则（确认后写入默认规则到 AGENTS.md）
npx stc init --defaults

# 3. 命令行检查中文文本规范
npx stc check <文件路径>
```

### 推荐实践：材料审阅授权准则
* **审阅授权准则（PCMP 推荐项）**：**审阅、审计或样式检查的材料由人类指定或显式授权挑选**；未获用户明确许可前，AI 不得擅自扫描全工程扩大审阅范围。

### 许可证与署名说明 (License & Attribution)
STC 项目遵循开源双许可协议：
* 写作规则与词表采用 [CC BY 4.0 国际许可协议 (Creative Commons Attribution 4.0 International)](https://creativecommons.org/licenses/by/4.0/)；
* 命令行工具与代码采用 [MIT License](https://opensource.org/licenses/MIT)；
* 版权所有 (c) 2026 Daimonia (杭州代梦智能科技有限公司)。在引用、集成或分发时需保留原作者版权声明及许可链接。

---

## 🏷️ 版本与发布

* **当前版本**：V2.1
* **更新内容**：
  - 引入能力边界声明（Non-promises）与冲突分级核验机制；
  - 规范 Frontmatter 变更标记（`revision`）与信息分层标注（`[事实]/[假设]/[提议]/[已确认]`）；
  - 架构决策记录（ADR）增加强制确认来源追溯；
  - 确立无历史记忆的新 Agent“恢复测试”验收标准；
  - 规范派生索引层（SQLite 缓存）的只读可重建性与 `.gitignore` 策略；
  - 增加推荐搭配技术中文工具（STC）安装使用说明、开源许可署名与材料审阅授权准则。
