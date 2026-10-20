---
pcmp_version: "2.2"
revision: 5
updated: 2026-10-20
---

# 当前唯一活动任务 (TASK.md)

## 当前任务与核心目标 (Current Task & Objective)
- **任务名称**：PCMP 治理通胀瘦身与自动化健全性强校验实现。
- **核心目标**：落地用户提出的 5 项核心治理建议，推出 PCMP Lite 与 Full 双档位，重构瘦身 AGENTS.md，强化 TASK.md 与 ADR Schema，实现 `scripts/pcmp_index.py --check` 自动化合规检查与测试套件，发布 PCMP v2.2。

## 背景与范围 (Why & Scope)
- **背景**：解决个人/小型项目应用 PCMP 时的治理通胀问题，消除 AGENTS.md 中规则失衡问题，建立机器级合规防线。
- **范围**：涵盖协议双语原版、索引工具校验逻辑、单元测试套件、AGENTS.md、官方 Skill 以及本仓库 dogfooding 记录。

## 约束与非目标 (Constraints & Non-Goals)
- **硬约束**：严格遵循 STC 规范；严禁破坏 PCMP“纯 Markdown 驱动一切”的初心；派生工具与 SQLite 始终保持为纯可选加速层，禁止使核心规范对 Python 脚本产生硬依赖。
- **非目标**：暂不拆分多仓库（维持单仓库分层架构，等待生态成熟）。

## 关联关键文件 (Relevant Files)
- `PROJECT_CONTEXT_ZH.md` / `PROJECT_CONTEXT.md`：核心通用协议原版
- `AGENTS.md`：智能体通用工程入口与硬事实
- `scripts/pcmp_index.py` & `tests/test_pcmp_index.py`：派生合规校验与测试
- `skills/pcmp/SKILL.md`：官方技能定义与斜杠命令
- `ai/DECISIONS.md` / `ai/STATE.md` / `ai/TASK.md`：本仓库自举上下文

## 验收结果 (Acceptance Result)
- [x] 在 `scripts/pcmp_index.py` 中实现 `check_compliance()` 与 `--check` 命令行开关；
- [x] 在 `tests/test_pcmp_index.py` 编写完整单元测试，验证通过（5/5 测试通过）；
- [x] 重构瘦身 `AGENTS.md`，精简中文写作规则至链接/回执要求，增加 15 行工程硬事实、常用命令与红线禁区；
- [x] 在 `PROJECT_CONTEXT_ZH.md` 与 `PROJECT_CONTEXT.md` 确立 PCMP Lite（极简 4 件套）与 Full 档位规范；
- [x] 强化 ADR Schema（增加 `Supersedes`、`Superseded-by`、`复审触发条件`）与 `TASK.md` Schema（增加 `Constraints & Non-Goals`、`Relevant Files`）；
- [x] 升级 `skills/pcmp/SKILL.md`，增加 `/pcmp check` 指令与 Lite/Full 档位支持，并同步至 `.claude` 与 `.agents`；
- [x] 更新 `README.md`，介绍双档位与合规校验命令，发布 V2.2 版本说明；
- [x] 登记 ADR `DEC-005`，刷新 `ai/STATE.md` 与 `ai/TASK.md` 并沉淀会话记录。

## 即时动作 (Immediate Next Action)
- 运行 `pcmp_index.py --update` 与 `pcmp_index.py --check`，执行本地 Git 提交并向用户汇报。
