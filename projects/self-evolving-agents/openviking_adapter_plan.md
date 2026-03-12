
# OpenViking 适配器详细实施方案

**日期**: 2026-03-11  
**项目**: Self-Evolving Agents  
**目标**: 设计并实现 OpenViking 适配器的详细方案

---

## 1. 整体架构

```
┌─────────────────────────────────────────────────────────┐
│              我们的现有系统（上层）                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│  │ start_task.py│  │complete_task.│  │memory_   │ │
│  │              │  │py            │  │search    │ │
│  └──────┬───────┘  └──────┬───────┘  └────┬─────┘ │
└─────────┼───────────────────┼───────────────────┼───────┘
          │                   │                   │
┌─────────▼───────────────────▼───────────────────▼───────┐
│              OpenViking 适配器层（中间层）              │
│  ┌──────────────────────────────────────────────────┐   │
│  │         OpenVikingAdapter (主类)                │   │
│  │  - import_experiences()                          │   │
│  │  - export_experiences()                          │   │
│  │  - search_memory()                               │   │
│  │  - get_hot_memories()                           │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────┐  ┌──────────────────┐          │
│  │ ExperienceAdapter │  │  MemoryTierAdapter│          │
│  └──────────────────┘  └──────────────────┘          │
└───────────────────────┬───────────────────────────────┘
                        │
┌───────────────────────▼───────────────────────────────┐
│              OpenViking 底层（下层）                  │
│  ┌──────────────────────────────────────────────────┐ │
│  │  OpenViking Python API / CLI                    │ │
│  │  - SyncOpenViking / AsyncOpenViking             │ │
│  │  - add_resource()                                │ │
│  │  - search()                                      │ │
│  └──────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘
```

---

## 2. 目录结构

```
projects/self-evolving-agents/
├── openviking_adapter/          # 新：OpenViking 适配器目录
│   ├── __init__.py
│   ├── adapter.py              # 主适配器类
│   ├── experience_adapter.py   # 经验文件适配器
│   ├── tier_adapter.py         # 记忆分层适配器
│   └── config.py               # 适配器配置
├── memory_access_hook.py       # 现有：保持不变
├── memory_flushing.py          # 现有：保持不变
├── signal_capture.py           # 现有：保持不变
└── ...
```

---

## 3. 核心类设计

### 3.1 OpenVikingAdapter（主适配器类）

**文件**: `openviking_adapter/adapter.py`

