# PCMP Lite 样板工程 (Boilerplate)

这是 **PCMP Lite（极简 4 件套）** 的标准开箱范例。适用于个人独立开发、快速原型验证或小型脚本工具项目。

## 包含文件（仅 4 个核心文件）

```text
├── AGENTS.md            # 智能体通用工程入口与硬边界
└── ai/
    ├── PROJECT.md       # 项目宗旨、范围与硬约束
    ├── STATE.md         # 全局状态快照（已合并活动任务，免建 TASK.md）
    └── DECISIONS.md     # 架构决策记录 (ADR)
```

## 如何在新项目中使用？

1. 直接将本目录下的 `AGENTS.md` 与 `ai/` 文件夹复制到新项目根目录；
2. 依据你项目的实际情况修改 `ai/PROJECT.md` 与 `ai/STATE.md`；
3. 对 AI 助手（Cursor / Claude / Antigravity 等）说：
   > `请按本项目的 AGENTS.md 与 ai/STATE.md 接管开发任务。`
4. 纯 Markdown 驱动，无需安装 Python、无需配置数据库、无任何外部依赖。
