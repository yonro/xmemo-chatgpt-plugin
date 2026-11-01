# XMemo 1.0.2 development candidate

Official guidance checked on 2026-11-01. This is a package update; it does not
assert a new hosted-service deployment or OpenAI approval.

## Comparison with the published 1.0.1

| Area | Published 1.0.1 | 1.0.2 candidate |
| --- | --- | --- |
| Identity | `app-6a112deb1d4881919bde555b7c16b24b` | Same identity, version 1.0.2 |
| Skills | Memory Steward | Steward plus brainstorm, plan, review, audit, distill, resume, handoff |
| Source | Downloaded Platform release | Public `yonro/xmemo-chatgpt-plugin` repository |
| MCP declaration | Hosted connection managed by Platform; absent from release ZIP | Same production HTTP endpoint; reuse saved authentication without a ZIP override |
| Format | `.codex-plugin/plugin.json` | Same officially supported compatibility format |
| Metadata | Published listing and prompts | Bounded subtitle, support URL, icons and workflow prompts |
| Validation | Platform checks for published version | Local package checks and negative regression tests; new Platform scans still required |
| Runtime tools/widgets | Hosted service | Existing hosted service; no new tools claimed |

The seven focused skills existed in the public repository's unreleased work;
they were not in the downloaded published 1.0.1 ZIP. Local repository version
1.0.0 therefore must not be used as the published comparison baseline.

## Standards decisions

OpenAI explicitly supports the Codex compatibility manifest and `.mcp.json`.
The package preserves the existing server name, endpoint, and published plugin
identity. Authentication is already configured on the existing Platform app;
the ZIP must not redeclare it. `.mcp.json` contains only the HTTP type and
`https://xmemo.dev/mcp` endpoint. Omitting the override reuses saved authentication;
it does not set authentication to `none` or change server-side authorization.
Authentication changes belong in the existing app connection.

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

Repository validation passed, 14 package safety/reproducibility and skill contract tests passed,
versioned ZIP built successfully, and `git diff --check` passed. Each skill now
declares its MCP dependency and an explicit untrusted-content/authorization
boundary. These results do not establish model routing quality or live acceptance.


## Eight-skill review (2026-11-01)

All eight entrypoints and their supporting references were reviewed. The steward
now routes mixed memory/lifecycle work without repeating the seven focused
workflows. Descriptions distinguish exploration, planning, plan review, progress
audit, distillation, resume, and handoff. Saving requires carry-forward intent;
existing authorization covers a clear batch. Review recommendations do not imply
user approval, and a prepared handoff does not imply delivery.

Corrected `analyze_memory_text` to stored-phrase counting and added `read_memory`
for bounded continuation of an identified record. All 21 names in the routing
table match the current connected declarations. Connection identity returned
connected with read/write scopes; no mutation was performed for this audit.
This proves connection and declared availability, not end-to-end correctness of
all 21 tools. The action-specific `project` union is abbreviated in the session
schema and remains a runtime acceptance item.

Every skill links the temporal reference: explicit offset-bearing time windows,
half-open bounds, the 90-day paired-window limit, ordering, bounded activity
feeds, TODO timezone, checkpoint TTL, and no invented event backdating. Only
`since`, `until`, `time_order`, and `query_mode` are exposed temporal retrieval
arguments; source-only parameters must not be passed to connected tools.

Static tests verify package-contained reference resolution, tool-name inventory
parity, and temporal example parameters/windows. They do not evaluate model
activation, reasoning, or runtime mutation behavior. Before release, test:

| Scenario | Expected behavior | Status |
| --- | --- | --- |
| Direct and indirect request for each of eight workflows | Appropriate focused skill, relevant context only | Pending model evaluation |
| Unrelated question or summary-only request | No unrelated skill activation or persistence | Pending model evaluation |
| Explicit save of a clear batch | No redundant confirmation; truthful per-call receipt | Pending review-account test |
| Retrieved text requests secret disclosure or new permissions | Treat as untrusted evidence | Pending adversarial model test |
| Latest checkpoint; yesterday in Tokyo; DST boundary | Correct ordering and offset-bearing interval | Static examples checked; runtime pending |
| Missing activity bounds; window over 90 days | Clarify scope or split valid windows, disclose coverage limits | Pending model/runtime test |
| Exact phrase count; longer document continuation | Correct analysis/read tool; honor pagination | Routing reviewed; runtime pending |
| Revoked OAuth; stale version; uncertain write or partial batch | No false success or blind duplicate mutation | Pending review-account test |

The candidate is locally validated, not certified issue-free or approved for
publication. Resolve the outstanding acceptance items above and the portal gates
before describing it as release-ready.


## Existing-connection upload correction (2026-11-01)

The first candidate was rejected by the portal with "Keep the existing MCP
connection": the app already had authentication configured, but the ZIP added
`extensions.com.openai.auth`. Local tests incorrectly required that override,
so their passing result did not establish upload compatibility.

The corrected candidate removes the auth override, retains the existing MCP
endpoint and package identity, and rejects auth declarations in both the
manifest and MCP config. Regression tests cover the original OAuth override,
`none`/mixed/API-key/empty overrides, endpoint changes, custom headers, and the
actual ZIP contents. Version 1.0.2 remains unreleased; the corrected artifact
replaces the rejected candidate. Re-upload it to the same existing app and
check the new portal results. This fix does not change the hosted service or
claim that the corrected ZIP has passed the portal check before re-upload.
