
#!/usr/bin/env python3
"""
Helper script to add a new task
"""

import sys
import os
import json
import argparse

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_manager import TaskManager

def get_result_json(task_id, title, description, priority, due, manager):
    """Get result as JSON"""
    # Find the task
    task = None
    for t in manager.data["tasks"]:
        if t["id"] == task_id:
            task = t
            break
    
    next_actions = [
        {
            "command": "start_task.py <task_id>",
            "description": "Start the new task",
            "params": {"task_id": task_id}
        },
        {
            "command": "task_manager.py",
            "description": "Check updated task status"
        },
        {
            "command": "add_task.py <title> <description> [priority] [due]",
            "description": "Add another task"
        }
    ]
    
    return {
        "ok": True,
        "command": f"add_task.py \"{title}\" \"{description}\" {priority} {due if due else ''}".strip(),
        "result": {
            "task_id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "due": due,
            "status": "backlog",
            "created_at": task.get("created") if task else None
        },
        "next_actions": next_actions
    }

def main():
    parser = argparse.ArgumentParser(description="Add a new task")
    parser.add_argument("title", help="Task title")
    parser.add_argument("description", help="Task description")
    parser.add_argument("priority", nargs="?", default="P2", help="Task priority (P0, P1, P2, P3)")
    parser.add_argument("due", nargs="?", help="Due date (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    manager = TaskManager()
    task_id = manager.add_task(args.title, args.description, args.priority, args.due)
    
    if args.json:
        result_json = get_result_json(task_id, args.title, args.description, args.priority, args.due, manager)
        print(json.dumps(result_json, indent=2, ensure_ascii=False))
        sys.exit(0)
    else:
        print(f"✅ Task {task_id} added!")
        manager.print_status()
        sys.exit(0)

if __name__ == "__main__":
    main()
