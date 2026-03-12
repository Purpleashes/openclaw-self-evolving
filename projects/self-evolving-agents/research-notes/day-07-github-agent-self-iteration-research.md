
# Day 07: GitHub上Agent自我迭代进化项目研究总结

**日期**: 2026-03-10  
**项目**: Self-Evolving Agents  
**研究目标**: 从GitHub上的优秀开源项目获取agent自我迭代进化方面的信息，总结关键洞察

---

## 1. 研究背景

根据用户要求，我们将GitHub作为推进项目研究的重要渠道之一。本次研究重点关注两个GitHub上的优秀开源项目：
1. **modelscope/AgentEvolver** - 高效的自进化Agent系统
2. **karpathy/autoresearch** - AI agent自动运行LLM训练研究

---

## 2. modelscope/AgentEvolver 项目分析

### 2.1 项目概述
- **项目名称**: AgentEvolver: Towards Efficient Self-Evolving Agent System
- **GitHub地址**: https://github.com/modelscope/AgentEvolver
- **核心定位**: 端到端的自进化训练框架，将自我提问、自我导航和自我归因统一为一个连贯的系统

### 2.2 三大自我进化机制（核心亮点）

#### 机制1: Automatic Task Generation (Self-Questioning)
- **功能**: 探索环境，自主创建多样化任务
- **优势**: 消除了昂贵的手动数据集构建
- **借鉴意义**: 我们可以考虑添加自主任务生成机制，让系统自动识别需要改进的领域

#### 机制2: Experience-guided Exploration (Self-Navigating)
- **功能**: 总结和重用跨任务经验，指导更高质量的rollouts
- **优势**: 提高探索效率
- **借鉴意义**: 我们的记忆系统已经有类似思路，但可以进一步加强经验的总结和重用

#### 机制3: Attribution-based Credit Assignment (Self-Attributing)
- **功能**: 处理长轨迹，揭示中间步骤的因果贡献
- **优势**: 实现细粒度、高效的策略优化
- **借鉴意义**: 这是我们目前缺少的，可以考虑添加归因分析机制

### 2.3 架构设计
- **服务导向的数据流架构**
- **环境兼容性**: 标准化接口，无缝集成各种外部环境和工具API
- **灵活的上下文管理器**: 内置工具管理多轮上下文和复杂交互逻辑
- **模块化和可扩展架构**: 解耦组件，便于定制、二次开发和未来算法升级

### 2.4 基准性能
- 在AppWorld和BFCL-v3基准上取得了优异结果
- 使用比更大基线模型少得多的参数，实现了更好的性能
- 例如：AgentEvolver (7B) 在AppWorld上达到32.4% avg@8，在BFCL v3上达到57.9% avg@8

---

## 3. karpathy/autoresearch 项目分析

### 3.1 项目概述
- **项目名称**: AI agents running research on single-GPU nanochat training automatically
- **GitHub地址**: https://github.com/karpathy/autoresearch
- **核心定位**: 给AI agent一个小但真实的LLM训练环境，让它在夜间自主实验

### 3.2 核心理念
> "One day, frontier AI research used to be done by meat computers... That era is long gone. Research is now entirely the domain of autonomous swarms of AI agents running across compute cluster megastructures in the skies."
> — @karpathy, March 2026

### 3.3 工作原理
1. **准备阶段**: 人类设置好`program.md`（agent的指令）
2. **自主实验**: Agent修改`train.py`，训练5分钟，检查结果是否改进，保留或丢弃，重复
3. **结果**: 第二天早上，人类查看实验日志和（希望）更好的模型

### 3.4 关键设计选择
1. **单个文件修改**: Agent只修改`train.py`，保持范围可控，差异可审查
2. **固定时间预算**: 训练总是运行恰好5分钟，确保实验直接可比
3. **自包含**: 除了PyTorch和几个小包外，没有外部依赖

### 3.5 项目结构
```
prepare.py      — 常量、数据准备+运行时工具（不修改）
train.py        — 模型、优化器、训练循环（agent修改这个）
program.md      — agent指令（人类修改这个）
pyproject.toml  — 依赖
```

---

## 4. 对我们项目的关键借鉴

### 4.1 从AgentEvolver借鉴
1. **添加自我任务生成机制** - 让系统自动识别需要改进的领域，创建自主任务
2. **加强经验导航** - 更好地总结和重用跨任务经验
3. **考虑添加归因分析** - 分析长轨迹中各步骤的因果贡献

### 4.2 从autoresearch借鉴
1. **固定时间预算的实验** - 为我们的迭代设置固定时间预算，确保实验可比
2. **单文件修改模式** - 考虑将我们的迭代范围限制在可控范围内
3. **人类-机器协作模式** - 人类设置高层指令（program.md），agent执行具体实验

### 4.3 综合建议
- 我们可以结合两者的优势：AgentEvolver的三大机制 + autoresearch的自主实验模式
- 考虑创建我们自己的"program.md"风格的指令文件，用于指导agent的自我迭代
- 添加实验日志系统，记录每次迭代的详细信息

---

## 5. 下一步行动计划

1. **短期（1-2天）**:
   - 深入阅读AgentEvolver的技术报告（arXiv:2511.10395）
   - 分析autoresearch的`program.md`和`train.py`结构
   - 考虑在我们的项目中添加固定时间预算的实验机制

2. **中期（3-5天）**:
   - 设计我们自己的自我任务生成机制
   - 加强经验导航和重用机制
   - 创建实验日志系统

3. **长期（1周+）**:
   - 考虑实现归因分析机制
   - 探索多agent协作的自我进化模式
   - 建立完整的自主实验框架

---

**研究总结完成日期**: 2026-03-10  
**创建人**: 柏林