```python
import openviking as ov
from pathlib import Path
from typing import List, Dict, Any
import json

class OpenVikingAdapter:
    """
    主适配器类，协调我们的系统与 OpenViking 之间的交互
    """
    
    def __init__(self, workspace_root="/root/.openclaw/workspace"):
        self.workspace_root = Path(workspace_root)
        self.experience_dir = self.workspace_root / "memory" / "experiences"
        
        # OpenViking 配置
        self.ov_path = self.workspace_root / "openviking_data"
        self.client = None
        self.initialized = False
    
    def initialize(self):
        """初始化 OpenViking 客户端"""
        try:
            self.client = ov.SyncOpenViking(path=str(self.ov_path))
            self.client.initialize()
            self.initialized = True
            print("✅ OpenViking 初始化成功")
            return True
        except Exception as e:
            print(f"❌ OpenViking 初始化失败: {e}")
            return False
    
    def import_experiences(self, dry_run=False):
        """
        将我们的经验文件导入到 OpenViking
        
        Args:
            dry_run: 是否只是模拟，不实际修改
            
        Returns:
            导入的经验数量
        """
        if not self.initialized:
            print("❌ 请先初始化 OpenViking")
            return 0
        
        imported_count = 0
        
        # 遍历所有经验文件
        for exp_file in self.experience_dir.glob("*-experience.jsonl"):
            try:
                with open(exp_file, 'r', encoding='utf-8') as f:
                    exp_data = json.load(f)
                
                task_id = exp_data.get("task_id")
                if not task_id:
                    continue
                
                # 构建 OpenViking URI
                tier = exp_data.get("access_count", 1)
                tier_folder = "cold"
                if tier >= 5:
                    tier_folder = "hot"
                elif tier >= 2:
                    tier_folder = "warm"
                
                ov_uri = f"viking://experiences/{tier_folder}/{task_id}.md"
                
                # 构建文件内容
                content = self._format_experience_content(exp_data)
                
                if not dry_run:
                    # 实际导入到 OpenViking
                    self.client.add_resource(uri=ov_uri, content=content)
                
                imported_count += 1
                print(f"✅ 导入: {task_id} → {ov_uri}")
                
            except Exception as e:
                print(f"⚠️ 导入失败 {exp_file.name}: {e}")
        
        print(f"\n✅ 导入完成，共 {imported_count} 个经验")
        return imported_count
    
    def _format_experience_content(self, exp_data: Dict[str, Any]) -> str:
        """将经验数据格式化为 Markdown 内容"""
        lines = []
        lines.append(f"# {exp_data.get('task_title', 'Untitled')}")
        lines.append("")
        lines.append(f"**任务 ID**: {exp_data.get('task_id')}")
        lines.append(f"**类型**: {exp_data.get('task_type', 'general')}")
        lines.append(f"**结果**: {exp_data.get('outcome', 'unknown')}")
        lines.append(f"**时间**: {exp_data.get('timestamp', 'Unknown')}")
        lines.append(f"**访问次数**: {exp_data.get('access_count', 1)}")
        lines.append("")
        
        if exp_data.get('context'):
            lines.append("## 上下文")
            lines.append(exp_data.get('context'))
            lines.append("")
        
        if exp_data.get('key_insights'):
            lines.append("## 关键洞察")
            for insight in exp_data.get('key_insights', []):
                lines.append(f"- {insight}")
            lines.append("")
        
        if exp_data.get('reusable_strategies'):
            lines.append("## 可重用策略")
            for strategy in exp_data.get('reusable_strategies', []):
                lines.append(f"- {strategy}")
            lines.append("")
        
        return "\n".join(lines)
    
    def search_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        在 OpenViking 中搜索记忆
        
        Args:
            query: 搜索查询
            limit: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        if not self.initialized:
            print("❌ 请先初始化 OpenViking")
            return []
        
        # TODO: 实现实际的搜索逻辑
        # 这需要根据 OpenViking 的实际 API 来实现
        print(f"🔍 搜索: {query}")
        return []
    
    def get_hot_memories(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        获取 Hot 记忆
        
        Args:
            limit: 返回结果数量
            
        Returns:
            Hot 记忆列表
        """
        if not self.initialized:
            print("❌ 请先初始化 OpenViking")
            return []
        
        # TODO: 从 OpenViking 的 hot/ 目录获取
        print(f"🔥 获取 Hot 记忆（前 {limit} 个）")
        return []
```

---

### 3.2 ExperienceAdapter（经验文件适配器）

**文件**: `openviking_adapter/experience_adapter.py`

```python
import json
from pathlib import Path
from typing import Dict, Any

class ExperienceAdapter:
    """
    经验文件适配器：在我们的 JSONL 格式与 OpenViking 的 Markdown 格式之间转换
    """
    
    @staticmethod
    def jsonl_to_markdown(exp_data: Dict[str, Any]) -> str:
        """将经验 JSONL 转换为 Markdown"""
        lines = []
        lines.append(f"# {exp_data.get('task_title', 'Untitled')}")
        lines.append("")
        
        # 元数据
        lines.append("---")
        lines.append(f"task_id: {exp_data.get('task_id')}")
        lines.append(f"task_type: {exp_data.get('task_type', 'general')}")
        lines.append(f"outcome: {exp_data.get('outcome', 'unknown')}")
        lines.append(f"timestamp: {exp_data.get('timestamp', 'Unknown')}")
        lines.append(f"access_count: {exp_data.get('access_count', 1)}")
        lines.append("---")
        lines.append("")
        
        # 内容
        if exp_data.get('context'):
            lines.append("## 上下文")
            lines.append(exp_data.get('context'))
            lines.append("")
        
        if exp_data.get('key_insights'):
            lines.append("## 关键洞察")
            for insight in exp_data.get('key_insights', []):
                lines.append(f"- {insight}")
            lines.append("")
        
        if exp_data.get('reusable_strategies'):
            lines.append("## 可重用策略")
            for strategy in exp_data.get('reusable_strategies', []):
                lines.append(f"- {strategy}")
            lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def markdown_to_jsonl(markdown_content: str) -> Dict[str, Any]:
        """将 Markdown 转换回经验 JSONL（可选，用于反向同步）"""
        # TODO: 实现从 Markdown 解析回 JSONL 的逻辑
        return {}
```

