---
pcmp_version: "2.1"
revision: 4
updated: 2026-10-20
---

# 当前唯一活动任务 (TASK.md)

## 当前任务与核心目标 (Current Task & Objective)
- **任务名称**：将 PCMP 核心工作流封装为官方 Skill 并建立斜杠命令支持。
- **核心目标**：编写 `skills/pcmp/SKILL.md`，内嵌索引工具，配置本地 `.claude/skills/` 与 `.agents/skills/` 环境，在 `README.md` 与 `AGENTS.md` 中增加 Skill 支持说明。

## 验收结果 (Acceptance Result)
- [x] 编写完成 `skills/pcmp/SKILL.md`，提供 `/pcmp init`、`/pcmp takeover`、`/pcmp finalize`、`/pcmp adr`、`/pcmp assess`、`/pcmp index` 六大快捷命令；
- [x] 在 `skills/pcmp/scripts/` 中自包含内嵌 `pcmp_index.py` 脚本；
- [x] 配置同步至 `.claude/skills/pcmp` 与 `.agents/skills/pcmp`；
- [x] 更新 `AGENTS.md` 引用 PCMP Skill；
- [x] 更新 `README.md` 配套工具章节并展示 Skill 命令对照表；
- [x] 登记 ADR DEC-004。

## 即时动作 (Immediate Next Action)
- 交付 PCMP Skill 成果给用户。
