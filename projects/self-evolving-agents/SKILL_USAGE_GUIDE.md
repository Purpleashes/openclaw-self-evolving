
# Skill 使用指南

本指南提供了我们项目中常用skill的详细使用方法、示例和最佳实践。

---

## 目录
1. [multi-search-engine](#multi-search-engine) - 多搜索引擎集成（17个引擎，无需API key）
2. [agent-browser](#agent-browser) - 浏览器自动化
3. [playwright-scraper-skill](#playwright-scraper-skill) - 反爬保护的网页抓取
4. [summary-report](#summary-report) - 工作总结报告生成
5. [feishu-docs](#feishu-docs) - 飞书文档和wiki操作

---

## multi-search-engine

**用途**: 17个搜索引擎集成，无需API key，支持国内和国际搜索。

**搜索引擎列表**:
- **国内（8个）**: Baidu, Bing CN, Bing INT, 360, Sogou, WeChat, Toutiao, Jisilu
- **国际（9个）**: Google, Google HK, DuckDuckGo, Yahoo, Startpage, Brave, Ecosia, Qwant, WolframAlpha

**便捷脚本**: `/root/.openclaw/workspace/scripts/multi_search_helper.py`

### 使用方法

#### 1. 列出所有搜索引擎
```bash
python3 /root/.openclaw/workspace/scripts/multi_search_helper.py --list
```

#### 2. 使用指定搜索引擎搜索
```bash
python3 /root/.openclaw/workspace/scripts/multi_search_helper.py --engine baidu "搜索关键词"
```

#### 3. 获取搜索结果
使用 `web_fetch` 工具获取搜索结果：
```python
web_fetch({"url": "https://www.baidu.com/s?wd=搜索关键词"})
```

### 高级搜索技巧

| 技巧 | 示例 | 说明 |
|------|------|------|
| 站点搜索 | `site:github.com python` | 只在指定站点搜索 |
| 文件类型 | `filetype:pdf report` | 搜索指定文件类型 |
| 精确匹配 | `"machine learning"` | 精确匹配短语 |
| 排除词 | `python -snake` | 排除包含指定词的结果 |
| 时间过滤 | `tbs=qdr:w` | 过去一周的结果 |

### 隐私搜索引擎
- **DuckDuckGo**: 无跟踪
- **Startpage**: Google结果 + 隐私
- **Brave**: 独立索引
- **Qwant**: 欧盟GDPR合规

### WolframAlpha 知识查询
- 数学: `integrate x^2 dx`
- 转换: `100 USD to CNY`
- 股票: `AAPL stock`
- 天气: `weather in Beijing`

---

## agent-browser

**用途**: 快速的Rust无头浏览器自动化CLI，支持导航、点击、输入、截图等。

**安装**:
```bash
npm install -g agent-browser
agent-browser install
agent-browser install --with-deps
```

### 核心工作流
1. **导航**: `agent-browser open <url>`
2. **快照**: `agent-browser snapshot -i`（获取交互元素和refs）
3. **交互**: 使用快照中的refs进行操作
4. **重新快照**: 导航或DOM变化后重新快照

### 常用命令

#### 导航
```bash
agent-browser open <url>      # 打开URL
agent-browser back            # 后退
agent-browser forward         # 前进
agent-browser reload          # 刷新
agent-browser close           # 关闭浏览器
```

#### 快照（页面分析）
```bash
agent-browser snapshot            # 完整可访问性树
agent-browser snapshot -i         # 仅交互元素（推荐）
agent-browser snapshot -c         # 紧凑输出
agent-browser snapshot -d 3       # 限制深度为3
agent-browser snapshot -s "#main" # 限制到CSS选择器
```

#### 交互（使用快照中的@refs）
```bash
agent-browser click @e1           # 点击
agent-browser dblclick @e1        # 双击
agent-browser focus @e1           # 聚焦元素
agent-browser fill @e2 "text"     # 清空并输入
agent-browser type @e2 "text"     # 输入（不清空）
agent-browser press Enter         # 按键
agent-browser press Control+a     # 组合键
agent-browser hover @e1           # 悬停
agent-browser check @e1           # 勾选复选框
agent-browser uncheck @e1         # 取消勾选
agent-browser select @e1 "value"  # 选择下拉框
agent-browser scroll down 500     # 滚动页面
agent-browser scrollintoview @e1  # 滚动元素到视图
agent-browser drag @e1 @e2        # 拖放
agent-browser upload @e1 file.pdf # 上传文件
```

#### 获取信息
```bash
agent-browser get text @e1        # 获取元素文本
agent-browser get html @e1        # 获取innerHTML
agent-browser get value @e1       # 获取输入值
agent-browser get attr @e1 href   # 获取属性
agent-browser get title           # 获取页面标题
agent-browser get url             # 获取当前URL
agent-browser get count ".item"   # 统计匹配元素
agent-browser get box @e1         # 获取边界框
```

#### 截图和PDF
```bash
agent-browser screenshot          # 截图到stdout
agent-browser screenshot path.png # 保存到文件
agent-browser screenshot --full   # 全页面截图
agent-browser pdf output.pdf      # 保存为PDF
```

#### 等待
```bash
agent-browser wait @e1                     # 等待元素
agent-browser wait 2000                    # 等待毫秒
agent-browser wait --text "Success"        # 等待文本
agent-browser wait --url "/dashboard"    # 等待URL模式
agent-browser wait --load networkidle      # 等待网络空闲
agent-browser wait --fn "window.ready"     # 等待JS条件
```

### 示例：表单提交
```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# 输出显示: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # 检查结果
```

### JSON输出（用于解析）
添加 `--json` 获取机器可读输出：
```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

### 调试
```bash
agent-browser open example.com --headed              # 显示浏览器窗口
agent-browser console                                # 查看控制台消息
agent-browser errors                                 # 查看页面错误
agent-browser highlight @e1                          # 高亮元素
```

---

## playwright-scraper-skill

**用途**: 基于Playwright的网页抓取，具有反爬保护，成功测试于复杂站点如Discuss.com.hk。

**位置**: `/root/.openclaw/workspace/skills/playwright-scraper-skill-1.2.0`

### 使用方法
1. 读取SKILL.md获取详细使用说明
2. 按照skill文档中的步骤进行配置和使用

---

## summary-report

**用途**: 从会话历史生成工作总结报告，支持日报/周报，输出PDF。

**位置**: `/root/.openclaw/workspace/skills/summary-report`

### 约定
- **"生成每天的日报"** → 使用此skill生成通用工作总结报告（位于`reports/daily-YYYY-MM-DD.md`）
- **"项目的日报"** → 生成self-evolving-agents研究项目的进展日报（位于`projects/self-evolving-agents/daily-reports/day-XX-daily-analysis.md`）

---

## feishu-docs

**用途**: 飞书（Lark）文档和wiki操作，读取、创建、追加文档，管理wiki空间。

**位置**: `/root/.openclaw/workspace/skills/feishu-docs`

---

**创建日期**: 2026-03-10  
**创建人**: 柏林