---

### 3.3 MemoryTierAdapter（记忆分层适配器）

**文件**: `openviking_adapter/tier_adapter.py`

```python
from typing import Dict, Any

class MemoryTierAdapter:
    """
    记忆分层适配器：在我们的 Hot/Warm/Cold 与 OpenViking 的目录结构之间映射
    """
    
    # 层级阈值
    TIER_THRESHOLDS = {
        "hot": 5,      # ≥ 5 次访问 → Hot
        "warm": 2,     # 2-4 次访问 → Warm
        "cold": 1      # 1 次访问 → Cold
    }
    
    @staticmethod
    def access_count_to_tier(access_count: int) -> str:
        """根据访问次数确定层级"""
        if access_count >= MemoryTierAdapter.TIER_THRESHOLDS["hot"]:
            return "hot"
        elif access_count >= MemoryTierAdapter.TIER_THRESHOLDS["warm"]:
            return "warm"
        else:
            return "cold"
    
    @staticmethod
    def tier_to_folder(tier: str) -> str:
        """将层级映射到目录名"""
        return tier
    
    @staticmethod
    def experience_to_uri(task_id: str, access_count: int) -> str:
        """生成经验的 OpenViking URI"""
        tier = MemoryTierAdapter.access_count_to_tier(access_count)
        folder = MemoryTierAdapter.tier_to_folder(tier)
        return f"viking://experiences/{folder}/{task_id}.md"
```

---

## 4. 分阶段实施计划

### 阶段 1: 基础框架（今天）
1. ✅ 创建适配器目录结构
2. ✅ 实现 `MemoryTierAdapter`（最简单，先做这个）
3. ✅ 实现 `ExperienceAdapter` 的 jsonl_to_markdown 方法
4. ✅ 创建 `OpenVikingAdapter` 骨架

### 阶段 2: 导入功能（明天）
1. ✅ 实现 `OpenVikingAdapter.initialize()`
2. ✅ 实现 `OpenVikingAdapter.import_experiences()`
3. ✅ 测试导入 1-2 个经验文件
4. ✅ 验证文件在 OpenViking 中正确创建

### 阶段 3: 搜索功能（后天）
1. ✅ 研究 OpenViking 的搜索 API
2. ✅ 实现 `OpenVikingAdapter.search_memory()`
3. ✅ 集成到我们的 `memory_search` 流程
4. ✅ 测试端到端搜索

### 阶段 4: 完整集成（下周）
1. ✅ 实现反向同步（从 OpenViking 导回）
2. ✅ 集成到 `start_task.py` 和 `complete_task.py`
3. ✅ 性能测试和优化
4. ✅ 文档完善

---

## 5. 使用示例

### 5.1 初始化适配器

```python
from openviking_adapter import OpenVikingAdapter

# 创建适配器
adapter = OpenVikingAdapter()

# 初始化 OpenViking
if adapter.initialize():
    print("✅ 适配器就绪")
```

### 5.2 导入经验

```python
# 导入所有经验（Dry Run，先看看会发生什么）
adapter.import_experiences(dry_run=True)

# 确认没问题后，实际导入
adapter.import_experiences(dry_run=False)
```

### 5.3 搜索记忆

```python
# 搜索记忆
results = adapter.search_memory("记忆机制优化", limit=5)
for result in results:
    print(f"📄 {result.get('title')}")
```

### 5.4 获取 Hot 记忆

```python
# 获取 Hot 记忆
hot_memories = adapter.get_hot_memories(limit=3)
for memory in hot_memories:
    print(f"🔥 {memory.get('title')}")
```

---

## 6. 回退方案

如果适配器出现问题，我们可以随时回退：

1. **停止使用适配器** —— 直接使用我们的原生系统
2. **删除 OpenViking 数据** —— `rm -rf ~/.openclaw/workspace/openviking_data`
3. **恢复原生代码** —— 我们的原有代码都没动，随时可以用

---

## 7. 总结

这个适配器方案的核心优势：
- ✅ **保持我们的优化层不变** —— Iteration 016-019 的成果都保留
- ✅ **灵活切换底层** —— 可以随时换用其他记忆系统
- ✅ **低风险** —— 分阶段实施，有问题随时回退
- ✅ **清晰的架构** —— 每一层责任明确，易于维护

---

**方案创建日期**: 2026-03-11  
**创建人**: 柏林
