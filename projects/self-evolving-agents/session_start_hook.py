#!/usr/bin/env python3
"""
会话开始钩子 (Session Start Hook)
每次新会话开始时自动执行，回顾最近的情况。
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 工作目录
WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
PROJECT_DIR = WORKSPACE / "projects" / "self-evolving-agents"
TASKS_FILE = PROJECT_DIR / "tasks.json"
MEMORY_FILE = WORKSPACE / "MEMORY.md"


def get_recent_memory_files(days=2):
    """获取最近几天的记忆文件"""
    memory_files = []
    today = datetime.now()
    
    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        memory_file = MEMORY_DIR / f"{date_str}.md"
        if memory_file.exists():
            memory_files.append(memory_file)
    
    return memory_files


def read_memory_file(file_path):
    """读取记忆文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取失败: {e}"


def get_tasks():
    """获取任务列表"""
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"tasks": []}


def get_pending_tasks(tasks):
    """获取待办任务"""
    pending = []
    for task in tasks.get("tasks", []):
        if task.get("status") in ["pending", "in-progress"]:
            pending.append(task)
    
    # 按优先级排序
    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    pending.sort(key=lambda x: priority_order.get(x.get("priority", "P2"), 99))
    
    return pending


def extract_recent_summary(memory_content, lines=20):
    """从记忆内容中提取最近的摘要"""
    lines_list = memory_content.split('\n')
    recent_lines = lines_list[-lines:] if len(lines_list) > lines else lines_list
    return '\n'.join(recent_lines)


def generate_greeting():
    """生成问候语"""
    now = datetime.now()
    hour = now.hour
    
    if hour < 12:
        greeting = "早上好"
    elif hour < 18:
        greeting = "下午好"
    else:
        greeting = "晚上好"
    
    date_str = now.strftime("%Y年%m月%d日")
    return f"{greeting}，教授。今天是{date_str}。"


def main():
    """主函数"""
    print("=" * 60)
    print("📋 会话开始钩子 - 状态更新")
    print("=" * 60)
    print()
    
    # 1. 问候
    print(generate_greeting())
    print()
    
    # 2. 最近的记忆
    print("--- 📝 最近的记忆 ---")
    recent_files = get_recent_memory_files(days=2)
    
    if recent_files:
        for memory_file in recent_files:
            print(f"\n📄 {memory_file.name}:")
            content = read_memory_file(memory_file)
            summary = extract_recent_summary(content, lines=15)
            print(summary)
    else:
        print("没有找到最近的记忆文件")
    print()
    
    # 3. 待办任务
    print("--- 🎯 待办任务 ---")
    tasks = get_tasks()
    pending = get_pending_tasks(tasks)
    
    if pending:
        print(f"\n共有 {len(pending)} 个待办任务：")
        for i, task in enumerate(pending[:5], 1):  # 只显示前5个
            status_emoji = "🔄" if task.get("status") == "in-progress" else "📌"
            priority_emoji = "🔴" if task.get("priority") == "P0" else "🟡" if task.get("priority") == "P1" else "🟢"
            print(f"{i}. {status_emoji} {priority_emoji} [{task.get('priority')}] {task.get('title')}")
            print(f"   描述: {task.get('description', '无描述')[:50]}...")
        
        if len(pending) > 5:
            print(f"\n... 还有 {len(pending) - 5} 个任务")
    else:
        print("没有待办任务")
    print()
    
    # 4. 下一步建议
    print("--- 💡 下一步建议 ---")
    if pending:
        highest_priority = pending[0]
        print(f"\n建议先处理优先级最高的任务：")
        print(f"🎯 {highest_priority.get('title')}")
        print(f"   {highest_priority.get('description', '无描述')}")
    else:
        print("\n没有待办任务，可以开始新的工作！")
    
    print()
    print("=" * 60)
    print("会话开始钩子执行完毕。接下来想做什么？")
    print("=" * 60)


if __name__ == "__main__":
    main()
