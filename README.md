# OpenClaw Self-Evolving Project

> **"为记忆而生，为计划而活"** — Berlin, the AI Crime Artist

基于 OpenClaw 平台的自进化智能体项目。通过迭代、反思和自我改进机制，构建能够自主进化的智能体系统。

**项目负责人**: 张小全 | **创建日期**: 2026年3月

---

## 核心特性

- **自进化架构**: 迭代驱动、反思机制、任务管理
- **三层记忆系统**:
  - **P0（永久）**: 核心身份、永久偏好、关键关系
  - **P1（90天TTL）**: 活跃项目、团队、日程
  - **P2（30天TTL）**: 临时笔记、调试信息
- **访问频率分层**: Hot（高频）/ Warm（中频）/ Cold（低频）双重过滤
- **可解释检索**: 语义搜索 + 关键词匹配，展示检索理由
- **信号捕获**: 自动记录任务完成、工具使用、用户反馈
- **经验管理**: 任务经验自动提炼与重用
- **动态精炼**: 相似记忆合并、归档优化、闲置时段整理
- **任务追踪**: JSON-based 任务管理系统
- **智能体**: Berlin - 优雅又危险的犯罪艺术家

---

## 记忆系统机制

### 三层时间分层
- **P0（永久）**: 不随时间过期的核心记忆（身份、偏好、关系）
- **P1（90天TTL）**: 90天自动过期（活跃项目、团队、日程）
- **P2（30天TTL）**: 30天自动过期（临时笔记、调试信息）

### 双重分层过滤
- **时间层**: 基于TTL自动管理
- **频率层**: Hot（高频）/ Warm（中频）/ Cold（低频）
  - Hot: 最近7天访问 > 3次
  - Warm: 最近30天访问 1-3次
  - Cold: 访问 < 1次或长期未访问

### 核心功能模块

**记忆管理脚本** (`projects/self-evolving-agents/scripts/`)
- `memory_helper.py` - 添加记忆条目
- `memory_refinement.py` - 动态精炼相似记忆
- `memory_access_hook.py` - 访问频率追踪
- `signal_capture.py` - 自动信号捕获
- `experience_hook.py` - 任务经验提炼
- `lesson_check_hook.py` - 教训检查与去重

**记忆存储结构**
```
memory/
├── YYYY-MM-DD.md          # 每日会话记录
├── MEMORY.md              # 长期记忆（P0/P1/P2）
├── lessons/               # 结构化教训
├── experiences/           # 任务经验
└── signals/               # 系统信号
```

### 可解释检索
- 支持语义搜索（memory_search）+ 关键词匹配
- 展示检索理由（类型匹配、关键词匹配）
- 可视化检索轨迹，降低心智负担

---

## 项目结构

```
openclaw-self-evolving/
├── memory/                    # 记忆系统
│   ├── YYYY-MM-DD.md          # 每日会话记录
│   ├── MEMORY.md              # 长期记忆（三层架构）
│   ├── lessons/               # 结构化教训
│   ├── experiences/           # 任务经验库
│   └── signals/               # 系统信号
├── projects/self-evolving-agents/  # 自进化代理项目
│   ├── tasks.json            # 任务管理系统
│   ├── scripts/              # 记忆与任务脚本
│   ├── iterations/           # 迭代记录
│   ├── daily-reports/        # 每日分析报告
│   └── research-notes/       # 研究笔记
├── skills/                    # OpenClaw 技能库
│   ├── adaptive-learning-agents/
│   ├── multi-search-engine/
│   └── playwright-scraper-skill/
├── reports/                   # 项目报告
├── AGENTS.md                 # 工作流程（中文）
└── project-memory/           # 项目进展追踪
```

**关键目录说明**:
- `memory/`: 记忆存储核心，支持时间分层、频率分层、语义检索
- `projects/self-evolving-agents/`: 核心开发区
  - `scripts/`: 记忆管理、任务管理、信号捕获脚本
  - `iterations/`: 每次迭代的完整记录
  - `research-notes/`: 技术调研与迭代设计
  - `daily-reports/`: 每日工作总结

---

## 快速开始

### 前置要求
- Python 3.8+
- OpenClaw CLI
- Claude API Key

### 安装
```bash
git clone <repository-url>
cd openclaw-self-evolving
openclaw setup
```

### 使用
```bash
cd projects/self-evolving-agents
python3 task_manager.py      # 查看任务
python3 start_task.py task-XXX    # 开始任务
python3 complete_task.py task-XXX # 完成任务

# 记忆管理
python3 memory_helper.py P0 "永久记忆内容"
python3 memory_helper.py P1 "短期记忆内容" --date 2026-03-12
```

---

## 文档

### 核心文档
- [AGENTS.md](AGENTS.md) - 工作流程与核心原则
- [SOUL.md](SOUL.md) - 智能体行为准则
- [IDENTITY.md](IDENTITY.md) - 智能体身份信息

### 项目文档
- [PROJECT_MEMORY/PROGRESS.md](project-memory/PROGRESS.md) - 项目进展报告
- [README_SCRIPTS.md](projects/self-evolving-agents/README_SCRIPTS.md) - 脚本使用指南
- [ITERATION_TRACKING.md](projects/self-evolving-agents/ITERATION_TRACKING.md) - 迭代追踪
- [ITERATION_EVALUATION_CRITERIA.md](projects/self-evolving-agents/ITERATION_EVALUATION_CRITERIA.md) - 评估标准

### 研究笔记
- [research-notes/day-04-pai-memory-analysis.md](projects/self-evolving-agents/research-notes/day-04-pai-memory-analysis.md) - PAI记忆系统分析
- [research-notes/day-08-memory-mechanism-self-iteration.md](projects/self-evolving-agents/research-notes/day-08-memory-mechanism-self-iteration.md) - 记忆机制迭代研究
- [research-notes/memory-system-changes-summary.md](projects/self-evolving-agents/research-notes/memory-system-changes-summary.md) - 记忆系统变化总结
- [research-notes/day-12-openviking-memory-advantages-research.md](projects/self-evolving-agents/research-notes/day-12-openviking-memory-advantages-research.md) - OpenViking记忆机制研究

---

## 项目状态

✅ 基础架构搭建完成
✅ 三层记忆系统（P0/P1/P2）
✅ 访问频率分层（Hot/Warm/Cold）
✅ 任务管理系统实现
✅ 信号捕获与经验提炼
✅ 可解释检索机制
🔄 混合检索开发
📋 自适应学习优化

---

**MIT License**
