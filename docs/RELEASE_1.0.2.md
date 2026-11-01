# XMemo 1.0.2 development candidate

Official guidance checked on 2026-11-01. This is a package update; it does not
assert a new hosted-service deployment or OpenAI approval.

## Comparison with the published 1.0.1

| Area | Published 1.0.1 | 1.0.2 candidate |
| --- | --- | --- |
| Identity | `app-6a112deb1d4881919bde555b7c16b24b` | Same identity, version 1.0.2 |
| Skills | Memory Steward | Steward plus brainstorm, plan, review, audit, distill, resume, handoff |
| Source | Downloaded Platform release | Public `yonro/xmemo-chatgpt-plugin` repository |
| MCP declaration | Hosted connection managed by Platform; absent from release ZIP | Explicit production HTTP endpoint and OAuth declaration |
| Format | `.codex-plugin/plugin.json` | Same officially supported compatibility format |
| Metadata | Published listing and prompts | Bounded subtitle, support URL, icons and workflow prompts |
| Validation | Platform checks for published version | Local package checks and negative regression tests; new Platform scans still required |
| Runtime tools/widgets | Hosted service | Existing hosted service; no new tools claimed |

The seven focused skills existed in the public repository's unreleased work;
they were not in the downloaded published 1.0.1 ZIP. Local repository version
1.0.0 therefore must not be used as the published comparison baseline.

## Standards decisions

OpenAI explicitly supports the Codex compatibility manifest and `.mcp.json`.
Using that supported format avoids asserting conformance to the portable MCP
schema that rejects OpenAI's documented OAuth extensions. OAuth remains explicit;
no authentication downgrade or credentials are included. The endpoint remains
`https://xmemo.dev/mcp` and registration details remain discoverable.

Local checks implement the relevant documented constraints; they do not replace
OpenAI's uploader, security scans, or review. The historical 20-tool snapshot in
`submission/` is preserved as historical evidence, not current runtime truth.

## Validation and release

Run `python scripts/validate_repo.py`, `python -m unittest discover -s tests -v`,
and `python scripts/package_plugin.py v1.0.2`. The artifact is
`dist/xmemo-plugin-v1.0.2.zip`.

Before publication, upload to the existing plugin draft, verify that the MCP
declaration retains the existing connection, and resolve all required findings.
Preserve and verify saved translations, availability, review cases and demo URL.
Run five positive and three negative cases with a dedicated review account;
confirm OAuth, current tool scan parity, desktop/mobile UI and all eight skills.
Provide reviewer access through the secure dashboard, never this repository.
No local check establishes those external acceptance results.

## Ownership

This repository owns plugin manifests, skills, assets, tests and ZIP releases.
The `memory-os` repository owns tool implementations, OAuth, persistence and
hosted widget code. Any necessary service changes require a separate PR there.
This package update does not require changing the service implementation.

## Official references

- [Package format and compatibility](https://developers.openai.com/plugins/build/plugins)
- [Submission and updates](https://developers.openai.com/plugins/deploy/submission)
- [Submission field limits](https://developers.openai.com/plugins/deploy/submission-errors)
- [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)
- [Skill instructions and dependencies](https://developers.openai.com/plugins/build/skills)

## Local results (2026-11-01)

Repository validation passed, eight package safety/reproducibility tests passed,
versioned ZIP built successfully, and `git diff --check` passed. Each skill now
declares its MCP dependency and an explicit untrusted-content/authorization
boundary. These results do not establish model routing quality or live acceptance.
