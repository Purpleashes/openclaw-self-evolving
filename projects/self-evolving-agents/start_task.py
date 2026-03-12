
#!/usr/bin/env python3
"""
Helper script to mark a task as in-progress
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_manager import TaskManager
from memory_access_hook import MemoryAccessHook

def load_experiences(experience_dir="/root/.openclaw/workspace/memory/experiences"):
    """Load all experiences from the experience directory"""
    experiences = []
    if os.path.exists(experience_dir):
        for filename in os.listdir(experience_dir):
            if filename.endswith("-experience.jsonl"):
                filepath = os.path.join(experience_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        experience = json.load(f)
                        experiences.append(experience)
                except Exception as e:
                    print(f"⚠️  Warning: Could not load experience {filename}: {e}")
    return experiences

def find_related_experiences(task, experiences, memory_hook=None):
    """Find experiences related to the current task and increment their access counts"""
    related = []
    seen_task_ids = set()  # 用于去重
    task_tags = task.get("tags", [])
    task_type = task_tags[0] if task_tags else "general"
    task_title = task.get("title", "").lower()
    
    for exp in experiences:
        task_id = exp.get("task_id")
        
        # 去重：如果已经处理过这个 task_id，跳过
        if task_id in seen_task_ids:
            continue
        
        # 收集检索理由
        retrieval_reasons = []
        
        # Match by task type
        exp_type = exp.get("task_type", "general")
        if exp_type == task_type:
            retrieval_reasons.append(f"类型匹配: {task_type}")
        
        # Check keyword matches (only match if keyword is in the experience)
        exp_title = exp.get("task_title", "").lower()
        matching_keywords = []
        for keyword in ["research", "test", "script", "skill", "memory", "iteration", "optimize", "analysis"]:
            if keyword in exp_title:  # 只匹配经验标题中包含的关键词
                matching_keywords.append(keyword)
        
        if matching_keywords:
            retrieval_reasons.append(f"关键词匹配: {', '.join(matching_keywords)}")
        
        # 如果有匹配理由，就加入相关经验
        if retrieval_reasons:
            # 标记为已处理
            seen_task_ids.add(task_id)
            
            # 添加检索理由到经验对象
            exp_with_reasons = exp.copy()
            exp_with_reasons["_retrieval_reasons"] = retrieval_reasons
            related.append(exp_with_reasons)
    
    # Increment access counts for related experiences using the memory hook
    if memory_hook:
        for exp in related:
            task_id = exp.get("task_id")
            if task_id:
                # Track access using the memory hook
                memory_hook.track_experience_access(task_id)
                
                # Also update the experience file's access_count for backward compatibility
                experience_file = Path("/root/.openclaw/workspace/memory/experiences") / f"{task_id}-experience.jsonl"
                if experience_file.exists():
                    with open(experience_file, 'r', encoding='utf-8') as f:
                        exp_data = json.load(f)
                    exp_data["access_count"] = exp_data.get("access_count", 0) + 1
                    with open(experience_file, 'w', encoding='utf-8') as f:
                        json.dump(exp_data, f, ensure_ascii=False, indent=2)
    
    # Return up to 3 most recent related experiences
    return sorted(related, key=lambda x: x.get("timestamp", ""), reverse=True)[:3]

def display_experiences(experiences):
    """Display related experiences in a user-friendly way (with retrieval reasons)"""
    if not experiences:
        print("📚 No related experiences found.")
        return
    
    print("\n📚 Related Experiences (with retrieval reasons):")
    print("=" * 60)
    for i, exp in enumerate(experiences, 1):
        # Get tier info
        access_count = exp.get('access_count', 1)
        tier = "🔥 Hot" if access_count >= 5 else "💡 Warm" if access_count >= 2 else "📦 Cold"
        
        print(f"\n{i}. {exp.get('task_title', 'Untitled')} ({exp.get('timestamp', 'Unknown date')})")
        print(f"   {tier} | access_count={access_count} | Outcome: {exp.get('outcome', 'unknown')}")
        
        # Show retrieval reasons
        retrieval_reasons = exp.get('_retrieval_reasons', [])
        if retrieval_reasons:
            print(f"   💡 检索理由:")
            for reason in retrieval_reasons:
                print(f"      - {reason}")
        
        # Show key insights and strategies
        if exp.get('key_insights'):
            print(f"   📝 Key Insights: {', '.join(exp.get('key_insights')[:2])}")
        if exp.get('reusable_strategies'):
            print(f"   🎯 Reusable Strategies: {', '.join(exp.get('reusable_strategies')[:2])}")
    print("\n" + "=" * 60)

def get_result_json(task_id, success, manager=None):
    """Get result as JSON"""
    if success:
        # Find the task
        task = None
        for t in manager.data["tasks"]:
            if t["id"] == task_id:
                task = t
                break
        
        next_actions = [
            {
                "command": "complete_task.py <task_id>",
                "description": "Complete the task when done",
                "params": {"task_id": task_id}
            },
            {
                "command": "task_manager.py",
                "description": "Check updated task status"
            }
        ]
        
        return {
            "ok": True,
            "command": f"start_task.py {task_id}",
            "result": {
                "task_id": task_id,
                "status": "in-progress",
                "started_at": task.get("startedAt") if task else None
            },
            "next_actions": next_actions
        }
    else:
        return {
            "ok": False,
            "command": f"start_task.py {task_id}",
            "error": f"Task {task_id} not found!",
            "next_actions": [
                {
                    "command": "task_manager.py",
                    "description": "Check available tasks"
                }
            ]
        }

def main():
    parser = argparse.ArgumentParser(description="Mark a task as in-progress")
    parser.add_argument("task_id", help="Task ID to start")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    task_id = args.task_id
    manager = TaskManager()
    success = manager.start_task(task_id)
    
    # If task started successfully, load and display related experiences
    if success and not args.json:
        # Find the task
        task = None
        for t in manager.data["tasks"]:
            if t["id"] == task_id:
                task = t
                break
        if task:
            # Initialize memory access hook
            memory_hook = MemoryAccessHook()
            
            # Load and display related experiences
            experiences = load_experiences()
            related = find_related_experiences(task, experiences, memory_hook)
            display_experiences(related)
    
    if args.json:
        result_json = get_result_json(task_id, success, manager)
        print(json.dumps(result_json, indent=2, ensure_ascii=False))
        sys.exit(0 if success else 1)
    else:
        if success:
            print(f"\nTask {task_id} marked as in-progress!")
            manager.print_status()
            sys.exit(0)
        else:
            print(f"Task {task_id} not found!")
            sys.exit(1)

if __name__ == "__main__":
    main()
