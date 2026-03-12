
#!/usr/bin/env python3
"""
Active Task Scheduling System
Manages task backlog, prioritization, and status tracking
"""

import json
import os
from datetime import datetime

TASKS_FILE = "/root/.openclaw/workspace/projects/self-evolving-agents/tasks.json"


class TaskManager:
    def __init__(self, tasks_file=TASKS_FILE):
        self.tasks_file = tasks_file
        self.data = self._load_tasks()

    def _load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                return json.load(f)
        return {
            "version": "1.0",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "tasks": [],
            "metadata": {
                "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
                "totalTasks": 0,
                "completedTasks": 0,
                "inProgressTasks": 0,
                "backlogTasks": 0
            }
        }

    def _save_tasks(self):
        """Save tasks to JSON file"""
        self._update_metadata()
        with open(self.tasks_file, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def _update_metadata(self):
        """Update metadata counts"""
        tasks = self.data["tasks"]
        self.data["metadata"]["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
        self.data["metadata"]["totalTasks"] = len(tasks)
        self.data["metadata"]["completedTasks"] = len(
            [t for t in tasks if t["status"] == "completed"]
        )
        self.data["metadata"]["inProgressTasks"] = len(
            [t for t in tasks if t["status"] == "in-progress"]
        )
        self.data["metadata"]["backlogTasks"] = len(
            [t for t in tasks if t["status"] == "backlog"]
        )

    def get_next_task(self):
        """Get highest priority task that's not completed or in-progress"""
        priority_order = ["P0", "P1", "P2", "P3"]
        tasks = self.data["tasks"]

        for priority in priority_order:
            for task in tasks:
                if task["priority"] == priority and task["status"] == "backlog":
                    return task
        return None

    def start_task(self, task_id):
        """Mark a task as in-progress"""
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                task["status"] = "in-progress"
                task["startedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_tasks()
                return True
        return False

    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save_tasks()
                return True
        return False

    def add_task(self, title, description, priority="P2", due=None, tags=None):
        """Add a new task"""
        task_id = "task-%03d" % (len(self.data["tasks"]) + 1)
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "backlog",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "due": due,
            "tags": tags or []
        }
        self.data["tasks"].append(task)
        self._save_tasks()
        return task_id

    def list_tasks(self, status=None):
        """List tasks, optionally filtered by status"""
        tasks = self.data["tasks"]
        if status:
            return [t for t in tasks if t["status"] == status]
        return tasks

    def print_status(self):
        """Print current task status"""
        metadata = self.data["metadata"]
        print("📊 Task System Status")
        print("   Total: %d | Completed: %d | In Progress: %d | Backlog: %d" % (
            metadata['totalTasks'],
            metadata['completedTasks'],
            metadata['inProgressTasks'],
            metadata['backlogTasks']
        ))
        
        next_task = self.get_next_task()
        if next_task:
            print("\n🎯 Next Task: %s - %s" % (next_task['id'], next_task['priority']))
            print("   %s" % next_task['title'])
            print("   %s" % next_task['description'])


def get_status_json(manager):
    """Get task status as JSON"""
    metadata = manager.data["metadata"]
    next_task = manager.get_next_task()
    
    result = {
        "total_tasks": metadata["totalTasks"],
        "completed_tasks": metadata["completedTasks"],
        "in_progress_tasks": metadata["inProgressTasks"],
        "backlog_tasks": metadata["backlogTasks"],
    }
    
    if next_task:
        result["next_task"] = next_task
    
    next_actions = []
    if next_task:
        next_actions.append({
            "command": "start_task.py <task_id>",
            "description": "Start the next task",
            "params": {"task_id": next_task["id"]}
        })
    next_actions.append({
        "command": "add_task.py <title> <description> [priority] [due]",
        "description": "Add a new task"
    })
    
    return {
        "ok": True,
        "command": "task_manager.py",
        "result": result,
        "next_actions": next_actions
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Task Manager")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    manager = TaskManager()
    
    if args.json:
        status_json = get_status_json(manager)
        print(json.dumps(status_json, indent=2, ensure_ascii=False))
    else:
        manager.print_status()


if __name__ == "__main__":
    main()
