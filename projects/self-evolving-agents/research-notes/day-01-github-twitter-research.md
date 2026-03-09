
# Day 1 补充调研：X/Twitter + GitHub热门agent应用调研简报

## GitHub热门agent项目分析（按Star排序）

### 1. EvoMap/evolver（1.3k stars，昨日更新）
- **核心功能**：基于GEP（Genome Evolution Protocol）的协议约束型自我进化引擎
- **痛点解决**：将临时的prompt调整转化为可审计、可重用的进化资产
- **关键特性**：
  - 自动日志分析：扫描记忆和历史文件中的错误和模式
  - 自我修复指导：从信号中发出修复导向的指令
  - GEP协议：标准化的进化与可重用资产
  - 突变与个性进化：每次进化运行都由显式突变对象和可进化个性状态控制
  - 可配置策略预设：EVOLVE_STRATEGY=balanced|innovate|harden|repair-only控制意图平衡
- **适用场景**：
  - 大规模维护agent prompt和日志的团队
  - 需要可审计进化痕迹（基因、胶囊、事件）的用户
  - 需要确定性、协议绑定变更的环境
- **不适用场景**：
  - 没有日志或历史的一次性脚本
  - 需要自由形式创意变更的项目
  - 无法容忍协议开销的系统

### 2. jihe520/social-push（256 stars，3天前更新）
- **核心功能**：AI社交媒体自动化skill，基于agent-browser实现自动化发布内容到各大社交平台
- **痛点解决**：传统脚本难以应对页面复杂变化，Playwright MCP消耗大量token且慢
- **关键特性**：
  - AI驱动的智能交互：无需硬编码选择器，AI自动理解页面元素，抗改版能力强
  - Self-Evolution（自我进化）：网页改版后可自动检测并修复workflow，无需手动维护代码
  - Markdown即配置：添加新平台只需创建一个markdown文件，无需编写复杂脚本
  - 自动保存登录状态：使用--state参数保持会话，一次登录永久有效
  - 可视化操作：浏览器对用户可见（--headed模式），方便调试和监控
  - 安全设计：仅暂存草稿，不自动发布，由用户最终确认
- **支持平台**：小红书（图文/长文）、X/Twitter、知乎、微博、微信公众号、掘金等

### 3. JARVIS-Xs/SE-Agent（238 stars，2025-09-23更新）
- **核心功能**：LLM Code agent的自我进化框架，通过Revision、Recombination、Refinement三个核心自我进化操作实现轨迹级进化，跨推理路径交换信息
- **关键特性**：
  - **Revision**：通过深度自我反思和针对性改进分析单个失败轨迹，创建架构正交的问题解决范式
  - **Recombination**：通过智能组合多个现有解决方案路径的优势创建新轨迹
  - **Refinement**：通过消除冗余和使用整个轨迹池的见解优化有希望的轨迹
- **性能**：在SWE-bench Verified上达到80% Top1性能
- **技术栈**：Python

### 4. XMUDeepLIT/Awesome-Self-Evolving-Agents（45 stars，2小时前更新）
- **核心功能**：自我进化agent的精选资源列表（调查、论文、基准、开源项目）
- **价值**：一站式获取自我进化agent的所有相关资源

---

## 初步发现与可借鉴点
1. **协议约束型进化**：EvoMap/evolver的GEP协议提供了安全、可审计的进化框架，可借鉴到我们的自我迭代中
2. **自动日志分析**：EvoMap/evolver的自动日志分析功能与我们当前的每日反思章节互补，可进一步优化
3. **可重用进化资产**：将临时调整转化为可重用的基因和胶囊，提高进化效率

---

## 后续计划
1. 深入分析EvoMap/evolver的GEP协议细节
2. 继续调研X/Twitter上的讨论（等agent-browser安装完成后）
3. 识别我们自身机制的可进化点
