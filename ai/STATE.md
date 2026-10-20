---
pcmp_version: "2.2"
revision: 5
updated: 2026-10-20
---

# 项目当前状态快照 (STATE.md)

- **Last Updated**: 2026-10-20
- **Overall Status**: PCMP v2.2 正式发布，确立 Lite/Full 双档位，实现 `--check` 自动化合规检查与测试，完成 `AGENTS.md` 瘦身治理。

## 已完成 (Completed)
- [已确认] [DEC-001] 发布 PCMP v1.0 与升级至 v2.1 协议规范手册（双语版）。
- [已确认] 建立能力边界声明、冲突分级核验准则、信息分层标签与恢复测试标准。
- [已确认] 添加 `.gitignore`，安全忽略 `node_modules/`、`package*.json`、`.claude/`、`.agents/`、`ai/.cache/` 与 Python 缓存。
- [已确认] 补充推荐工具 STC 说明及材料审阅授权准则。
- [已确认] 成功向远端 GitHub 仓库推送 `main` 分支与 `v1.0.0` / `v2.1.0` 标签。
- [已确认] 完成 PCMP 本项目自身的 `ai/` 上下文目录初始化。
- [已确认] [DEC-002] 编写并落地方案 A 的 SQLite 派生索引工具 `scripts/pcmp_index.py`。
- [已确认] [DEC-003] 确立单仓库分层架构（方案 1），更新 README 突出“单文档开箱自举”指南。
- [已确认] [DEC-004] 推出官方 PCMP Skill (`skills/pcmp/`)，提供 `/pcmp init`、`/pcmp takeover`、`/pcmp finalize` 等快捷命令，并配置至 `.claude` 与 `.agents`。
- [已确认] [DEC-005] 引入 PCMP Lite 极简 4 件套与 Full 档位双轨标准，杜绝个人与小项目治理通胀。
- [已确认] 重构瘦身 `AGENTS.md`，精炼写作规则并注入 15 行工程硬事实、常用命令与红线禁区。
- [已确认] 强化 `TASK.md`（约束与非目标、关联文件）与 ADR Schema（Supersedes、被取代、复审触发条件）。
- [已确认] `scripts/pcmp_index.py` 新增 `--check` 自动化合规检查，并提供完整单元测试套件 `tests/test_pcmp_index.py`。
- [已确认] 升级 PCMP Skill 支持 `/pcmp check` 与分档初始化。

## 进行中 (In Progress)
- [无] 当前治理通胀瘦身与强校验任务已圆满完成。

## 阻塞项 (Blocked)
- 无

## 当前风险与焦点 (Current Risks & Focus)
- 确保外部使用者理解 Lite 与 Full 档位差异，优先在小项目中推广极简 4 件套。

## 下一步即时动作 (Immediate Next Action)
- 交付 PCMP v2.2 治理与强校验成果给用户。
