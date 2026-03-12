
#!/usr/bin/env python3
"""
Summary Report Generator
Generates work summary reports from daily memory files
"""

from datetime import datetime, timedelta
from pathlib import Path
import argparse

# Workspace paths
WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
REPORTS_DIR = WORKSPACE / "reports"


def read_memory_file(date_str):
    """Read memory file for a specific date"""
    memory_file = MEMORY_DIR / f"{date_str}.md"
    if not memory_file.exists():
        return None
    with open(memory_file, 'r', encoding='utf-8') as f:
        return f.read()


def generate_daily_report(date_str):
    """Generate daily summary report"""
    memory_content = read_memory_file(date_str)
    if not memory_content:
        return f"No memory file found for {date_str}"
    
    # Generate report (for now, just use the memory content as a base)
    # In the future, we can add more sophisticated summarization
    report = f"# {date_str} 工作总结\n\n"
    report += "## 今日主要工作\n\n"
    report += "(内容从记忆文件中提取)\n\n"
    report += memory_content
    
    return report


def save_report(date_str, report_content):
    """Save report to reports directory"""
    REPORTS_DIR.mkdir(exist_ok=True)
    report_file = REPORTS_DIR / f"daily-{date_str}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report_content)
    return report_file


def main():
    parser = argparse.ArgumentParser(description="Generate work summary reports")
    parser.add_argument("--date", help="Date in YYYY-MM-DD format (defaults to yesterday)")
    
    args = parser.parse_args()
    
    if args.date:
        date_str = args.date
    else:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = yesterday.strftime("%Y-%m-%d")
    
    print(f"Generating report for {date_str}...")
    report = generate_daily_report(date_str)
    report_file = save_report(date_str, report)
    print(f"Report saved to {report_file}")


if __name__ == "__main__":
    main()
