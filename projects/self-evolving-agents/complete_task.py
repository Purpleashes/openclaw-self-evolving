
#!/usr/bin/env python3
"""
Helper script to mark a task as completed
"""

import sys
import os
import json
import argparse
import time
from datetime import datetime

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_manager import TaskManager
from experience_hook import ExperienceHook
from signal_capture import SignalCapture

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
                "command": "task_manager.py",
                "description": "Check next task"
            },
            {
                "command": "add_task.py <title> <description> [priority] [due]",
                "description": "Add a new task"
            }
        ]
        
        return {
            "ok": True,
            "command": f"complete_task.py {task_id}",
            "result": {
                "task_id": task_id,
                "status": "completed",
                "completed_at": task.get("completedAt") if task else None
            },
            "next_actions": next_actions
        }
    else:
        return {
            "ok": False,
            "command": f"complete_task.py {task_id}",
            "error": f"Task {task_id} not found!",
            "next_actions": [
                {
                    "command": "task_manager.py",
                    "description": "Check available tasks"
                }
            ]
        }

def main():
    parser = argparse.ArgumentParser(description="Mark a task as completed")
    parser.add_argument("task_id", help="Task ID to complete")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    # Record start time for duration calculation
    start_time = time.time()
    
    task_id = args.task_id
    manager = TaskManager()
    success = manager.complete_task(task_id)
    
    # If task completed successfully, save experience and capture signal
    if success:
        # Find the task
        task = None
        for t in manager.data["tasks"]:
            if t["id"] == task_id:
                task = t
                break
        if task:
            # Process experience hook
            hook = ExperienceHook()
            result = hook.process_task_completion(task)
            
            # Capture task complete signal
            signal_capture = SignalCapture()
            duration_ms = int((time.time() - start_time) * 1000)
            signal_capture.capture_task_complete(
                task_id=task_id,
                task_title=task.get("title", "Untitled"),
                success=True,
                duration_ms=duration_ms,
                output_summary=f"Task {task_id} completed successfully",
                output_quality="good"
            )
            print(f"📡 Task complete signal captured")
    
    if args.json:
        result_json = get_result_json(task_id, success, manager)
        print(json.dumps(result_json, indent=2, ensure_ascii=False))
        sys.exit(0 if success else 1)
    else:
        if success:
            print(f"Task {task_id} marked as completed!")
            manager.print_status()
            sys.exit(0)
        else:
            print(f"Task {task_id} not found!")
            sys.exit(1)

if __name__ == "__main__":
    main()
