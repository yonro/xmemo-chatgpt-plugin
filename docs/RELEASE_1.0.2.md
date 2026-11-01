# XMemo 1.0.2 development candidate

The maintainer cancelled the prior submission and requested changes in 1.0.2.
This document describes the current candidate, not OpenAI approval or deployment.

## Comparison with published 1.0.1

| Area | Published 1.0.1 | 1.0.2 candidate |
| --- | --- | --- |
| Identity | `app-6a112deb1d4881919bde555b7c16b24b` | Same identity |
| Version | 1.0.1 | 1.0.2 |
| Skills | Memory Steward | One Memory Steward plus seven focused workflows |
| Basic memory | General steward | Explicit save, recall, correction, application, and tool-routing guidance in the same steward |
| Focused workflows | Not packaged | Brainstorm, plan, review, audit, distill, resume, handoff |
| Connection | Existing Platform authentication | Same endpoint; no ZIP authentication override |
| Runtime | Hosted XMemo service | Existing service; no added server-side tools |

The original eight-skill candidate mentioned save/recall tools but emphasized
advanced project workflows in its UI and did not give the basic operations a
complete workflow. The fix strengthens the existing steward rather than creating
separate save and recall skills. The package must contain exactly eight skills.

## One general memory entrypoint

Memory Steward decides when relevant context should be recalled, when saving is
authorized, which tool to use, and when one of the seven companion skills is
appropriate. Ordinary personal preferences, knowledge, decisions, lessons, and
procedures do not require a project or another skill. Retrieved information is
applied when useful; exact saved-fact corrections update the existing concept.
Generic questions do not trigger private reads, and recall-only or summary-only
requests do not authorize writes. Clear save requests need no repeated approval.

Reads choose among quick recall, targeted search, bounded context, paginated
record reading, and overview. Writes distinguish durable memory, corrections,
TODOs, current state, timeline events, projects, and financial records. Time
windows, version-consistent pagination, ambiguous targets, untrusted content,
partial batches, and uncertain write outcomes have explicit handling rules.

## Claude reference and adaptation

The reference is the latest `xmemo-claude-plugin` version 1.0.6, local and remote
main both verified at `271f537c6898fa78b3c81c68d0dc1bb4c2cbd2a5` on 2026-11-01.
Read `skills/memory-steward/SKILL.md` and its tool-routing reference. Adapted its
single general entrypoint, proactive relevant recall, useful save suggestions,
application of remembered preferences, corrections, stable organization,
truthful receipts, own-connection boundary, and specialized-skill routing.

Only tools exposed by the connected ChatGPT plugin are used. Claude-only
commands and unexposed project/decision tools are not copied. The current
connected inventory is recorded separately from the historical submission
snapshot; neither declaration inventory nor local tests proves runtime success.

## Existing-connection upload correction

The first candidate was rejected with "Keep the existing MCP connection": it
added `extensions.com.openai.auth` to an app with saved authentication. Its local
validator incorrectly required that override. The corrected package preserves
`.codex-plugin/plugin.json`, the published identity, and the existing
`https://xmemo.dev/mcp` endpoint. `.mcp.json` declares only HTTP type and URL.
Omitting an override reuses the saved connection; it does not set auth to none.
Authentication changes belong in the existing app connection.

Regressions reject authentication overrides, endpoint drift, and custom headers,
and inspect the actual ZIP. No runtime service change or deployment is required.

## Validation and submission

Run `python scripts/validate_repo.py`, `python -m unittest discover -s tests -v`,
and skill-creator format validation for all eight skills. Build with
`python scripts/package_plugin.py v1.0.2`; upload the rebuilt
`dist/xmemo-plugin-v1.0.2.zip`, not a previously downloaded candidate.

Before publication, inspect the new portal scans and confirm the saved MCP
connection is retained. Check translations, availability, reviewer access, demo,
and review cases. Execute positive/negative cases with a dedicated review
account, including save/read/update, ordinary non-project use, time windows,
failed authorization, uncertain writes, and skill selection. Check relevant
widgets on desktop/mobile. Local and synthetic tests do not replace these gates.

## Ownership

The public plugin repository owns packaging, skills, assets, tests, and ZIPs.
The `memory-os` repository owns tools, OAuth, persistence, and hosted widgets.
This change requires no main-service edits. Service changes, if discovered in
acceptance, require a separate runtime PR.

## Official references

- [Skill workflows and discovery](https://developers.openai.com/plugins/build/skills)
- [Package format](https://developers.openai.com/plugins/build/plugins)
- [Submission and existing connections](https://developers.openai.com/plugins/deploy/submission)
- [Plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines)


## Local validation results (2026-11-01)

- All 16 regression tests passed, including exact package inventory, required
  steward, companion-skill reference resolution, temporal examples, connection
  preservation, and deterministic packaging.
- All eight skill-creator format checks passed; repository and diff checks passed.
- Inspected the built ZIP: eight skills, version 1.0.2, original identity, and
  endpoint-only MCP declaration. No separate save or recall skill remains.
- Independent read-only inspection confirmed the general steward handles basic
  save/recall/correction and routes plan critique to the existing review skill.
  No unavailable Claude tools or slash commands remain in packaged instructions.
- These are local checks and instruction review, not live XMemo mutations,
  installed-model activation, hosted-runtime acceptance, or portal approval.
