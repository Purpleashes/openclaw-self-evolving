#!/usr/bin/env python3
"""
Memory Access Hook System - Dynamic access frequency tracking and memory tiering
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class MemoryAccessHook:
    def __init__(self, workspace_root="/root/.openclaw/workspace"):
        self.workspace_root = Path(workspace_root)
        self.experience_dir = self.workspace_root / "memory" / "experiences"
        self.lesson_dir = self.workspace_root / "memory" / "lessons"
        self.access_counts_file = self.workspace_root / "memory" / "access_counts.json"
        
        # Memory tier thresholds (access counts)
        self.tier_thresholds = {
            "hot": 5,      # Hot memory: accessed >= 5 times
            "warm": 2,     # Warm memory: accessed 2-4 times
            "cold": 1      # Cold memory: accessed 1 time
        }
        
        # Initialize access counts
        self.access_counts = self._load_access_counts()
    
    def _load_access_counts(self):
        """Load access counts from file"""
        if self.access_counts_file.exists():
            try:
                with open(self.access_counts_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Ensure all required keys exist
                    if "experiences" not in data:
                        data["experiences"] = {}
                    if "lessons" not in data:
                        data["lessons"] = {}
                    if "memory_md" not in data:
                        data["memory_md"] = {"count": 0, "last_accessed": None}
                    return data
            except Exception as e:
                print(f"⚠️  Warning: Could not load access counts: {e}")
        
        # Initialize empty counts
        return {
            "experiences": {},
            "lessons": {},
            "memory_md": {"count": 0, "last_accessed": None}
        }
    
    def _save_access_counts(self):
        """Save access counts to file"""
        # Convert defaultdict to regular dict for JSON serialization
        save_data = {
            "experiences": dict(self.access_counts["experiences"]),
            "lessons": dict(self.access_counts["lessons"]),
            "memory_md": self.access_counts["memory_md"]
        }
        
        with open(self.access_counts_file, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
    
    def _get_memory_tier(self, access_count):
        """Determine memory tier based on access count"""
        if access_count >= self.tier_thresholds["hot"]:
            return "hot"
        elif access_count >= self.tier_thresholds["warm"]:
            return "warm"
        else:
            return "cold"
    
    def track_experience_access(self, experience_id):
        """Track access to an experience file"""
        # Ensure experiences dict exists
        if "experiences" not in self.access_counts:
            self.access_counts["experiences"] = {}
        
        if experience_id not in self.access_counts["experiences"]:
            self.access_counts["experiences"][experience_id] = {
                "count": 0,
                "last_accessed": None,
                "tier": "cold"
            }
        
        # Update count and timestamp
        self.access_counts["experiences"][experience_id]["count"] += 1
        self.access_counts["experiences"][experience_id]["last_accessed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update tier
        new_tier = self._get_memory_tier(self.access_counts["experiences"][experience_id]["count"])
        old_tier = self.access_counts["experiences"][experience_id].get("tier", "cold")
        
        if new_tier != old_tier:
            print(f"🔄 Experience {experience_id} tier changed: {old_tier} → {new_tier}")
        
        self.access_counts["experiences"][experience_id]["tier"] = new_tier
        
        # Save the updated counts
        self._save_access_counts()
        
        return self.access_counts["experiences"][experience_id]
    
    def track_lesson_access(self, lesson_id):
        """Track access to a lesson file"""
        # Ensure lessons dict exists
        if "lessons" not in self.access_counts:
            self.access_counts["lessons"] = {}
        
        if lesson_id not in self.access_counts["lessons"]:
            self.access_counts["lessons"][lesson_id] = {
                "count": 0,
                "last_accessed": None,
                "tier": "cold"
            }
        
        # Update count and timestamp
        self.access_counts["lessons"][lesson_id]["count"] += 1
        self.access_counts["lessons"][lesson_id]["last_accessed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update tier
        new_tier = self._get_memory_tier(self.access_counts["lessons"][lesson_id]["count"])
        old_tier = self.access_counts["lessons"][lesson_id].get("tier", "cold")
        
        if new_tier != old_tier:
            print(f"🔄 Lesson {lesson_id} tier changed: {old_tier} → {new_tier}")
        
        self.access_counts["lessons"][lesson_id]["tier"] = new_tier
        
        # Save the updated counts
        self._save_access_counts()
        
        return self.access_counts["lessons"][lesson_id]
    
    def track_memory_md_access(self):
        """Track access to MEMORY.md"""
        self.access_counts["memory_md"]["count"] += 1
        self.access_counts["memory_md"]["last_accessed"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save the updated counts
        self._save_access_counts()
        
        return self.access_counts["memory_md"]
    
    def get_hot_memories(self, memory_type="experiences", limit=5):
        """Get the hottest (most accessed) memories"""
        if memory_type not in ["experiences", "lessons"]:
            return []
        
        memories = list(self.access_counts[memory_type].items())
        
        # Sort by access count (descending)
        memories.sort(key=lambda x: x[1]["count"], reverse=True)
        
        # Return top N hot memories
        return memories[:limit]
    
    def get_cold_memories(self, memory_type="experiences", days_threshold=30):
        """Get cold memories that haven't been accessed in N days"""
        if memory_type not in ["experiences", "lessons"]:
            return []
        
        cold_memories = []
        now = datetime.now()
        
        for memory_id, data in self.access_counts[memory_type].items():
            if data["last_accessed"]:
                last_accessed = datetime.strptime(data["last_accessed"], "%Y-%m-%d %H:%M:%S")
                days_since_access = (now - last_accessed).days
                
                if days_since_access >= days_threshold and data["tier"] == "cold":
                    cold_memories.append((memory_id, data))
        
        return cold_memories
    
    def print_memory_stats(self):
        """Print memory access statistics"""
        print("📊 Memory Access Statistics")
        print("=" * 60)
        
        # Experience stats
        exp_count = len(self.access_counts["experiences"])
        exp_total_accesses = sum(d["count"] for d in self.access_counts["experiences"].values())
        
        print(f"\n📝 Experiences:")
        print(f"  Total: {exp_count}")
        print(f"  Total accesses: {exp_total_accesses}")
        
        # Tier breakdown for experiences
        exp_tiers = defaultdict(int)
        for data in self.access_counts["experiences"].values():
            tier = data.get("tier", "cold")
            exp_tiers[tier] += 1
        
        print(f"  Tier breakdown: Hot={exp_tiers['hot']}, Warm={exp_tiers['warm']}, Cold={exp_tiers['cold']}")
        
        # Lesson stats
        lesson_count = len(self.access_counts["lessons"])
        lesson_total_accesses = sum(d["count"] for d in self.access_counts["lessons"].values())
        
        print(f"\n📚 Lessons:")
        print(f"  Total: {lesson_count}")
        print(f"  Total accesses: {lesson_total_accesses}")
        
        # Tier breakdown for lessons
        lesson_tiers = defaultdict(int)
        for data in self.access_counts["lessons"].values():
            tier = data.get("tier", "cold")
            lesson_tiers[tier] += 1
        
        print(f"  Tier breakdown: Hot={lesson_tiers['hot']}, Warm={lesson_tiers['warm']}, Cold={lesson_tiers['cold']}")
        
        # MEMORY.md stats
        print(f"\n🧠 MEMORY.md:")
        print(f"  Total accesses: {self.access_counts['memory_md']['count']}")
        print(f"  Last accessed: {self.access_counts['memory_md']['last_accessed']}")
        
        print("\n" + "=" * 60)
    
    def get_access_count(self, memory_id, memory_type="experiences"):
        """Get access count for a specific memory"""
        if memory_type == "experiences":
            if memory_id in self.access_counts["experiences"]:
                return self.access_counts["experiences"][memory_id]["count"]
        elif memory_type == "lessons":
            if memory_id in self.access_counts["lessons"]:
                return self.access_counts["lessons"][memory_id]["count"]
        elif memory_type == "memory_md":
            return self.access_counts["memory_md"]["count"]
        
        return 0

