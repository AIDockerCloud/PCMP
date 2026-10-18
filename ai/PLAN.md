---
pcmp_version: "2.1"
revision: 1
updated: 2026-10-19
---

# 高阶路线图与规划 (PLAN.md)

## 当前阶段 (Current Phase)
- **阶段**：Phase 1 — 协议核心规范确立与基础工具原型建设。
- **目标**：完成 PCMP v2.1 协议规范手册、初始化工程自身上下文体系，并完成方案 A 的 SQLite 索引层工具实现。

## 里程碑规划 (Milestones)
- [x] **M1 (已完成)**：PCMP v1.0 协议规范初版发布并开源提交。
- [x] **M2 (已完成)**：升级至 PCMP v2.1，引入能力边界、冲突分级核验、信息分层标注、恢复测试与 STC 推荐准则。
- [x] **M3 (已完成)**：建立 `.gitignore` 规则，净化工作区，配置推送至远程仓库。
- [x] **M4 (已完成)**：按规范完成本工程自身 `ai/` 上下文体系的首次初始化。
- [ ] **M5 (进行中)**：实现方案 A 的 Python 3 SQLite 派生索引工具 (`scripts/pcmp_index.py`)。
- [ ] **M6 (规划中)**：增加自动化恢复测试验证脚本或 CLI 扩展，提升多项目复用能力。

## 近期计划 (Next Steps)
1. 编写与调试 `scripts/pcmp_index.py`；
2. 验证 `--rebuild`、`--status`、`--search` 等常用指令；
3. 更新会话记录并归档至 `ai/sessions/`。
