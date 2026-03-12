#!/usr/bin/env python3
"""
Cron Task Stats - Generate cron task execution statistics
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import argparse

def load_all_cron_runs(cron_runs_dir="/root/.openclaw/cron/runs"):
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
    
    # Sort by timestamp (oldest first)
    runs.sort(key=lambda x: x.get('ts', 0))
    return runs

def analyze_cron_runs(runs, days=7):
    """Analyze cron runs and generate statistics"""
    if not runs:
        return {}
    
    # Filter by time range
    cutoff_time = (datetime.now() - timedelta(days=days)).timestamp() * 1000
    recent_runs = [r for r in runs if r.get('ts', 0) >= cutoff_time]
    
    if not recent_runs:
        return {}
    
    # Analyze by job
    job_stats = defaultdict(lambda: {
        'total': 0,
        'success': 0,
        'error': 0,
        'durations': [],
        'first_run': None,
        'last_run': None
    })
    
    for run in recent_runs:
        job_id = run.get('jobId', 'unknown')
        status = run.get('status', 'unknown')
        duration = run.get('durationMs', 0)
        ts = run.get('ts', 0)
        
        stats = job_stats[job_id]
        stats['total'] += 1
        
        if status == 'success':
            stats['success'] += 1
        elif status == 'error':
            stats['error'] += 1
        
        if duration > 0:
            stats['durations'].append(duration)
        
        if stats['first_run'] is None or ts < stats['first_run']:
            stats['first_run'] = ts
        
        if stats['last_run'] is None or ts > stats['last_run']:
            stats['last_run'] = ts
    
    # Calculate aggregate stats
    for job_id, stats in job_stats.items():
        if stats['durations']:
            stats['avg_duration'] = sum(stats['durations']) / len(stats['durations'])
            stats['min_duration'] = min(stats['durations'])
            stats['max_duration'] = max(stats['durations'])
        else:
            stats['avg_duration'] = 0
            stats['min_duration'] = 0
            stats['max_duration'] = 0
        
        if stats['total'] > 0:
            stats['success_rate'] = (stats['success'] / stats['total']) * 100
        else:
            stats['success_rate'] = 0
    
    return dict(job_stats)

def print_stats_report(stats, days=7):
    """Print statistics report in a user-friendly format"""
    if not stats:
        print("📭 No cron task runs found for the specified time range.")
        return
    
    print(f"📊 Cron Task Statistics (Last {days} days)")
    print("=" * 120)
    
    # Print header
    print(f"\n{'Job ID':<60} | {'Total':<6} | {'Success':<6} | {'Error':<6} | {'Success %':<10} | {'Avg (ms)':<10} | {'Min (ms)':<10} | {'Max (ms)':<10}")
    print("-" * 120)
    
    # Print each job's stats
    for job_id, job_stats in stats.items():
        total = job_stats['total']
        success = job_stats['success']
        error = job_stats['error']
        success_rate = job_stats['success_rate']
        avg_duration = job_stats['avg_duration']
        min_duration = job_stats['min_duration']
        max_duration = job_stats['max_duration']
        
        status_emoji = "✅" if success_rate == 100 else "⚠️" if success_rate >= 80 else "❌"
        
        print(f"{status_emoji} {job_id[:58]:<58} | {total:<6} | {success:<6} | {error:<6} | {success_rate:>8.1f}% | {avg_duration:>9.0f} | {min_duration:>9.0f} | {max_duration:>9.0f}")
    
    # Print aggregate summary
    print("\n" + "=" * 120)
    print("📈 Aggregate Summary:")
    
    total_jobs = len(stats)
    total_runs = sum(s['total'] for s in stats.values())
    total_success = sum(s['success'] for s in stats.values())
    total_error = sum(s['error'] for s in stats.values())
    overall_success_rate = (total_success / total_runs * 100) if total_runs > 0 else 0
    
    print(f"   Total jobs:    {total_jobs}")
    print(f"   Total runs:    {total_runs}")
    print(f"   Success:       {total_success} ({overall_success_rate:.1f}%)")
    print(f"   Errors:        {total_error}")
    
    perfect_jobs = len([s for s in stats.values() if s['success_rate'] == 100])
    print(f"   Perfect jobs:  {perfect_jobs}/{total_jobs} ({perfect_jobs/total_jobs*100:.1f}%)" if total_jobs > 0 else "   Perfect jobs:  0")

def main():
    parser = argparse.ArgumentParser(description="Cron Task Statistics")
    parser.add_argument("--days", type=int, default=7, help="Number of days to analyze (default: 7)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    runs = load_all_cron_runs()
    stats = analyze_cron_runs(runs, args.days)
    
    if args.json:
        output = {
            'days': args.days,
            'stats': stats,
            'generated_at': datetime.now().isoformat()
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print_stats_report(stats, args.days)

if __name__ == "__main__":
    main()
