
#!/usr/bin/env python3
"""
Directory Index Generator
Generates and updates DIRECTORY_INDEX.md with detailed file information
"""

from datetime import datetime
from pathlib import Path
import os
import json

# Configuration
WORKSPACE = Path("/root/.openclaw/workspace")
INDEX_FILE = WORKSPACE / "DIRECTORY_INDEX.md"
EXCLUDE_DIRS = [".git", "__pycache__", ".openclaw", "node_modules", "memory.backup.20260303_101205"]
EXCLUDE_FILES = [".DS_Store", "google-chrome-stable_current_amd64.deb"]

# Known file information (can be expanded)
KNOWN_FILES = {
    "AGENTS.md": {
        "source": "Initial workspace setup",
        "description": "Agent configuration and core principles",
    },
    "SOUL.md": {
        "source": "Initial workspace setup",
        "description": "Berlin's persona and voice guidelines",
    },
    "USER.md": {
        "source": "Initial workspace setup",
        "description": "User information and preferences",
    },
    "TOOLS.md": {
        "source": "Initial workspace setup",
        "description": "Local tool configuration and notes",
    },
    "IDENTITY.md": {
        "source": "Initial workspace setup",
        "description": "Berlin's identity information",
    },
    "MEMORY.md": {
        "source": "Memory system",
        "description": "Long-term memory file (P0/P1/P2 entries)",
    },
    "HEARTBEAT.md": {
        "source": "Heartbeat system",
        "description": "Heartbeat task scheduling and checklist",
    },
    "BOOTSTRAP.md": {
        "source": "Initial workspace setup (missing)",
        "description": "Initial bootstrap instructions",
    },
    "DIRECTORY_INDEX.md": {
        "source": "Directory index system",
        "description": "Auto-generated directory index and file documentation",
    },
    "openclaw-feishu-config.json": {
        "source": "Feishu integration",
        "description": "Feishu channel configuration",
    },
}

def get_file_info(file_path):
    """Get detailed information about a file"""
    stat = file_path.stat()
    mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    
    # Try to determine source and description
    known_info = KNOWN_FILES.get(file_path.name, {"source": "Unknown", "description": ""})
    source = known_info["source"]
    description = known_info["description"]
    
    # Check if it's in projects/self-evolving-agents
    if "projects/self-evolving-agents" in str(file_path):
        source = "Self-Evolving Agents Project"
    
    # Check if it's in memory/
    if "memory/" in str(file_path):
        source = "Daily memory logs"
    
    # Check if it's in skills/
    if "skills/" in str(file_path):
        source = "OpenClaw skills"
    
    # Check if it's in reports/
    if "reports/" in str(file_path):
        source = "summary-report skill output"
    
    return {
        "path": str(file_path.relative_to(WORKSPACE)),
        "type": "directory" if file_path.is_dir() else "file",
        "size": stat.st_size,
        "mod_time": mod_time,
        "source": source,
        "description": description,
    }

def scan_directory(root_path, exclude_dirs=None, exclude_files=None):
    """Scan directory and collect file info"""
    if exclude_dirs is None:
        exclude_dirs = EXCLUDE_DIRS
    if exclude_files is None:
        exclude_files = EXCLUDE_FILES
    
    file_info_list = []
    
    # Use os.walk to properly skip excluded directories
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Modify dirnames in-place to skip excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs and not d.startswith(".")]
        
        for filename in filenames:
            # Skip excluded files and hidden files
            if filename in exclude_files or filename.startswith("."):
                continue
            
            file_path = Path(dirpath) / filename
            file_info = get_file_info(file_path)
            file_info_list.append(file_info)
    
    # Sort by path
    file_info_list.sort(key=lambda x: x["path"])
    return file_info_list

def generate_markdown_index(file_info_list):
    """Generate markdown content for directory index"""
    md = "# 工作区目录索引\n\n"
    md += "## 说明\n"
    md += "- 本文档自动生成，记录工作区所有重要文件的详细信息\n"
    md += "- 最后更新时间：{}\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    md += "---\n\n"
    
    # Group by directory
    directories = {}
    for info in file_info_list:
        dir_path = str(Path(info["path"]).parent)
        if dir_path not in directories:
            directories[dir_path] = []
        directories[dir_path].append(info)
    
    # Generate content for each directory
    for dir_path in sorted(directories.keys()):
        md += f"## {dir_path if dir_path != '.' else '根目录'}\n\n"
        
        for info in directories[dir_path]:
            type_emoji = "📁" if info["type"] == "directory" else "📄"
            md += f"### {type_emoji} {info['path']}\n"
            md += f"- **类型**: {info['type']}\n"
            md += f"- **大小**: {info['size']} bytes\n"
            md += f"- **修改时间**: {info['mod_time']}\n"
            md += f"- **来源**: {info['source']}\n"
            if info["description"]:
                md += f"- **说明**: {info['description']}\n"
            md += "\n"
    
    return md

def get_result_json(file_info_list):
    """Get result as JSON"""
    next_actions = [
        {
            "command": "cat /root/.openclaw/workspace/DIRECTORY_INDEX.md",
            "description": "View the generated directory index"
        },
        {
            "command": "update_directory_index.py",
            "description": "Update the directory index again later"
        }
    ]
    
    return {
        "ok": True,
        "command": "update_directory_index.py",
        "result": {
            "total_items": len(file_info_list),
            "index_file": str(INDEX_FILE),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "next_actions": next_actions
    }


def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="Directory Index Generator")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()
    
    print("Scanning workspace...")
    file_info_list = scan_directory(WORKSPACE)
    
    print(f"Found {len(file_info_list)} items")
    
    print("Generating directory index...")
    md_content = generate_markdown_index(file_info_list)
    
    print("Writing index file...")
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    if args.json:
        result_json = get_result_json(file_info_list)
        print(json.dumps(result_json, indent=2, ensure_ascii=False))
        sys.exit(0)
    else:
        print(f"Directory index saved to {INDEX_FILE}")
        sys.exit(0)


if __name__ == "__main__":
    import sys
    main()
