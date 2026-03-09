
#!/usr/bin/env python3
"""
Memory Helper Script
Helps manage MEMORY.md file with proper P0/P1/P2 formatting
"""

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


def main():
    """Main function for CLI use"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Helper Script")
    parser.add_argument("priority", choices=["P0", "P1", "P2"], help="Priority level (P0, P1, P2)")
    parser.add_argument("content", help="Memory content")
    parser.add_argument("--date", help="Date in YYYY-MM-DD format (defaults to today)")
    
    args = parser.parse_args()
    
    add_memory_entry(args.priority, args.content, args.date)


if __name__ == "__main__":
    main()