def main():
    parser = argparse.ArgumentParser(description="Memory Access Hook System")
    parser.add_argument("--stats", action="store_true", help="Print memory access statistics")
    parser.add_argument("--track-experience", help="Track access to an experience")
    parser.add_argument("--track-lesson", help="Track access to a lesson")
    parser.add_argument("--track-memory-md", action="store_true", help="Track access to MEMORY.md")
    parser.add_argument("--hot", action="store_true", help="Show hot memories")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    hook = MemoryAccessHook()
    
    if args.stats:
        hook.print_memory_stats()
    elif args.track_experience:
        result = hook.track_experience_access(args.track_experience)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✅ Tracked experience access: {args.track_experience}")
            print(f"   Access count: {result['count']}")
            print(f"   Tier: {result['tier']}")
    elif args.track_lesson:
        result = hook.track_lesson_access(args.track_lesson)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✅ Tracked lesson access: {args.track_lesson}")
            print(f"   Access count: {result['count']}")
            print(f"   Tier: {result['tier']}")
    elif args.track_memory_md:
        result = hook.track_memory_md_access()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✅ Tracked MEMORY.md access")
            print(f"   Total accesses: {result['count']}")
    elif args.hot:
        hot_experiences = hook.get_hot_memories("experiences")
        hot_lessons = hook.get_hot_memories("lessons")
        
        if args.json:
            print(json.dumps({
                "hot_experiences": hot_experiences,
                "hot_lessons": hot_lessons
            }, ensure_ascii=False, indent=2))
        else:
            print("🔥 Hot Memories")
            print("=" * 60)
            
            print("\n📝 Hot Experiences:")
            for exp_id, data in hot_experiences:
                print(f"  - {exp_id}: {data['count']} accesses ({data['tier']})")
            
            print("\n📚 Hot Lessons:")
            for lesson_id, data in hot_lessons:
                print(f"  - {lesson_id}: {data['count']} accesses ({data['tier']})")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
