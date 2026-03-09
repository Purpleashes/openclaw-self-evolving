# MEMORY.md - Long-Term Memory
<!-- Format: [P0/P1/P2][YYYY-MM-DD] content -->
<!-- P0=永不过期, P1=90天, P2=30天 -->
<!-- Auto-managed by memory-janitor.py -->

## About User [P0]
- [P0] 用户: 李教授
- [P0] 项目: OpenClaw 记忆系统研究与维护
- [P0] 服务器: 118.196.93.33 (root)

## Key Relationships [P0]
- [P0] 周杰伦 - 客户/朋友, jay@example.com, 音乐人，喜欢吃辣，想学电子音乐
- [P0] 李教授 - Project Memory 负责人, prof.li@example.edu / 138-0000-0001
- [P0] 王五 - 朋友, 3 月 15 日生日，喜欢摄影，预算 5000 元

## Preferences [P0]
- [P0] 需要完整备份确保可以回退
- [P0] 重视记忆系统的稳定性和可恢复性
- [P0][2026-03-09] 网页搜索方案：停用 web_search 工具，改用 skills
  - ❌ 不再使用 web_search（需要API key且经常出错）
  - ✅ 使用 multi-search-engine（17个搜索引擎，无需API key）
  - ✅ 直接网页访问使用 web_fetch
  - ✅ 浏览器交互使用 agent-browser
  - ✅ 复杂网页抓取使用 playwright-scraper-skill

## Active Projects [P1]
- [P1][2026-03-05] Project Memory - 研究 OpenClaw 的长期记忆处理机制
- [P1][2026-03-05] Project Dialogue - 对话状态追踪，保持多轮对话上下文一致性
- [P1][2026-03-06] Project Self-Evolving Agents - Agent自我迭代与学习前沿技术研究
  - 技术方向: 大语言模型驱动的agent自我改进
  - 时间周期: 一周（2026-03-06至2026-03-12）
  - 输出形式:
    1. 每日研究过程文档（综述+技术）
    2. 每日自我迭代
    3. 最终完成自我迭代并总结迭代过程

## Project Teams [P1]
- [P1][2026-03-05] Project Dialogue 团队: 张三（算法）、李四（工程）、赵六（产品）

## Schedule [P1]
- [P1][2026-03-05] 下周三下午 3 点：和李教授开会（Project Memory）
- [P1][2026-03-05] 每周五下午 2 点：Project Dialogue 团队会议
- [P1][2026-03-05] 3 月 15 日：王五生日

## Temporary [P2]
- [P2][2026-03-05] 进行三层记忆系统融合实施
- [P2][2026-03-05] 配置 memory-janitor.py 自动归档脚本
- [P2][2026-03-09] 张洋铨消息自动回复机制已配置
- [P2][2026-03-09] 会话开始钩子自动化约定：每次新会话开始时，柏林主动运行 session_start_hook.py，自动展示状态更新

---
*Lessons & historical details: `memory/lessons/*.jsonl` + `memory/archive/`*
*Use `memory_search` to find archived content*
