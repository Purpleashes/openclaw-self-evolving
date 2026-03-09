
#!/usr/bin/env python3
"""
Adaptive Learning Agent - Learn from errors and corrections in real-time
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

class Learning:
    def __init__(self, content: str, category: str, source: str, context: str = ""):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.content = content
        self.category = category
        self.source = source
        self.context = context
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "category": self.category,
            "source": self.source,
            "context": self.context,
            "timestamp": self.timestamp
        }

class Error:
    def __init__(self, error_description: str, context: str, solution: str = "", prevention_tip: str = ""):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.error_description = error_description
        self.context = context
        self.solution = solution
        self.prevention_tip = prevention_tip
        self.timestamp = datetime.now().isoformat()
        self.resolved = bool(solution)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "error_description": self.error_description,
            "context": self.context,
            "solution": self.solution,
            "prevention_tip": self.prevention_tip,
            "timestamp": self.timestamp,
            "resolved": self.resolved
        }

class AdaptiveLearningAgent:
    def __init__(self, storage_dir: Optional[str] = None):
        if storage_dir is None:
            storage_dir = Path.home() / ".adaptive_learning"
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.learnings_file = self.storage_dir / "learnings.json"
        self.errors_file = self.storage_dir / "errors.json"
        self._load_data()

    def _load_data(self):
        self.learnings: List[Learning] = []
        self.errors: List[Error] = []
        
        if self.learnings_file.exists():
            with open(self.learnings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    learning = Learning(
                        content=item["content"],
                        category=item["category"],
                        source=item["source"],
                        context=item.get("context", "")
                    )
                    learning.id = item["id"]
                    learning.timestamp = item["timestamp"]
                    self.learnings.append(learning)
        
        if self.errors_file.exists():
            with open(self.errors_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    error = Error(
                        error_description=item["error_description"],
                        context=item["context"],
                        solution=item.get("solution", ""),
                        prevention_tip=item.get("prevention_tip", "")
                    )
                    error.id = item["id"]
                    error.timestamp = item["timestamp"]
                    error.resolved = item.get("resolved", False)
                    self.errors.append(error)

    def _save_data(self):
        with open(self.learnings_file, "w", encoding="utf-8") as f:
            json.dump([l.to_dict() for l in self.learnings], f, ensure_ascii=False, indent=2)
        
        with open(self.errors_file, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.errors], f, ensure_ascii=False, indent=2)

    def record_learning(self, content: str, category: str = "technique", source: str = "successful-pattern", context: str = "") -> Learning:
        learning = Learning(content=content, category=category, source=source, context=context)
        self.learnings.append(learning)
        self._save_data()
        return learning

    def record_error(self, error_description: str, context: str, solution: str = "", prevention_tip: str = "") -> Error:
        error = Error(
            error_description=error_description,
            context=context,
            solution=solution,
            prevention_tip=prevention_tip
        )
        self.errors.append(error)
        
        if solution:
            self.record_learning(
                content=f"Error: {error_description}\nSolution: {solution}",
                category="bug-fix",
                source="error-discovery",
                context=context
            )
        
        self._save_data()
        return error

    def search_learnings(self, query: str) -> List[Learning]:
        results = []
        query_lower = query.lower()
        for learning in self.learnings:
            if (query_lower in learning.content.lower() or 
                query_lower in learning.category.lower() or 
                query_lower in learning.context.lower()):
                results.append(learning)
        return sorted(results, key=lambda x: x.timestamp, reverse=True)

    def get_recent_learnings(self, limit: int = 10) -> List[Learning]:
        return sorted(self.learnings, key=lambda x: x.timestamp, reverse=True)[:limit]

    def get_learnings_by_category(self, category: str) -> List[Learning]:
        return [l for l in self.learnings if l.category == category]

    def get_learning_summary(self) -> Dict[str, Any]:
        total_learnings = len(self.learnings)
        total_errors = len(self.errors)
        resolved_errors = len([e for e in self.errors if e.resolved])
        unresolved_errors = total_errors - resolved_errors
        
        category_counts = {}
        for learning in self.learnings:
            category_counts[learning.category] = category_counts.get(learning.category, 0) + 1
        
        return {
            "total_learnings": total_learnings,
            "total_errors": total_errors,
            "error_statistics": {
                "total": total_errors,
                "resolved": resolved_errors,
                "unresolved": unresolved_errors
            },
            "category_counts": category_counts,
            "recent_learnings": [l.to_dict() for l in self.get_recent_learnings(5)],
            "recent_errors": [e.to_dict() for e in sorted(self.errors, key=lambda x: x.timestamp, reverse=True)[:5]]
        }

    def format_learning_summary(self) -> str:
        summary = self.get_learning_summary()
        lines = []
        lines.append("=== Adaptive Learning Summary ===")
        lines.append(f"Total Learnings: {summary['total_learnings']}")
        lines.append(f"Total Errors: {summary['error_statistics']['total']}")
        lines.append(f"  Resolved: {summary['error_statistics']['resolved']}")
        lines.append(f"  Unresolved: {summary['error_statistics']['unresolved']}")
        lines.append("\nCategory Counts:")
        for category, count in summary['category_counts'].items():
            lines.append(f"  {category}: {count}")
        lines.append("\nRecent Learnings:")
        for learning in summary['recent_learnings']:
            lines.append(f"  - [{learning['timestamp']}] {learning['content'][:50]}...")
        return "\n".join(lines)

    def export_learnings(self, output_file: str = "learnings_export.json"):
        export_data = {
            "learnings": [l.to_dict() for l in self.learnings],
            "errors": [e.to_dict() for e in self.errors],
            "exported_at": datetime.now().isoformat()
        }
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        return output_file
