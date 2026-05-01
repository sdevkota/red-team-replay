# Red Team Replay

Replayable incident traces for AI agent failures.

> Version: 1.0.0 | License: MIT | Status: production-oriented v1 foundation

## Problem

AI incidents are hard to reproduce because prompts, tool calls, hidden context, retrieval, and approvals are scattered across logs.

## What this project solves

A normalized replay bundle validator for prompts, context, tool calls, decisions, outcomes, and mitigation notes.

Red Team Replay ships as a small, dependency-free CLI and library. It validates a domain-specific JSON packet, emits actionable findings, and gives contributors a concrete surface for adding adapters, richer checks, schemas, and integrations.

## Who it is for

AI red teams, incident responders, platform observability teams.

## Quick start

```bash
npm test
npm start -- sample
```

Analyze your own packet:

```bash
red-team-replay ./packet.json
```

Or pipe JSON:

```bash
cat packet.json | node src/cli.js
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

```js
const { analyze } = require("./src/index.js");

const report = analyze({
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
});
console.log(report.summary);
```

## v1 behavior

- Validates required fields for the domain packet.
- Scores readiness from 0 to 100.
- Reports missing or weak governance evidence.
- Suggests next actions and contributor extension points.
- Runs fully offline with no API keys and no network access.

## Contribution map

Good first contributions:

- Add OpenTelemetry mapping.
- Add LangSmith imports.
- Add privacy scrubbing.
- Add replay runners.

Larger contributions:

- Add a JSON Schema and compatibility tests.
- Build import/export adapters for popular AI frameworks.
- Add real-world fixtures from public, non-sensitive examples.
- Improve scoring with transparent, documented heuristics.

## Project principles

- Human agency over blind automation.
- Open standards over vendor lock-in.
- Auditable decisions over hidden magic.
- Privacy and safety as design constraints, not release notes.

## GitHub Pages

The marketing site lives in `site/index.html`. Enable GitHub Pages from the `site` folder or use the included Pages workflow after publishing.

## Security

This project does not process secrets by default. If you build adapters that touch production systems, keep least privilege, explicit consent, and auditable logs in the design.
