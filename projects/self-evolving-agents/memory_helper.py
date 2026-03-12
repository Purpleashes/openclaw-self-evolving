
#!/usr/bin/env python3
"""
Memory Helper Script
Helps manage MEMORY.md file with proper P0/P1/P2 formatting
"""

import sys
from datetime import datetime
from pathlib import Path

MEMORY_FILE = Path("/root/.openclaw/workspace/MEMORY.md")


def read_memory_file():
    """Read the current MEMORY.md file"""
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def add_memory_entry(priority, content, date=None):
    """
    Add a memory entry to MEMORY.md
    
    Args:
        priority: "P0", "P1", or "P2"
        content: The memory content
        date: Date in YYYY-MM-DD format (defaults to today)
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    if priority == "P0":
        entry = f"- [P0] {content}\n"
    else:
        entry = f"- [{priority}][{date}] {content}\n"
    
    # Read current content
    content = read_memory_file()
    
    # Determine where to insert the entry
    # Find the appropriate section
    if priority == "P0":
        # Add to "About User" or "Key Relationships" or "Preferences" section
        # For simplicity, add to the end of the "Preferences [P0]" section
        if "## Preferences [P0]" in content:
            section_start = content.find("## Preferences [P0]")
            # Find the next section header
            next_section = content.find("##", section_start + 1)
            if next_section == -1:
                # Insert at end of file
                new_content = content + "\n" + entry
            else:
                # Insert before next section
                new_content = content[:next_section] + entry + content[next_section:]
        else:
            # Add to end of file
            new_content = content + "\n" + entry
    elif priority == "P1":
        # Add to "Active Projects [P1]" section
        if "## Active Projects [P1]" in content:
            section_start = content.find("## Active Projects [P1]")
            next_section = content.find("##", section_start + 1)
            if next_section == -1:
                new_content = content + "\n" + entry
            else:
                new_content = content[:next_section] + entry + content[next_section:]
        else:
            new_content = content + "\n" + entry
    elif priority == "P2":
        # Add to "Temporary [P2]" section
        if "## Temporary [P2]" in content:
            section_start = content.find("## Temporary [P2]")
            next_section = content.find("---", section_start + 1)
            if next_section == -1:
                new_content = content + "\n" + entry
            else:
                new_content = content[:next_section] + entry + content[next_section:]
        else:
            new_content = content + "\n" + entry
    else:
        raise ValueError("Priority must be P0, P1, or P2")
    
    # Write back to file
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added memory entry: {entry.strip()}")


def get_result_json(priority, content, date, entry):
    """Get result as JSON"""
    next_actions = [
        {
            "command": "memory_helper.py <priority> <content> [--date YYYY-MM-DD]",
            "description": "Add another memory entry"
        },
        {
            "command": "cat /root/.openclaw/workspace/MEMORY.md",
            "description": "View updated MEMORY.md"
        }
    ]
    
    return {
        "ok": True,
        "command": f"memory_helper.py {priority} \"{content}\" {f'--date {date}' if date else ''}".strip(),
        "result": {
            "priority": priority,
            "content": content,
            "date": date,
            "entry": entry.strip()
        },
        "next_actions": next_actions
    }


def main():
    """Main function for CLI use"""
    import argparse
    import json
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description="Memory Helper Script")
    parser.add_argument("priority", choices=["P0", "P1", "P2"], help="Priority level (P0, P1, P2)")
    parser.add_argument("content", help="Memory content")
    parser.add_argument("--date", help="Date in YYYY-MM-DD format (defaults to today)")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    if args.date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        date = args.date
    
    if args.priority == "P0":
        entry = f"- [P0] {args.content}\n"
    else:
        entry = f"- [{args.priority}][{date}] {args.content}\n"
    
    # Add the entry first
    add_memory_entry(args.priority, args.content, args.date)
    
    if args.json:
        result_json = get_result_json(args.priority, args.content, date, entry)
        print(json.dumps(result_json, indent=2, ensure_ascii=False))
        sys.exit(0)


if __name__ == "__main__":
    main()
