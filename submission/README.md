# ChatGPT submission snapshot

This directory preserves the public, non-secret submission material copied from `memory-os` commit `8f90aca5cb8bfeff1fe0433c0a574e12f54a6e28` on 2026-08-01.

- `chatgpt-app-submission.json` uses the official v1 submission schema.
- The snapshot declares 20 public tools, 5 reproducible positive test cases, and 3 negative test cases.
- `prompts.json` maps three starter prompts to compliant screenshots.
- Screenshots use synthetic data and contain no reviewer credentials or private user content.

Do not add reviewer passwords, OAuth codes, bearer tokens, cookies, or private test-account exports here. Private access instructions belong only in the submission portal.

## Connected inventory (2026-11-01)

`connected-tool-contract.json` records 21 tool names, descriptions, and exposed
parameter names from the authenticated Codex session. It is a dated declaration
snapshot, not a full JSON Schema or a successful execution of every tool. The
`project` declaration abbreviates union branches, so its parameter inventory
is null with an explicit limitation instead of falsely listing zero parameters.
The old submission snapshot remains unchanged and must not be used as live parity.
