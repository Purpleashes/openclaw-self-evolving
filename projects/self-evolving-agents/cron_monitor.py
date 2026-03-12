#!/usr/bin/env python3
"""
Cron Task Monitor - Monitor cron task execution and alert on failures
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime
import argparse

def load_last_cron_runs(cron_runs_dir="/root/.openclaw/cron/runs"):
    """Load the last run for each cron job"""
    runs_dir = Path(cron_runs_dir)
    if not runs_dir.exists():
        return {}
    
    last_runs = {}
    
    for run_file in runs_dir.glob("*.jsonl"):
        try:
            with open(run_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        run = json.loads(line)
                        job_id = run.get('jobId')
                        if job_id:
                            ts = run.get('ts', 0)
                            if job_id not in last_runs or ts > last_runs[job_id].get('ts', 0):
                                last_runs[job_id] = run
        except Exception as e:
            print(f"⚠️  Warning: Could not load {run_file}: {e}")
    
    return last_runs

def check_cron_failures(last_runs):
    """Check for cron job failures"""
    failures = []
    
    for job_id, run in last_runs.items():
        status = run.get('status')
        if status == 'error':
            failures.append({
                'job_id': job_id,
                'error': run.get('error', 'Unknown error'),
                'ts': run.get('ts'),
                'summary': run.get('summary', '')
            })
    
    return failures

def print_monitor_report(last_runs, failures):
    """Print monitor report in a user-friendly format"""
    print("🔍 Cron Task Monitor Report")
    print("=" * 100)
    
    # Print last runs status
    print(f"\n📋 Last run status for each job:")
    print("-" * 100)
    
    for job_id, run in last_runs.items():
        ts = run.get('ts')
        dt = datetime.fromtimestamp(ts / 1000) if ts else "Unknown"
        status = run.get('status', 'Unknown')
        next_run = run.get('nextRunAtMs')
        next_dt = datetime.fromtimestamp(next_run / 1000) if next_run else "Unknown"
        
        status_emoji = "✅" if status == "success" else "❌" if status == "error" else "⏳"
        
        print(f"{job_id[:60]:60} | {status_emoji} {status:10} | Last: {dt} | Next: {next_dt}")
    
    # Print failures
    if failures:
        print("\n" + "=" * 100)
        print("⚠️  FAILED JOBS DETECTED!")
        print("-" * 100)
        
        for i, failure in enumerate(failures):
            ts = failure.get('ts')
            dt = datetime.fromtimestamp(ts / 1000) if ts else "Unknown"
            job_id = failure.get('job_id')
            error = failure.get('error')
            
            print(f"\n{i+1}. {dt} - {job_id}")
            print(f"   Error: {error}")
            
            summary = failure.get('summary')
            if summary:
                print(f"   Summary: {summary[:100]}..." if len(summary) > 100 else f"   Summary: {summary}")
    else:
        print("\n" + "=" * 100)
        print("✅ No failures detected! All cron jobs are running successfully.")
    
    print("\n" + "=" * 100)

def main():
    parser = argparse.ArgumentParser(description="Cron Task Monitor")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--watch", action="store_true", help="Watch mode (check every 60 seconds)")
    args = parser.parse_args()
    
    if args.watch:
        print("🔍 Watching cron tasks (Ctrl+C to stop)...")
        try:
            while True:
                last_runs = load_last_cron_runs()
                failures = check_cron_failures(last_runs)
                
                if failures:
                    print("\n" + "=" * 100)
                    print(f"⚠️  {len(failures)} FAILURE(S) DETECTED at {datetime.now()}!")
                    print("=" * 100)
                    print_monitor_report(last_runs, failures)
                
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n👋 Stopping watch mode...")
    else:
        last_runs = load_last_cron_runs()
        failures = check_cron_failures(last_runs)
        
        if args.json:
            output = {
                "last_runs": last_runs,
                "failures": failures,
                "timestamp": datetime.now().isoformat()
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print_monitor_report(last_runs, failures)

if __name__ == "__main__":
    main()
