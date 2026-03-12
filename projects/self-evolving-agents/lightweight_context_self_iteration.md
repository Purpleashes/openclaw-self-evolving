
# 轻量级上下文自迭代方案

**日期**: 2026-03-11  
**项目**: Self-Evolving Agents  
**原则**: 不冗余系统模块，不强行融合机制，轻量、非侵入式

---

## 核心理念

**"贴心的助手，而非霸道的管家"**

- ✅ 默默地观察，但不强行干预
- ✅ 适当地提示，但不啰嗦
- ✅ 悄悄地理财，但不炫耀
- ✅ 基于实际数据调整，而不是预设规则

---

## 方案概览

| 优化项 | 现有模块 | 轻量级改进 | 难度 |
|--------|---------|-----------|------|
| 渐进式记忆披露 | start_task.py | 先展示 Hot，需要时再展示 Warm/Cold | 低 |
| 高质量记忆筛选 | memory_search | 优先展示高 access_count + 成功的记忆 | 低 |
| 温和的层级调整 | memory_access_hook.py | 积累数据后，慢慢调整层级 | 中 |
| 闲置深度整理 | HEARTBEAT.md + memory_refinement.py | 闲置时段才做深度整理 | 低 |
| 数据观察面板 | 新建简单脚本 | 展示记忆使用数据，不自动优化 | 低 |

---

## 1. 渐进式记忆披露

### 修改：start_task.py

**目标**: 先只展示 Hot 记忆，任务进行中如果需要，再逐步展示 Warm 和 Cold

**具体修改**:
```python
# 在 start_task.py 的 display_experiences() 中

# 修改前：展示所有相关经验（最多 3 个）
related = find_related_experiences(...)
display_experiences(related)

# 修改后：
# 1. 先只展示 Hot 记忆
hot_experiences = [exp for exp in related if exp.get("access_count", 0) >= 5]
if hot_experiences:
    print("\n🔥 Hot Memories (High Priority):")
    display_experiences(hot_experiences[:2])  # 最多 2 个

# 2. 提示还有 Warm 记忆可以查看
warm_experiences = [exp for exp in related if 2 <= exp.get("access_count", 0) < 5]
if warm_experiences:
    print(f"\n💡 还有 {len(warm_experiences)} 个 Warm 记忆可用，需要时告诉我")
```

**为什么这样改？**
- ✅ 不冗余，只是调整展示逻辑
- ✅ 不强行融合，只是分阶段披露
- ✅ 轻量，用户体验更好，不会信息过载

---

## 2. 高质量记忆筛选

### 修改：find_related_experiences()（在 start_task.py 中）

**目标**: 优先展示 access_count 高、之前任务成功的记忆

**具体修改**:
```python
# 在 find_related_experiences() 中

# 修改前：只按时间倒序排序
related.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

# 修改后：按质量排序
def experience_quality_score(exp):
    """计算经验质量分数"""
    score = 0
    # access_count 高加分
    score += exp.get("access_count", 0) * 10
    # 成功的经验加分
    if exp.get("outcome") == "success":
        score += 50
    # 近期的经验加分
    # ... 可以加时间因子
    return score

related.sort(key=experience_quality_score, reverse=True)
```

**为什么这样改？**
- ✅ 不冗余，只是调整排序逻辑
- ✅ 不强行融合，只是给经验打分
- ✅ 轻量，优先展示高质量的记忆，效果更好

---

## 3. 温和的层级调整

### 新建：memory_tier_suggestions.py（注意是 suggestions，不是自动调整）

**目标**: 只给出层级调整建议，不自动调整，让用户决定

**具体实现**:
```python
#!/usr/bin/env python3
"""
记忆层级建议（只建议，不自动调整）
"""

import json
from pathlib import Path
from datetime import datetime

def analyze_memory_tiers():
    """分析记忆使用情况，给出层级调整建议"""
    access_counts_file = Path("/root/.openclaw/workspace/memory/access_counts.json")
    
    if not access_counts_file.exists():
        print("❌ 没有访问计数数据")
        return
    
    with open(access_counts_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    suggestions = []
    
    for exp_id, exp_data in data.get("experiences", {}).items():
        current_tier = exp_data.get("tier", "cold")
        access_count = exp_data.get("count", 0)
        
        # 给出建议，但不自动调整
        suggested_tier = current_tier
        if access_count >= 5 and current_tier != "hot":
            suggested_tier = "hot"
            suggestions.append(f"🔥 {exp_id}: {current_tier} → hot (access_count={access_count})")
        elif 2 <= access_count < 5 and current_tier == "cold":
            suggested_tier = "warm"
            suggestions.append(f"💡 {exp_id}: cold → warm (access_count={access_count})")
    
    print("📊 记忆层级分析")
    print("=" * 60)
    
    if suggestions:
        print("\n💡 层级调整建议（不自动调整，请手动决定）:")
        for suggestion in suggestions:
            print(f"  {suggestion}")
    else:
        print("\n✅ 无需调整")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    analyze_memory_tiers()
```

