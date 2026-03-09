
#!/usr/bin/env python3
"""
Helper script to mark a task as completed
"""

import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task_manager import TaskManager

def main():
    if len(sys.argv) < 2:
        print("Usage: python complete_task.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    manager = TaskManager()
    
    if manager.complete_task(task_id):
        print(f"Task {task_id} marked as completed!")
        manager.print_status()
    else:
        print(f"Task {task_id} not found!")
        sys.exit(1)

if __name__ == "__main__":
    main()
