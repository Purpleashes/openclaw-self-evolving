
#!/bin/bash
# Arena System Setup Script

if [ $# -ne 1 ]; then
    echo "Usage: $0 <arena-directory>"
    exit 1
fi

ARENA_DIR="$1"

mkdir -p "$ARENA_DIR/prompts" "$ARENA_DIR/outputs/agent" "$ARENA_DIR/outputs/anti-agent"

cat > "$ARENA_DIR/state.json" << 'EOF'
{
  "current_turn": "agent",
  "iteration": 0,
  "topic": "my-project",
  "active": true,
  "max_iterations": 10
}
EOF

cat > "$ARENA_DIR/prompts/agent.md" << 'EOF'
# Agent Persona
You are the primary agent. Your job is to:
1. Complete the task thoroughly
2. Write clear, detailed reports
3. Defend your work when challenged
EOF

cat > "$ARENA_DIR/prompts/anti-agent.md" << 'EOF'
# Anti-Agent Persona
You are the critical reviewer. Your job is to:
1. Question every assumption
2. Look for hallucinations and mistakes
3. Write counter-reports with evidence
4. Push for validation and testing
EOF

echo "Arena system set up at $ARENA_DIR"