**为什么这样设计？**
- ✅ 不冗余，只是分析和建议
- ✅ 不强行融合，只建议，不自动调整
- ✅ 轻量，用户保持控制权

---

## 4. 闲置深度整理

### 修改：HEARTBEAT.md + memory_refinement.py

**目标**: 在闲置时段才做深度整理，工作时间不打扰

**具体修改**:

#### 4.1 在 HEARTBEAT.md 中添加闲置时段检测
```
## 闲置时段深度整理
- 如果连续 1 小时没有活动 → 自动运行 memory_refinement.py refine_memory
- 在凌晨 2:00-4:00 之间 → 自动运行 memory_refinement.py refine_memory
- 其他时间 → 只运行 idle_organization（轻量化整理）
```

#### 4.2 在 memory_refinement.py 中保持两种模式
- **idle_organization()**: 轻量化整理，随时可以运行
- **refine_memory()**: 深度整理，只在闲置时段运行

**为什么这样改？**
- ✅ 不冗余，只是添加时间判断
- ✅ 不强行融合，只在合适的时间做合适的事
- ✅ 轻量，工作时间不打扰，闲置时间悄悄整理

---

## 5. 数据观察面板

### 新建：memory_insights.py（只展示数据，不自动优化）

**目标**: 展示记忆使用的洞察，让用户了解情况，但不自动优化

**具体实现**:
```python
#!/usr/bin/env python3
"""
记忆洞察面板（只展示数据，不自动优化）
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def show_memory_insights():
    """展示记忆使用洞察"""
    access_counts_file = Path("/root/.openclaw/workspace/memory/access_counts.json")
    
    if not access_counts_file.exists():
        print("❌ 没有访问计数数据")
        return
    
    with open(access_counts_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("📊 记忆洞察面板")
    print("=" * 60)
    
    # 层级分布
    tiers = defaultdict(int)
    for exp_data in data.get("experiences", {}).values():
        tier = exp_data.get("tier", "cold")
        tiers[tier] += 1
    
    print(f"\n📁 层级分布:")
    print(f"  🔥 Hot: {tiers.get('hot', 0)}")
    print(f"  💡 Warm: {tiers.get('warm', 0)}")
    print(f"  📦 Cold: {tiers.get('cold', 0)}")
    
    # 访问计数统计
    access_counts = [exp.get("count", 0) for exp in data.get("experiences", {}).values()]
    if access_counts:
        avg_access = sum(access_counts) / len(access_counts)
        max_access = max(access_counts)
        print(f"\n📈 访问统计:")
        print(f"  平均: {avg_access:.1f} 次")
        print(f"  最高: {max_access} 次")
    
    # 最近访问
    print(f"\n⏰ 最近访问:")
    recent = []
    for exp_id, exp_data in data.get("experiences", {}).items():
        last_accessed = exp_data.get("last_accessed")
        if last_accessed:
            recent.append((last_accessed, exp_id))
    
    recent.sort(reverse=True)
    for last_accessed, exp_id in recent[:5]:
        print(f"  {last_accessed}: {exp_id}")
    
    print("\n" + "=" * 60)
    print("\n💡 提示：这只是数据展示，不会自动优化。")
    print("   如需调整，请手动操作。")

if __name__ == "__main__":
    show_memory_insights()
```

**为什么这样设计？**
- ✅ 不冗余，只是展示数据
- ✅ 不强行融合，只展示，不优化
- ✅ 轻量，用户保持完全控制权

---

## 实施计划

### 第 1 步：今天（最轻量）
1. ✅ 修改 start_task.py：渐进式记忆披露 + 高质量记忆筛选
2. ✅ 新建 memory_insights.py：数据观察面板

### 第 2 步：明天（轻量）
1. ✅ 新建 memory_tier_suggestions.py：层级建议（只建议，不调整）
2. ✅ 修改 HEARTBEAT.md：闲置时段深度整理

### 第 3 步：观察（不急于优化）
1. ✅ 运行 1-2 周，收集数据
2. ✅ 观察效果，再决定是否需要进一步优化

---

## 总结

### 核心原则

1. **不冗余系统模块** —— 所有改进都基于现有模块，只是调整逻辑
2. **不强行融合机制** —— 只建议、只展示、只在合适时间做，用户保持控制权
3. **轻量、非侵入式** —— 像贴心的助手，而不是霸道的管家

### 预期效果

- ✅ 用户体验更好（信息不过载，渐进式披露）
- ✅ 记忆质量更高（优先展示高质量记忆）
- ✅ 系统更智能（悄悄整理，不打扰）
- ✅ 用户保持控制（不自动调整，只展示数据和建议）

---

**方案创建日期**: 2026-03-11  
**创建人**: 柏林
