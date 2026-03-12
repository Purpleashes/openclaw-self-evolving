#!/usr/bin/env python3
"""
Lesson Check Hook System - Periodically check lessons directory for actionable insights
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class LessonCheckHook:
    def __init__(self, workspace_root="/root/.openclaw/workspace"):
        self.workspace_root = Path(workspace_root)
        self.lesson_dir = self.workspace_root / "memory" / "lessons"
        self.signals_dir = self.workspace_root / "memory" / "signals"
        
        # Create directories if they don't exist
        self.signals_dir.mkdir(parents=True, exist_ok=True)
    
    def load_all_lessons(self):
        """Load all lessons from the lessons directory"""
        lessons = []
        
        if not self.lesson_dir.exists():
            return lessons
        
        for lesson_file in self.lesson_dir.glob("*.jsonl"):
            try:
                with open(lesson_file, "r", encoding="utf-8") as f:
                    lesson = json.load(f)
                    lesson["_file"] = str(lesson_file)
                    lesson["_mtime"] = datetime.fromtimestamp(lesson_file.stat().st_mtime)
                    lessons.append(lesson)
            except Exception as e:
                print(f"⚠️  Warning: Could not load {lesson_file}: {e}")
        
        return lessons
    
    def check_duplicate_lessons(self, lessons):
        """Check for duplicate lessons by title or content"""
        duplicates = []
        title_map = defaultdict(list)
        content_map = defaultdict(list)
        
        for lesson in lessons:
            title = lesson.get("title", "").lower()
            if title:
                title_map[title].append(lesson)
            
            problem = lesson.get("problem", "").lower()
            solution = lesson.get("solution", "").lower()
            content_key = f"{problem}|{solution}"
            if content_key:
                content_map[content_key].append(lesson)
        
        # Check title duplicates
        for title, lesson_list in title_map.items():
            if len(lesson_list) > 1:
                duplicates.append({
                    "type": "duplicate_title",
                    "title": title,
                    "lessons": [l["_file"] for l in lesson_list]
                })
        
        # Check content duplicates
        for content_key, lesson_list in content_map.items():
            if len(lesson_list) > 1:
                duplicates.append({
                    "type": "duplicate_content",
                    "content_key": content_key[:100],
                    "lessons": [l["_file"] for l in lesson_list]
                })
        
        return duplicates
    
    def check_stale_lessons(self, lessons, days_threshold=30):
        """Check for lessons that haven't been accessed in a long time"""
        stale_lessons = []
        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        
        for lesson in lessons:
            mtime = lesson.get("_mtime")
            if mtime and mtime < cutoff_date:
                stale_lessons.append({
                    "type": "stale_lesson",
                    "title": lesson.get("title"),
                    "file": lesson["_file"],
                    "last_modified": mtime.strftime("%Y-%m-%d"),
                    "age_days": (datetime.now() - mtime).days
                })
        
        return stale_lessons
    
    def check_tag_distribution(self, lessons):
        """Check tag distribution and identify under-tagged lessons"""
        tag_stats = defaultdict(int)
        under_tagged = []
        
        for lesson in lessons:
            tags = lesson.get("tags", [])
            if not tags:
                under_tagged.append({
                    "type": "no_tags",
                    "title": lesson.get("title"),
                    "file": lesson["_file"]
                })
            else:
                for tag in tags:
                    tag_stats[tag] += 1
        
        return {
            "tag_distribution": dict(tag_stats),
            "under_tagged": under_tagged
        }
    
    def generate_signal(self, check_results):
        """Generate a signal file with check results"""
        signal = {
            "type": "lesson-check",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_lessons_checked": check_results.get("total_lessons", 0),
                "duplicates_found": len(check_results.get("duplicates", [])),
                "stale_lessons_found": len(check_results.get("stale_lessons", [])),
                "under_tagged_found": len(check_results.get("tag_analysis", {}).get("under_tagged", []))
            },
            "details": check_results
        }
        
        signal_file = self.signals_dir / f"lesson-check-{datetime.now().strftime('%Y%m%d-%H%M%S')}.jsonl"
        
        with open(signal_file, "w", encoding="utf-8") as f:
            json.dump(signal, f, ensure_ascii=False, indent=2)
        
        return signal_file
    
    def run_check(self, days_threshold=30):
        """Run the complete lesson check"""
        print("🔍 Running lesson check...")
        
        lessons = self.load_all_lessons()
        print(f"📚 Loaded {len(lessons)} lessons")
        
        duplicates = self.check_duplicate_lessons(lessons)
        stale_lessons = self.check_stale_lessons(lessons, days_threshold)
        tag_analysis = self.check_tag_distribution(lessons)
        
        check_results = {
            "total_lessons": len(lessons),
            "duplicates": duplicates,
            "stale_lessons": stale_lessons,
            "tag_analysis": tag_analysis,
            "check_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Generate signal
        signal_file = self.generate_signal(check_results)
        print(f"📡 Signal generated: {signal_file}")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 LESSON CHECK SUMMARY")
        print("="*60)
        print(f"Total lessons checked: {len(lessons)}")
        print(f"Duplicate lessons found: {len(duplicates)}")
        print(f"Stale lessons found: {len(stale_lessons)}")
        print(f"Under-tagged lessons found: {len(tag_analysis.get('under_tagged', []))}")
        
        if tag_analysis.get("tag_distribution"):
            print("\n🏷️  Tag Distribution:")
            for tag, count in sorted(tag_analysis["tag_distribution"].items(), key=lambda x: x[1], reverse=True):
                print(f"  {tag}: {count}")
        
        print("="*60)
        
        return check_results

def main():
    parser = argparse.ArgumentParser(description="Lesson Check Hook System")
    parser.add_argument("--days", type=int, default=30, help="Days threshold for stale lessons (default: 30)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    hook = LessonCheckHook()
    results = hook.run_check(days_threshold=args.days)
    
    if args.json:
        print(json.dumps({
            "ok": True,
            "results": results
        }, indent=2, ensure_ascii=False))
    else:
        print("\n✅ Lesson check complete!")

if __name__ == "__main__":
    main()
