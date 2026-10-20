---
pcmp_version: "2.2"
revision: 7
updated: 2026-10-20
---

# 当前唯一活动任务 (TASK.md)

## 当前任务与核心目标 (Current Task & Objective)
- **任务名称**：PCMP v2.2 终版收敛封板：单测守护 Lite 样板与双语校验口径诚实化。
- **核心目标**：将 `examples/lite/` 纳入单元测试与 CI 持续守护，诚实化修正双语校验口径（版本与章节骨架对齐），正式宣告 PCMP v2.2 协议封板，转向真实业务项目实践验证。

## 背景与范围 (Why & Scope)
- **背景**：采纳 Alice 第三轮评审意见，消除最后两处微瑕（样板纳检防腐化、校验口径严谨诚实），并恪守工程克制原则，立即冻结功能。
- **范围**：`tests/test_pcmp_index.py`、`scripts/pcmp_index.py`、`skills/pcmp/SKILL.md`、`README.md`。

## 约束与非目标 (Constraints & Non-Goals)
- **硬约束**：PCMP 核心规范冻结在 v2.2，不再扩张新字段或新功能；遵循 STC 规范。
- **非目标**：暂不进行 v2.3 开发。

## 关联关键文件 (Relevant Files)
- `tests/test_pcmp_index.py`：样板守护单测
- `scripts/pcmp_index.py` & `skills/pcmp/scripts/pcmp_index.py`：校验器与准确描述
- `skills/pcmp/SKILL.md` & `README.md`：文档口径对齐
- `examples/lite/`：受测样板工程

## 验收结果 (Acceptance Result)
- [x] 在 `tests/test_pcmp_index.py` 增加 `test_examples_lite_compliance`，让 CI 自动守护 `examples/lite/` 质量（9/9 测试全过）；
- [x] 准确修正双语校验口径为“中英双语版本与章节骨架对齐”，并在代码注释、CLI 描述与 README/Skill 中统一；
- [x] 运行全量单元测试与合规检查无任何错误；
- [x] 正式宣告 PCMP v2.2 封板完成。

## 即时动作 (Immediate Next Action)
- 提交本地变更，向用户交付封板总结。
