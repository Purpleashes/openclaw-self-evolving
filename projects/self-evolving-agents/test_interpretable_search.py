
#!/usr/bin/env python3
"""
测试可解释检索功能
"""

import sys
import os
import json
from pathlib import Path

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the functions from start_task.py
from start_task import load_experiences, find_related_experiences, display_experiences
from memory_access_hook import MemoryAccessHook

def test_interpretable_search():
    """测试可解释检索"""
    print("=" * 60)
    print("🔍 测试可解释检索功能")
    print("=" * 60)
    
    # 1. 加载经验
    print("\n📥 加载经验文件...")
    experiences = load_experiences()
    print(f"✅ 加载了 {len(experiences)} 个经验")
    
    # 2. 创建一个测试任务
    test_task = {
        "id": "test-001",
        "title": "Test: 可解释检索验证",
        "description": "这是一个测试任务，用于验证可解释检索的效果",
        "priority": "P2",
        "status": "pending",
        "created": "2026-03-11",
        "tags": ["research", "test", "memory", "iteration"]
    }
    
    # 3. 初始化 memory hook
    memory_hook = MemoryAccessHook()
    
    # 4. 查找相关经验（带检索理由）
    print("\n🔍 查找相关经验...")
    related = find_related_experiences(test_task, experiences, memory_hook=None)  # 不实际更新 access_count
    
    # 5. 展示结果（带检索理由）
    print("\n📊 展示结果（带检索理由）:")
    display_experiences(related)
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_interpretable_search()

