
# HEARTBEAT.md - Active Task Scheduling

## 🎯 Task-Driven Heartbeat Workflow

When this heartbeat triggers:

1. **First, check the task system** - Run the task manager to see what needs work
2. **Select highest priority task** - Always work on P0 tasks first, then P1, etc.
3. **Start the task** - Mark it as in-progress before beginning
4. **Execute the task** - Complete the actual work
5. **Mark as completed** - Update status when done
6. **Repeat** - If time allows, pick the next task

## 📋 Task Commands

To use the task system:
```bash
# Check status and see next task
python3 /root/.openclaw/workspace/projects/self-evolving-agents/task_manager.py

# Tasks are stored in:
/root/.openclaw/workspace/projects/self-evolving-agents/tasks.json
```

## 🔄 Workflow Reminder

Never let a day pass without active work. The task system exists to eliminate that.

## 📚 Lesson Check Reminder

**每两天检查一次lesson目录**：
- 检查任务：task-026（定期检查lesson目录）
- 下次检查时间：2026-03-13
