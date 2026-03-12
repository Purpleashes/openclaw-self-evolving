#!/usr/bin/env python3
"""
Experience Hook System - Enhanced experience saving with auto-lesson extraction
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

class ExperienceHook:
    def __init__(self, workspace_root="/root/.openclaw/workspace"):
        self.workspace_root = Path(workspace_root)
        self.experience_dir = self.workspace_root / "memory" / "experiences"
        self.lesson_dir = self.workspace_root / "memory" / "lessons"
        self.memory_file = self.workspace_root / "MEMORY.md"
        
        # Create directories if they don't exist
        self.experience_dir.mkdir(parents=True, exist_ok=True)
        self.lesson_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_lessons_from_experience(self, experience):
        """
        Automatically extract lessons from experience data
        Returns a list of lesson objects
        """
        lessons = []
        
        # Extract lessons from key insights
        for insight in experience.get("key_insights", []):
            lesson = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "title": f"洞察：{insight[:50]}...",
                "problem": "通过任务执行发现的新洞察",
                "solution": insight,
                "tags": ["insight", "auto-extracted"]
            }
            lessons.append(lesson)
        
        # Extract lessons from problems encountered and solutions applied
        problems = experience.get("problems_encountered", [])
        solutions = experience.get("solutions_applied", [])
        
        for i, problem in enumerate(problems):
            solution = solutions[i] if i < len(solutions) else "待定"
            lesson = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "title": f"问题解决：{problem[:50]}...",
                "problem": problem,
                "solution": solution,
                "tags": ["problem-solution", "auto-extracted"]
            }
            lessons.append(lesson)
        
        # Extract lessons from reusable strategies
        for strategy in experience.get("reusable_strategies", []):
            lesson = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "title": f"策略：{strategy[:50]}...",
                "problem": "需要可重用的执行策略",
                "solution": strategy,
                "tags": ["strategy", "auto-extracted", "reusable"]
            }
            lessons.append(lesson)
        
        return lessons
    
    def save_lesson(self, lesson, task_id):
        """Save a single lesson to the lessons directory"""
        lesson_file = self.lesson_dir / f"{datetime.now().strftime('%Y-%m-%d')}-{task_id}-lesson.jsonl"
        
        # Avoid duplicate filenames
        counter = 1
        while lesson_file.exists():
            lesson_file = self.lesson_dir / f"{datetime.now().strftime('%Y-%m-%d')}-{task_id}-lesson-{counter}.jsonl"
            counter += 1
        
        with open(lesson_file, "w", encoding="utf-8") as f:
            json.dump(lesson, f, ensure_ascii=False, indent=2)
        
        return lesson_file
    
    def update_memory_md(self, experience, lessons):
        """
        Update MEMORY.md with key information from the experience
        """
        if not self.memory_file.exists():
            return False
        
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                memory_content = f.read()
            
            # Add a P2 entry for the completed task
            today = datetime.now().strftime("%Y-%m-%d")
            task_entry = f"- [P2][{today}] {experience['task_title']} (经验已保存)\n"
            
            # Check if entry already exists
            if task_entry not in memory_content:
                # Find the Temporary section and add the entry
                temp_section = "## Temporary [P2]"
                if temp_section in memory_content:
                    new_content = memory_content.replace(
                        temp_section,
                        f"{temp_section}\n{task_entry}"
                    )
                    
                    with open(self.memory_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    
                    return True
            
            return False
        except Exception as e:
            print(f"⚠️  Warning: Could not update MEMORY.md: {e}")
            return False
    
    def process_task_completion(self, task):
        """
        Main hook function: process a completed task
        1. Save detailed experience
        2. Extract and save lessons
        3. Update MEMORY.md
        """
        print(f"🔄 Processing experience hook for task: {task['id']}")
        
        # 1. Save enhanced experience
        experience = self._create_enhanced_experience(task)
        experience_file = self._save_experience(experience)
        print(f"✅ Experience saved to: {experience_file}")
        
        # 2. Extract and save lessons
        lessons = self.extract_lessons_from_experience(experience)
        saved_lessons = []
        for lesson in lessons:
            lesson_file = self.save_lesson(lesson, task['id'])
            saved_lessons.append(lesson_file)
        
        if saved_lessons:
            print(f"✅ {len(saved_lessons)} lessons auto-extracted and saved")
        
        # 3. Update MEMORY.md
        if self.update_memory_md(experience, lessons):
            print(f"✅ MEMORY.md updated")
        
        return {
            "experience_file": str(experience_file),
            "lesson_files": [str(f) for f in saved_lessons]
        }
    
    def _create_enhanced_experience(self, task):
        """Create an enhanced experience object with more details"""
        experience = {
            "task_id": task.get("id"),
            "task_title": task.get("title"),
            "task_type": task.get("tags", ["general"])[0] if task.get("tags") else "general",
            "context": task.get("description"),
            "actions": [],
            "tools_used": [],
            "outcome": "success",
            "key_insights": [],
            "reusable_strategies": [],
            "problems_encountered": [],
            "solutions_applied": [],
            "user_feedback": "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "access_count": 1,
            "priority": task.get("priority", "P2"),
            "completed_at": task.get("completedAt")
        }
        
        # Auto-extract some insights based on task type
        task_title_lower = task.get("title", "").lower()
        
        if "lesson" in task_title_lower or "检查" in task_title_lower:
            experience["key_insights"].append("定期检查机制对于持续改进很重要")
            experience["reusable_strategies"].append("建立定期检查的任务调度机制")
        
        if "经验" in task_title_lower or "experience" in task_title_lower:
            experience["key_insights"].append("经验保存和重用是自我迭代的核心")
            experience["reusable_strategies"].append("任务完成后自动保存经验")
        
        if "记忆" in task_title_lower or "memory" in task_title_lower:
            experience["key_insights"].append("记忆分层管理提高检索效率")
            experience["reusable_strategies"].append("使用 P0/P1/P2 三层记忆架构")
        
        return experience
    
    def _save_experience(self, experience):
        """Save experience to file"""
        experience_file = self.experience_dir / f"{experience['task_id']}-experience.jsonl"
        with open(experience_file, "w", encoding="utf-8") as f:
            json.dump(experience, f, ensure_ascii=False, indent=2)
        return experience_file

def main():
    parser = argparse.ArgumentParser(description="Experience Hook System")
    parser.add_argument("task_id", help="Task ID to process")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    hook = ExperienceHook()
    manager = TaskManager()
    
    # Find the task
    task = None
    for t in manager.data["tasks"]:
        if t["id"] == args.task_id:
            task = t
            break
    
    if not task:
        print(f"❌ Task {args.task_id} not found!")
        sys.exit(1)
    
    # Process the task completion
    result = hook.process_task_completion(task)
    
    if args.json:
        print(json.dumps({
            "ok": True,
            "task_id": args.task_id,
            "result": result
        }, indent=2, ensure_ascii=False))
    else:
        print(f"\n🎉 Experience hook processing complete!")

if __name__ == "__main__":
    main()
