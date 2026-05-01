"""Red Team Replay: Python-first packet analyzer."""

from __future__ import annotations

import re
from typing import Any

__version__ = "2.0.0"

PROJECT = {
  "slug": "red-team-replay",
  "title": "Red Team Replay",
  "version": "2.0.0",
  "tagline": "Replayable incident traces for AI agent failures.",
  "problem": "AI incidents are hard to reproduce because prompts, tool calls, hidden context, retrieval, and approvals are scattered across logs.",
  "solution": "A normalized replay bundle validator for prompts, context, tool calls, decisions, outcomes, and mitigation notes.",
  "required": [
    "incident.id",
    "incident.severity",
    "trace",
    "mitigation.addedGate"
  ],
  "opportunities": [
    "OpenTelemetry mapping",
    "LangSmith imports",
    "privacy scrubbing",
    "replay runners"
  ]
}

SAMPLE_PACKET = {
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


def _get_path(packet: dict[str, Any], dotted_path: str) -> Any:
    value: Any = packet
    for key in dotted_path.split("."):
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and not value.strip():
        return True
    if isinstance(value, (list, tuple, set, dict)) and len(value) == 0:
        return True
    return False


RISK_PATTERN = re.compile(
    r"(ignore previous|system:|developer:|send secrets|full[-_ ]?access|all permissions|wildcard|unreviewed|unknown)",
    re.IGNORECASE,
)


def _scan_risk_signals(value: Any, prefix: str = "") -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(_scan_risk_signals(item, f"{prefix}[{index}]"))
        return findings
    if isinstance(value, dict):
        for key, item in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else key
            findings.extend(_scan_risk_signals(item, next_prefix))
        return findings
    if isinstance(value, str) and RISK_PATTERN.search(value):
        findings.append(
            {
                "id": "risky-language",
                "path": prefix or "value",
                "severity": "medium",
                "message": "Risky instruction-like or over-broad language detected.",
                "recommendation": "Review this field as untrusted data and keep it separate from system instructions.",
            }
        )
    return findings


def analyze(packet: dict[str, Any] | None = None) -> dict[str, Any]:
    """Analyze a domain packet and return readiness findings."""
    candidate = SAMPLE_PACKET if packet is None else packet
    missing = [
        {
            "id": "missing-required-field",
            "path": field,
            "severity": "high",
            "message": f"Missing required field: {field}",
            "recommendation": "Provide this value so the packet can be audited and reused by other tools.",
        }
        for field in PROJECT["required"]
        if _is_empty(_get_path(candidate, field))
    ]
    findings = [*missing, *_scan_risk_signals(candidate)]
    high_count = sum(1 for finding in findings if finding["severity"] == "high")
    medium_count = sum(1 for finding in findings if finding["severity"] == "medium")
    score = max(0, 100 - high_count * 18 - medium_count * 7)
    status = "ready" if score >= 90 else "needs-review" if score >= 70 else "blocked"
    return {
        "project": {
            "slug": PROJECT["slug"],
            "title": PROJECT["title"],
            "version": PROJECT["version"],
            "runtime": "python",
        },
        "status": status,
        "score": score,
        "summary": f"{PROJECT['title']} found {len(findings)} issue(s); readiness score {score}/100.",
        "findings": findings,
        "nextActions": [finding["recommendation"] for finding in findings[:5]]
        or ["Packet is complete for the v2 Python validator. Consider adding adapter-specific evidence."],
        "contributionIdeas": PROJECT["opportunities"],
    }
