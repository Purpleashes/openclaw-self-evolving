
#!/usr/bin/env python3
"""
Helper script to update access counts for memory entries
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Define paths
ACCESS_COUNTS_FILE = Path("/root/.openclaw/workspace/memory/access_counts.json")
EXPERIENCES_DIR = Path("/root/.openclaw/workspace/memory/experiences")
LESSONS_DIR = Path("/root/.openclaw/workspace/memory/lessons")

def load_access_counts():
    """Load access counts from file"""
    if ACCESS_COUNTS_FILE.exists():
        with open(ACCESS_COUNTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "version": "1.0",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entries": {}
    }

def save_access_counts(data):
    """Save access counts to file"""
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ACCESS_COUNTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_experience_access_count(task_id):
    """Update access count for an experience"""
    # First, update the experience file itself
    experience_file = EXPERIENCES_DIR / f"{task_id}-experience.jsonl"
    if experience_file.exists():
        with open(experience_file, 'r', encoding='utf-8') as f:
            experience = json.load(f)
        experience["access_count"] = experience.get("access_count", 0) + 1
        with open(experience_file, 'w', encoding='utf-8') as f:
            json.dump(experience, f, ensure_ascii=False, indent=2)
    
    # Also update the access_counts.json file
    access_counts = load_access_counts()
    key = f"experience:{task_id}"
    access_counts["entries"][key] = access_counts["entries"].get(key, 0) + 1
    save_access_counts(access_counts)

def update_lesson_access_count(lesson_id):
    """Update access count for a lesson"""
    # First, update the lesson file itself if it's JSON
    lesson_file = LESSONS_DIR / f"{lesson_id}.jsonl"
    if lesson_file.exists():
        with open(lesson_file, 'r', encoding='utf-8') as f:
            # Read JSONL line
            line = f.readline().strip()
            if line:
                lesson = json.loads(line)
                # Note: lessons are JSONL, we'll just track in access_counts.json for now
                pass
    
    # Update the access_counts.json file
    access_counts = load_access_counts()
    key = f"lesson:{lesson_id}"
    access_counts["entries"][key] = access_counts["entries"].get(key, 0) + 1
    save_access_counts(access_counts)

def main():
    """Main function for CLI use"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Update access counts for memory entries")
    parser.add_argument("type", choices=["experience", "lesson"], help="Type of entry to update")
    parser.add_argument("id", help="ID of the entry (task_id for experience, lesson_id for lesson)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    if args.type == "experience":
        update_experience_access_count(args.id)
        entry_key = f"experience:{args.id}"
    else:
        update_lesson_access_count(args.id)
        entry_key = f"lesson:{args.id}"
    
    access_counts = load_access_counts()
    new_count = access_counts["entries"].get(entry_key, 1)
    
    if args.json:
        print(json.dumps({
            "ok": True,
            "type": args.type,
            "id": args.id,
            "new_count": new_count
        }, ensure_ascii=False, indent=2))
    else:
        print(f"✅ Updated access count for {args.type} {args.id}: new count = {new_count}")

if __name__ == "__main__":
    main()
