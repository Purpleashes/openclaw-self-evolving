
#!/usr/bin/env python3
"""
Import existing experiences into the memory access hook system
"""

import sys
import os
import json
from pathlib import Path

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory_access_hook import MemoryAccessHook

def import_existing_experiences():
    """Import existing experience files into the access hook system"""
    hook = MemoryAccessHook()
    experience_dir = Path("/root/.openclaw/workspace/memory/experiences")
    
    if not experience_dir.exists():
        print("❌ Experience directory not found!")
        return
    
    imported_count = 0
    for filename in experience_dir.glob("*-experience.jsonl"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                experience = json.load(f)
            
            task_id = experience.get("task_id")
            if not task_id:
                continue
            
            # Get the access count from the experience file
            file_access_count = experience.get("access_count", 1)
            
            # Manually update the access counts in the hook
            if "experiences" not in hook.access_counts:
                hook.access_counts["experiences"] = {}
            
            # Initialize with the file's access count
            hook.access_counts["experiences"][task_id] = {
                "count": file_access_count,
                "last_accessed": experience.get("timestamp", None),
                "tier": hook._get_memory_tier(file_access_count)
            }
            
            imported_count += 1
            print(f"✅ Imported: {task_id} (count={file_access_count}, tier={hook.access_counts['experiences'][task_id]['tier']})")
            
        except Exception as e:
            print(f"⚠️  Could not import {filename}: {e}")
    
    # Save the updated access counts
    hook._save_access_counts()
    
    print(f"\n✅ Import complete! Total imported: {imported_count}")
    
    # Print the stats
    hook.print_memory_stats()

if __name__ == "__main__":
    import_existing_experiences()

