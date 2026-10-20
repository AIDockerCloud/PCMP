---
pcmp_version: "2.2"
revision: 1
updated: 2026-10-20
---

# 架构与技术决策记录 (DECISIONS.md - Lite)

## DEC-001 — 采用 Argon2id 作为用户密码哈希算法
日期: 2026-10-20 | 状态: Accepted
- 确认来源: 技术负责人在架构评审会中批准采纳
- Supersedes: 无
- Superseded-by: 无
- 复审触发条件 (Review Trigger): 当国际密码学标准发布更高安全性推荐，或硬件环境对内存开销产生严重限制时复审
- 背景 (Context): 系统需要存储用户认证密码，需抵御 GPU/ASIC 离线暴力破解与彩虹表攻击。
- 决策 (Decision): 采用 Argon2id 算法，配置内存参数 64MB、迭代次数 3、并行度 4 进行密钥派生。
- 理由 (Reason): Argon2 是密码哈希竞赛（PHC）优胜标准，Argon2id 兼具抵御侧信道攻击与 GPU 并行破解的最优平衡。
- 备选方案 (Alternatives): bcrypt (内存受限、截断 72 字节)、PBKDF2 (抵御 GPU 破解能力弱于现代算法)。
- 影响 (Consequences): 显著提升密码存储安全性；注册和校验时对单核 CPU 和内存有可量化消耗（约 50ms/次），需要结合速率限制防止资源耗尽。
