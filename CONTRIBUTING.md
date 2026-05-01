# Contributing to Red Team Replay

Thank you for helping. This project is intentionally small at the core so contributors can extend it in focused ways.

## Best first issues

- OpenTelemetry mapping
- LangSmith imports
- privacy scrubbing
- replay runners

## Development

```bash
npm test
npm start -- sample
```

## Contribution standards

- Keep the core CLI offline by default.
- Add tests for every new rule or adapter.
- Document new packet fields in the README.
- Avoid sending user data to third-party services unless the user explicitly configures that adapter.
- Prefer transparent heuristics over hidden model-only decisions.
