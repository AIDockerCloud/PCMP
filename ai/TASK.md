---
pcmp_version: "2.2"
revision: 6
updated: 2026-10-20
---

# 当前唯一活动任务 (TASK.md)

## 当前任务与核心目标 (Current Task & Objective)
- **任务名称**：落实 Alice 二次评审深度治理：ADR 全量回填、强硬化校验、CI 闭环与 Lite 样板。
- **核心目标**：全面补齐历史 ADR 字段（DEC-001~004），将 `--check` 弱校验升格为强硬化拦截（包含脚本副本一致性与双语标题对称性），接入 GitHub Actions CI，提供 `examples/lite/` 开箱工程并补齐编码规范。

## 背景与范围 (Why & Scope)
- **背景**：解决协议从“结构设计完成”到“落地执行深度”存在的 5 个遗留断点，消除荣誉制依赖与重复真源漂移。
- **范围**：包括 `ai/DECISIONS.md`、`scripts/pcmp_index.py`、`tests/test_pcmp_index.py`、`.github/workflows/ci.yml`、`examples/lite/`、`AGENTS.md`。

## 约束与非目标 (Constraints & Non-Goals)
- **硬约束**：Python 脚本严格依赖标准库，零 pip 依赖，单文件自足；Lite 样例必须真实可运行且零工具依赖；必须遵循 STC 规范。
- **非目标**：暂不拆分多仓库。

## 关联关键文件 (Relevant Files)
- `ai/DECISIONS.md`：历史 ADR 字段回填与 DEC-006
- `scripts/pcmp_index.py` & `skills/pcmp/scripts/pcmp_index.py`：硬化校验实现与双副本镜像
- `tests/test_pcmp_index.py`：单元测试用例
- `.github/workflows/ci.yml`：GitHub Actions 持续集成工作流
- `examples/lite/`：开箱样板工程全套文件
- `AGENTS.md`：代码规范补充

## 验收结果 (Acceptance Result)
- [x] 全量回填 DEC-001 至 DEC-004 的 `Supersedes`、`Superseded-by` 与 `复审触发条件`，登记 DEC-006；
- [x] 强化 `scripts/pcmp_index.py --check`：将 ADR 与 TASK 字段缺失设为 error，增加脚本双副本 SHA-256 镜像比对与双语标题对称性校验；
- [x] 扩展 `tests/test_pcmp_index.py` 单元测试套件（8/8 项测试全部通过）；
- [x] 接入 GitHub Actions CI 工作流（`.github/workflows/ci.yml`），自动化运行 unittest 与 `--check`；
- [x] 创建 `examples/lite/` 完整可运行样板工程（含 4 件套及 README 说明）；
- [x] 在 `AGENTS.md` 补齐 Python 脚本编码约束；
- [x] 更新 `README.md` 索引并沉淀会话记录。

## 即时动作 (Immediate Next Action)
- 运行 `python3 scripts/pcmp_index.py --update` 与 `python3 scripts/pcmp_index.py --check`，执行本地 Git 提交并向用户汇报。
