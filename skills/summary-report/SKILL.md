---
name: "summary-report"
description: "Generate work summary reports from session history. Supports daily/weekly reports, outputs PDF."
---

# Summary Report Skill

Generate work summary reports from OpenClaw session history.

## Features
- Daily reports (昨日工作总结)
- Weekly reports (本周工作总结)
- Output as PDF
- Extracts key activities, decisions, and outcomes from session logs

## Usage
1. Read session history files from `memory/YYYY-MM-DD.md
2. Summarize key points:
   - Tasks completed
   - Decisions made
   - Key learnings
   - Next steps
3. Generate Markdown report
4. Convert to PDF (optional)

## Quick Example
```javascript
// Read daily log
read("/root/.openclaw/workspace/memory/2026-03-06.md")

// Generate summary
// ... summarize content ...

// Write report
write("/root/.openclaw/workspace/reports/daily-2026-03-06.md", summary)

// Convert to PDF (if needed)
exec("pandoc daily-2026-03-06.md -o daily-2026-03-06.pdf")
```
