---
name: "capability-evolver"
description: "Analyze agent runtime history, automatically identify capability gaps, and evolve safely within protocol constraints."
---

# Capability Evolver Skill

## Features
- Analyze agent runtime history from memory logs
- Automatically identify capability gaps and areas for improvement
- Propose safe evolution strategies within predefined protocol constraints
- Track evolution progress and outcomes

## Usage
1. Read memory logs from `memory/YYYY-MM-DD.md
2. Analyze past performance to identify gaps
3. Propose evolution actions (e.g., new skills, improved workflows)
4. Execute evolution within safety constraints
5. Document outcomes in memory

## Quick Example
```javascript
// Read recent memory logs
read("/root/.openclaw/workspace/memory/2026-03-05.md")
read("/root/.openclaw/workspace/memory/2026-03-06.md")

// Analyze for capability gaps
// ... identify areas where agent struggled ...

// Propose and execute safe evolution
// ... implement improvements ...
```

## Safety Constraints
- Never modify core system files without explicit approval
- All evolution actions must be documented in memory
- Rollback capability must be maintained for all changes
- Evolution must not compromise privacy or security
