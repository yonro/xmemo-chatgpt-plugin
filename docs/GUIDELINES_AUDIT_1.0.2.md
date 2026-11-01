# XMemo 1.0.2 plugin guidelines audit

Status: package corrections implemented; service and submission acceptance remain separate.
Verified: 2026-11-01. Scope: the seven-skill 1.0.2 package, current connected tool
inventory, bounded main-service source/tests, and public URL availability.

## Standard and evidence

Reviewed the full [official plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines),
including plugin fundamentals, MCP requirements, and skills. The fetched Markdown
SHA-256 was `d756819aa5e7c9db77db43224910ebf90ba1590c9f990c7ef3b2b851384fac43`.
The guidelines can change; this is a dated assessment, not OpenAI approval.

Package baseline: `8ebf310711a1531683bccb293cad3fc7eb6185ab`.
Main-service source baseline: `18a028d930e1e3800a8bdb46d60773780b1ee116`.
The [connected contract](../submission/connected-tool-contract.json) describes
21 tools. The older submission JSON is a historical snapshot, not proof of the
current runtime, permissions, or accepted listing.

## Findings and corrections

| Finding | Correction and status |
| --- | --- |
| Some specialist write steps implied that approving a plan or recommendation also authorized persistence. | Fixed brainstorm, planning, and plan-review steps. Saving, events, TODOs, and checkpoints follow actual authorized scope; existing permission is reused. |
| Restricted-data exclusions and collection boundaries were incomplete and scattered. | Added shared [plugin boundaries](../plugins/xmemo/skills/xmemo-memory-steward/references/plugin-boundaries.md), required before every skill's tool use. Covers inputs and returned content, PCI data, PHI, government IDs, credentials, minimization, precise location, user control, and commerce. Instruction coverage does not certify server enforcement. |
| Resume and handoff duplicated recovery/reconciliation. | Combined into Work Continuity with three distinct modes: resume, prepare handoff, receive handoff. Preparing/saving is not sending or receiving; a readiness recommendation does not authorize execution. |
| Basic save/recall discovery was weak. | Retained one general Memory Steward; starter prompts and descriptions explicitly cover ordinary preferences, recall, and resume. No separate save/recall skills. |
| Ledger routing could imply unsupported subscription mutations or actual financial execution. | Restricted routing to expense records and existing subscription history; explicitly excludes payment execution and retired subscription writes. |
| Existing authenticated app uploads reject ZIP authentication overrides. | Preserved endpoint-only `.mcp.json`, original package identity, and saved app authentication. Regression tests reject overrides and connection drift. |
| `remember` can supersede an existing preference but advertised an additive annotation and omitted that side effect. | Corrected in main-service [PR #372](https://github.com/yunze7373/memory-os/pull/372), pending review and deployment. Skills now disclose that `remember` is not append-only and prefer exact-target updates for corrections. A ZIP cannot change hosted annotations. |
| Optional service redaction does not establish an unconditional restricted-data boundary. | Recorded as a runtime defense-in-depth limitation. The package prohibits these data; additional automatic input filtering is deferred from this package change. The guidelines do not prescribe a universal classifier, and pattern-based filtering cannot establish complete PHI or all-identifier coverage. |

## Skill consolidation

The maintainer selected seven skills. Only resume and handoff were merged:

| Skill | Distinct responsibility |
| --- | --- |
| Memory Steward | Ordinary save, recall, application, correction, lifecycle, and tool/skill selection |
| Brainstorm | Compare alternatives before committing to a direction |
| Plan Project | Produce scoped, executable phases and acceptance evidence |
| Review Plan | Evaluate a proposed plan before execution |
| Audit Progress | Reconcile claims with evidence of work already performed |
| Distill Session | Extract and deduplicate durable outcomes from a session |
| Work Continuity | Recover work or prepare/receive a handoff with provenance and access limits |

Further merging would blur prospective review versus retrospective verification,
or durable extraction versus operational continuation. The general skill routes
to all six companions; ordinary memory needs neither a project nor another skill.

## Requirement coverage

“Source checked” below means inspected code or packaged instructions and bounded
local checks. It does not mean the installed host or production service passed.

| Guideline area | Evidence and assessment |
| --- | --- |
| Purpose and originality | Cross-conversation, authorized XMemo memory is the specific service. No OpenAI endorsement or comparative claims in packaged metadata. Ownership/permission for branding remains the publisher's attestation. |
| Quality and reliability | Error, unavailable connection, stale evidence, pagination, partial batch, and uncertain-write handling are explicit. Local package tests pass. Live latency, availability, and end-to-end behavior remain acceptance checks. |
| Name, description, prompts | Brand name XMemo; no MCP/Plugin suffix, pricing, promotions, or unverifiable superlatives. Three concrete starter prompts. Screenshots are not relied on for Directory presentation. |
| Usage policies and general audiences | No mature content in inspected skills; maintainer confirms no adult content. Shared boundaries prohibit harmful activities and targeting under-13 users. Account signup age and content suitability are distinct; this audit does not alter legal eligibility or certify all future stored content. |
| Respect user intent | Corrected approval/write ambiguity; no full-chat archival or unsolicited handoff sending. Tool availability and workflow completion do not grant authority. |
| Fair play | No instructions to disparage or override competing plugins, host rules, or user choices. Recalled text is untrusted evidence, not authority. |
| Third-party access | Uses the existing authenticated XMemo endpoint. No unofficial pass-through, scraping dependency, or rate-limit bypass in the package. External source use still requires authorization. |
| Privacy policy publication | Privacy URL returned HTTP 200 without credentials or redirect. Policy contains categories, purposes, recipients, retention criteria, and user controls. Actual processing, retention execution, and backup/log alignment require operator verification; the URL check proves reachability only. |
| Data minimization and restricted data | Shared instructions prohibit restricted categories in queries, writes, and redistribution. Source audit identified limits in optional server redaction; additional filtering is deferred. Local instructions and regex coverage cannot justify a blanket compliance claim. |
| Regulated sensitive data | Requires necessity, adequate consent, and disclosure before collection; unclear cases stay unsent. User consent cannot override restricted-data exclusions. |
| Tracking transparency and user control | Source separates account/technical processing from deliberately saved memories; corrected the repository privacy summary accordingly. Production telemetry, controls, and policy alignment were not exhaustively audited. |
| Commerce and monetization | No plans, checkout links, upsells, advertisements, money transfers, or investment execution in the package. Inspected MCP/widget paths reject retired subscription writes. Ledger recordkeeping is distinct from selling subscriptions. Price parity and all deployed entitlement messages remain operational checks. |
| Prohibited goods/services and checkout | No commerce workflow supplied; shared rules exclude prohibited activities. Checkout requirements are inapplicable to this package's recordkeeping behavior. Any future commerce feature needs a fresh review. |
| Developer verification and support | Metadata names Yonro and provides support URL/email; support URL returned 200. Platform verification, business affiliation, IP rights, and actual support responsiveness require publisher/portal confirmation. |
| Tool names and descriptions | 21 declared tools have purpose-oriented descriptions and defined schemas. Corrected skill routing; `remember` overwrite disclosure needs the separate service fix. |
| Tool independence and exposure | No external plugin dependency or discovery/schema-fetch generic executor found. Action-based tools expose their schemas directly; review must still assess their per-operation exposure against the guideline. No claim of platform acceptance is made. |
| Correct annotations | All 21 descriptors have explicit `readOnlyHint`, `destructiveHint`, and `openWorldHint`; 12 read-only and 9 write tools. `remember` had a reproduced overwrite mismatch requiring a service fix. Undo/version history does not exempt overwrites. |
| Minimal inputs | Public profile filters undeclared/private fields. No raw conversation array or required precise-location field in inspected public schemas. Skills send targeted context; IANA timezone for chronology is not GPS/address collection. |
| Predictable behavior and retries | Skills disclose version/idempotency requirements and reconcile uncertain writes. `remember` has no client mutation ID. Local source tests cover profile/input constraints; hosted retry behavior still needs acceptance. |
| Response minimization | Inspected identity and workspace paths remove internal IDs/request metadata. Required memory IDs, versions, and event dates support exact reads/updates. This was bounded source inspection, not an exhaustive output audit. |
| Data boundaries and safeguards | No full-chat reconstruction instruction; exact-target lifecycle and permanent-delete confirmation rules remain. Server policy gaps and host confirmation UX are separate from skill coverage. |
| Authentication and permissions | ZIP preserves existing authentication; public discovery endpoints respond. Tool descriptors advertise memory read/write scopes. Verify the saved app requests only necessary scopes: the service's legacy omitted-scope fallback also includes knowledge scopes. No live OAuth roundtrip or token renewal test was performed. |
| Optional UI and iframes | Three inspected widget resources have restrictive CSP and deployment-specific asset origins. No nested third-party iframe/checkout found in inspected paths. If embedded pages are introduced, declare frame domains and submit justifications. Desktop/mobile rendering remains unverified in this audit. |
| Testing and reviewer credentials | Local checks and synthetic service tests ran. A functioning sample-data reviewer account and accessible login flow must be supplied privately through Platform, not committed here. No live reviewer-login verification. |
| Skills and automatic scans | Seven skill formats and relative-resource/routing contracts checked locally. Portal security/skill scans must pass for the rebuilt ZIP; local checks are not a substitute. |

## Validation performed

- Plugin regression suite: 16 passed, covering deterministic packaging, seven
  skills, original identity/version, required steward, auth/endpoint preservation,
  path traversal, symlinks, unexpected files, metadata, relative references,
  connected tool inventory, and temporal parameter/window contracts.
- Skill-creator validation: all seven skills; repository validator and diff check.
- Built ZIP inspected for seven skills, version 1.0.2, original app identity,
  and endpoint-only MCP configuration.
- Main-service pre-fix source tests: 14 profile/descriptor/input/sanitizer checks
  and 13 CSP/OAuth checks passed. Warnings concerned an unresolved Pydantic
  lifespan annotation and deprecated Starlette TestClient/httpx integration.
- Synthetic fake-repository execution reproduced preference supersession; no
  real user memories or production databases were changed by the audit.
- Public GETs returned 200 for homepage, privacy, terms, support, protected-resource
  metadata, and authorization-server metadata on 2026-11-01. Scanner access can
  still differ; a successful local request is not a portal scan result.

Reproduce plugin checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_repo.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/package_plugin.py v1.0.2
git diff --check
```

## Separate service correction

[Main-service PR #372](https://github.com/yunze7373/memory-os/pull/372) changes
`remember` annotations and descriptions to disclose existing overwrite behavior;
it does not change memory business logic or add tools. It remains a draft and
has not been merged or deployed. Its 189 focused tests passed. The required local
quick CI passed 7 of 11 checks; 4 frontend/Docs checks could not pass because root
frontend dependencies and generated assets were absent. No thresholds were lowered.

Additional restricted-input hardening was explored, then deferred to keep this
package delivery scoped. No second service PR was created; unfinished edits were
removed from the main-service checkout. This does not establish production data
handling compliance or remove the policy requirement to exclude restricted data.

## Acceptance still required

1. Review, merge, deploy, and verify any separate main-service corrections. A
   public-package merge does not deploy them or change existing hosted tools.
2. Verify restricted-data handling across actual input/output paths, narrow OAuth
   scopes on the saved connection, and operational privacy-policy alignment.
3. Run the rebuilt package's portal scans and authenticated reviewer scenarios:
   ordinary non-project save/read/correct/delete, time windows, failed auth,
   uncertain writes, no-save planning/review, and each continuity mode.
4. Check actual ChatGPT desktop/mobile UI and relevant Codex skill activation.
   Confirm publisher verification and provide reviewer access privately.
5. Submit only after mandatory checks pass. This report does not certify every
   ChatGPT agent mode or guarantee Directory approval.
