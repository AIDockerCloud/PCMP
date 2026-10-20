# 工程智能体规范 (AGENTS.md - Lite)

## 项目定位
本项目采用 **PCMP Lite** 极简上下文管理协议：**纯 Markdown 驱动、零工具依赖、单目录自足**。

## 关键路径
- 项目硬约束：[ai/PROJECT.md](ai/PROJECT.md)
- 状态与活动任务：[ai/STATE.md](ai/STATE.md)（接管必读，已合并活动任务）
- 决策真源：[ai/DECISIONS.md](ai/DECISIONS.md)

## 智能体协作守则
1. **接管必读**：换新会话必须首选通读 `ai/PROJECT.md` 与 `ai/STATE.md`，明确当前活动任务与硬约束后再动工；
2. **状态合一**：Lite 档位无需维护独立 `TASK.md`，任务进展、验收勾选与 Next Action 直接维护在 `ai/STATE.md` 中；
3. **决策留痕**：重大技术选型或依赖引入必须在 `ai/DECISIONS.md` 追加记录，并附带人类确认来源；
4. **收尾更新**：任务完成后递增 `ai/STATE.md` 的 `revision`，更新完成项与即时下一步。
