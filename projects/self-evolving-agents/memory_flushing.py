
#!/usr/bin/env python3
"""
Memory Flushing System - Pre-compression memory flushing mechanism
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

from memory_access_hook import MemoryAccessHook

class MemoryFlushing:
    def __init__(self, workspace_root="/root/.openclaw/workspace"):
        self.workspace_root = Path(workspace_root)
        self.hook = MemoryAccessHook(workspace_root)
        
        # Context limit configuration (in tokens, approximate)
        self.context_limit = 200000  # Our model has 262144 context window, leave some buffer
        self.warning_threshold = 0.8  # 80% of limit
        self.danger_threshold = 0.95  # 95% of limit
        
        # Approximate token counts for different memory types
        self.token_estimates = {
            "experience": 500,  # Average experience file size in tokens
            "lesson": 300,     # Average lesson file size in tokens
            "memory_md": 2000  # MEMORY.md size in tokens
        }
    
    def estimate_current_context(self):
        """Estimate the current context usage in tokens"""
        total_tokens = 0
        
        # Count experiences
        exp_count = len(self.hook.access_counts["experiences"])
        total_tokens += exp_count * self.token_estimates["experience"]
        
        # Count lessons
        lesson_count = len(self.hook.access_counts["lessons"])
        total_tokens += lesson_count * self.token_estimates["lesson"]
        
        # Add MEMORY.md
        total_tokens += self.token_estimates["memory_md"]
        
        return total_tokens
    
    def check_context_status(self):
        """Check the current context status"""
        current_tokens = self.estimate_current_context()
        usage_percent = (current_tokens / self.context_limit) * 100
        
        status = "safe"
        if usage_percent >= self.danger_threshold * 100:
            status = "danger"
        elif usage_percent >= self.warning_threshold * 100:
            status = "warning"
        
        return {
            "current_tokens": current_tokens,
            "context_limit": self.context_limit,
            "usage_percent": usage_percent,
            "status": status
        }
    
    def flush_warm_to_cold(self, dry_run=False):
        """Flush warm memories to cold tier"""
        flushed = []
        
        for exp_id, data in self.hook.access_counts["experiences"].items():
            if data.get("tier") == "warm":
                flushed.append(exp_id)
                if not dry_run:
                    # Change tier to cold
                    data["tier"] = "cold"
        
        # Save the changes
        if not dry_run:
            self.hook._save_access_counts()
        
        return flushed
    
    def flush_cold_to_archive(self, days_threshold=30, dry_run=False):
        """Flush cold memories to archive"""
        archived = []
        now = datetime.now()
        
        for exp_id, data in self.hook.access_counts["experiences"].items():
            if data.get("tier") == "cold" and data.get("last_accessed"):
                last_accessed = datetime.strptime(data["last_accessed"], "%Y-%m-%d %H:%M:%S")
                days_since = (now - last_accessed).days
                
                if days_since >= days_threshold:
                    archived.append(exp_id)
                    # In a real implementation, we would move the file to archive
                    # For now, just mark it
                    if not dry_run:
                        data["archived"] = True
        
        if not dry_run:
            self.hook._save_access_counts()
        
        return archived
    
    def execute_flush(self, dry_run=False):
        """Execute the memory flushing process"""
        status = self.check_context_status()
        
        print("🔄 Memory Flushing Check")
        print("=" * 60)
        print(f"Current: {status['current_tokens']:,} tokens / {status['context_limit']:,} tokens")
        print(f"Usage: {status['usage_percent']:.1f}%")
        print(f"Status: {status['status'].upper()}")
        print()
        
        if status["status"] == "safe":
            print("✅ Context is safe, no flushing needed.")
            return []
        
        flushed = []
        
        if status["status"] == "warning":
            print("⚠️  Context warning - flushing warm memories to cold...")
            flushed = self.flush_warm_to_cold(dry_run)
        
        elif status["status"] == "danger":
            print("🚨 Context danger - flushing warm and cold memories...")
            flushed = self.flush_warm_to_cold(dry_run)
            archived = self.flush_cold_to_archive(dry_run)
            flushed.extend(archived)
        
        if dry_run:
            print(f"\n📋 DRY RUN: Would flush {len(flushed)} memories:")
            for exp_id in flushed:
                print(f"  - {exp_id}")
        else:
            print(f"\n✅ Flushed {len(flushed)} memories.")
        
        print("\n" + "=" * 60)
        
        return flushed
    
    def print_status(self):
        """Print the current memory status"""
        status = self.check_context_status()
        
        print("📊 Memory Context Status")
        print("=" * 60)
        print(f"Current: {status['current_tokens']:,} tokens")
        print(f"Limit: {status['context_limit']:,} tokens")
        print(f"Usage: {status['usage_percent']:.1f}%")
        
        # Status indicator
        if status["status"] == "safe":
            print(f"Status: ✅ Safe")
        elif status["status"] == "warning":
            print(f"Status: ⚠️ Warning")
        else:
            print(f"Status: 🚨 Danger")
        
        # Tier breakdown
        print("\n📝 Memory Tier Breakdown:")
        tiers = defaultdict(int)
        for data in self.hook.access_counts["experiences"].values():
            tier = data.get("tier", "cold")
            tiers[tier] += 1
        
        print(f"  Hot: {tiers['hot']}")
        print(f"  Warm: {tiers['warm']}")
        print(f"  Cold: {tiers['cold']}")
        
        print("\n" + "=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Memory Flushing System")
    parser.add_argument("--status", action="store_true", help="Check memory context status")
    parser.add_argument("--flush", action="store_true", help="Execute memory flushing")
    parser.add_argument("--dry-run", action="store_true", help="Dry run (don't modify anything)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    flushing = MemoryFlushing()
    
    if args.status:
        if args.json:
            status = flushing.check_context_status()
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            flushing.print_status()
    elif args.flush:
        flushed = flushing.execute_flush(dry_run=args.dry_run)
        if args.json:
            print(json.dumps({
                "ok": True,
                "flushed": flushed,
                "dry_run": args.dry_run
            }, ensure_ascii=False, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

