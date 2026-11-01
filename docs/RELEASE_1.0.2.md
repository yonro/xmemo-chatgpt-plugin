# XMemo 1.0.2 development candidate

Official guidance checked on 2026-11-01. This is a package update; it does not
assert a new hosted-service deployment or OpenAI approval.

## Comparison with the published 1.0.1

| Area | Published 1.0.1 | 1.0.2 candidate |
| --- | --- | --- |
| Identity | `app-6a112deb1d4881919bde555b7c16b24b` | Same identity, version 1.0.2 |
| Skills | Memory Steward | Ten skills: dedicated save and recall, steward, brainstorm, plan, review, audit, distill, resume, handoff |
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
confirm OAuth, current tool scan parity, desktop/mobile UI and all ten skills.
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


## Initial eight-skill review (2026-11-01; superseded by basic-memory review below)

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


## Revised 1.0.2 after withdrawal of submission

The maintainer cancelled the submission on 2026-11-01 and requested that these
changes remain in 1.0.2. No 1.0.3 release is being prepared.

## Basic memory gap and correction

The initial 1.0.2 candidate exposed save/recall tools and mentioned them inside Memory Steward,
but had no focused basic-memory skills. Its steward UI description and starter
prompt emphasized advanced project workflows. Tool existence did not establish
that everyday save/recall was discoverable or adequately guided.

The revised 1.0.2 candidate adds `xmemo-save-memory` and `xmemo-recall-memory` (ten skills total).
They cover personal preferences, knowledge, decisions, lessons, and procedures
without requiring a project. The steward remains the general coordinator for
mixed recall/save and lifecycle work. Plugin starter prompts expose basic save
and recall directly. Simple authorized saves do not require redundant approval;
recall-only requests do not write; corrections use exact existing records.

## Claude reference and ChatGPT adaptation

Reviewed `xmemo-claude-plugin` commit
`271f537c6898fa78b3c81c68d0dc1bb4c2cbd2a5`, especially
`skills/memory-steward/SKILL.md`. Adapted its useful-context recall, application
of saved preferences, explicit correction, stable organization, and truthful
receipts. Do not copy its host-specific commands, unavailable tools, automatic
checkpoint writes, or redundant batch confirmation into ChatGPT.

The connected ChatGPT tools already provide `remember(content, path)`, exact
`update_memory`, `recall`, `search_memory`, `recall_context`, and `read_memory`.
No server changes or deployment are required. Preserve the existing endpoint,
plugin identity, and omission of ZIP authentication overrides.

## Validation

Run repository validation, package tests, and skill-creator validation for all
ten skills. Build with `python scripts/package_plugin.py v1.0.2`; output is
`dist/xmemo-plugin-v1.0.2.zip`. Rebuild the 1.0.2 artifact after validation; do not reuse the earlier eight-skill ZIP.

Static checks establish packaging and reference integrity, not model activation
or live persistence. Use synthetic fixtures for instruction walkthroughs and a
dedicated review account for actual save/read/update acceptance. Never test
writes against the maintainer's real memories without an explicit test scope.

Required acceptance scenarios: simple Chinese/English save; clear batch; exact
correction; known duplicate; secret exclusion; summary-only no-write; personal
recall; strict no-match; paginated document; local-date and latest ordering;
retrieved instruction injection; failed or uncertain tool results. Confirm both
automatic selection and explicit skill invocation after installation. Portal
scans and real-client end-to-end tests remain separate release gates.


### Revised-candidate results (2026-11-01)

- 15 regression tests passed, including missing-basic-skill rejection and actual
  ZIP inventory checks; all ten skill-creator format validations passed.
- Repository validation, deterministic packaging, and diff checks passed. The
  archive contains version 1.0.2, ten skills, and the endpoint-only MCP config.
- An independent instruction-only walkthrough selected the save skill for a
  Chinese preference, exact correction, and partially failed two-item batch;
  the recall skill for empty lookup, Tokyo yesterday, untrusted retrieved text,
  and paginated Document reading; and no memory tool for a summary-only request.
- The walkthrough identified two wording gaps. The final skills now explicitly
  preserve uncertainty after an empty reconciliation of a timed-out write and
  pin returned document versions on subsequent pages. Static checks were rerun
  after these clarifications; the walkthrough is not a live execution test.
- No real memories were read or mutated for the synthetic scenarios. Platform
  activation, scans, and review-account read/write acceptance remain unverified.
