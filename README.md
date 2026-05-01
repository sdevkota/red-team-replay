# Red Team Replay

Replayable incident traces for AI agent failures.

> Version: 2.0.0 | Runtime: Python | License: MIT | Status: production-oriented v2 foundation

## Problem

AI incidents are hard to reproduce because prompts, tool calls, hidden context, retrieval, and approvals are scattered across logs.

## What this project solves

A normalized replay bundle validator for prompts, context, tool calls, decisions, outcomes, and mitigation notes.

Red Team Replay is now Python-first. It ships as a dependency-free Python package and CLI that validates a domain-specific JSON packet, emits actionable findings, and gives contributors a practical foundation for adapters, datasets, evals, and workflow integrations.

## Quick start

```bash
python3 -m unittest discover -s tests
python3 -m red_team_replay.cli sample
```

Analyze your own packet:

```bash
python3 -m red_team_replay.cli ./packet.json
```

Or pipe JSON:

```bash
cat packet.json | python3 -m red_team_replay.cli
```

## Example packet

```json
{
  "incident": {
    "id": "agi-2026-001",
    "severity": "high"
  },
  "trace": [
    {
      "step": 1,
      "actor": "agent",
      "action": "read_email"
    },
    {
      "step": 2,
      "actor": "tool",
      "action": "send_email"
    }
  ],
  "mitigation": {
    "addedGate": "human_approval"
  }
}
```

## Library usage

```python
from red_team_replay import analyze

report = analyze({
  "incident": {
    "id": "agi-2026-001",
    "severity": "high"
  },
  "trace": [
    {
      "step": 1,
      "actor": "agent",
      "action": "read_email"
    },
    {
      "step": 2,
      "actor": "tool",
      "action": "send_email"
    }
  ],
  "mitigation": {
    "addedGate": "human_approval"
  }
})
print(report["summary"])
```

## v2 behavior

- Python-first CLI and importable library.
- Validates required fields for the domain packet.
- Scores readiness from 0 to 100.
- Reports missing or weak governance evidence.
- Runs fully offline with no API keys and no network access.

## Contribution map

- Add OpenTelemetry mapping.
- Add LangSmith imports.
- Add privacy scrubbing.
- Add replay runners.

## Project principles

- Human agency over blind automation.
- Open standards over vendor lock-in.
- Auditable decisions over hidden magic.
- Privacy and safety as design constraints, not release notes.
