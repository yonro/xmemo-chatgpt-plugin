# Contributing

## Development rules

1. Keep the public plugin package under `plugins/xmemo`.
2. Do not duplicate production MCP, OAuth, database, or widget-runtime logic from `memory-os`.
3. Update the plugin version only as part of an intentional release.
4. Keep tool names and product claims aligned with the current production public profile.
5. Use synthetic data in examples, tests, and screenshots.
6. Run `python scripts/validate_repo.py` before opening a pull request.

Changes to server behavior must land and deploy in the runtime repository before this repository advertises or tests the new contract.
