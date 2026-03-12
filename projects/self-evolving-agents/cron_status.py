#!/usr/bin/env python3
"""
Cron Task Status - Conveniently view cron task run status
"""

import os
import json
from pathlib import Path
from datetime import datetime
import argparse

def load_cron_runs(cron_runs_dir="/root/.openclaw/cron/runs"):
    """Load all cron run records"""
    runs_dir = Path(cron_runs_dir)
    if not runs_dir.exists():
        return []
    
    runs = []
    for run_file in runs_dir.glob("*.jsonl"):
        try:
            with open(run_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        run = json.loads(line)
                        runs.append(run)
        except Exception as e:
            print(f"⚠️  Warning: Could not load {run_file}: {e}")
    
    # Sort by timestamp (newest first)
    runs.sort(key=lambda x: x.get('ts', 0), reverse=True)
    return runs

def print_cron_status(runs, limit=20):
    """Print cron task status in a user-friendly format"""
    if not runs:
        print("📭 No cron task runs found.")
        return
    
    print("📊 Cron Task Status")
    print("=" * 100)
    
    # Print recent runs
    print(f"\n📋 Recent {limit} runs:")
    print("-" * 100)
    
    for i, run in enumerate(runs[:limit]):
        ts = run.get('ts')
        dt = datetime.fromtimestamp(ts / 1000) if ts else "Unknown"
        job_id = run.get('jobId', 'Unknown')
        action = run.get('action', 'Unknown')
        status = run.get('status', 'Unknown')
        duration = run.get('durationMs', 0)
        
        status_emoji = "✅" if status == "success" else "❌" if status == "error" else "⏳"
        
        print(f"{i+1:2d}. {dt} | {job_id[:40]:40} | {action:10} | {status_emoji} {status:10} | {duration:6}ms")
    
    # Print summary
    print("\n" + "=" * 100)
    print("📈 Summary:")
    
    total_runs = len(runs)
    success_runs = len([r for r in runs if r.get('status') == 'success'])
    error_runs = len([r for r in runs if r.get('status') == 'error'])
    
    print(f"   Total runs: {total_runs}")
    print(f"   Success:    {success_runs} ({success_runs/total_runs*100:.1f}%)" if total_runs > 0 else "   Success:    0")
    print(f"   Errors:     {error_runs} ({error_runs/total_runs*100:.1f}%)" if total_runs > 0 else "   Errors:     0")
    
    if error_runs > 0:
        print("\n⚠️  Recent errors:")
        error_runs_list = [r for r in runs if r.get('status') == 'error'][:5]
        for i, run in enumerate(error_runs_list):
            ts = run.get('ts')
            dt = datetime.fromtimestamp(ts / 1000) if ts else "Unknown"
            job_id = run.get('jobId', 'Unknown')
            error = run.get('error', 'Unknown error')
            print(f"   {i+1}. {dt} - {job_id}: {error}")

def main():
    parser = argparse.ArgumentParser(description="Cron Task Status")
    parser.add_argument("--limit", type=int, default=20, help="Number of recent runs to show (default: 20)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    runs = load_cron_runs()
    
    if args.json:
        print(json.dumps(runs[:args.limit], indent=2, ensure_ascii=False))
    else:
        print_cron_status(runs, args.limit)

if __name__ == "__main__":
    main()
