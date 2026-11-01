---
name: xmemo-work-continuity
description: Resume unfinished work or prepare and reconcile a cross-session or cross-agent handoff using XMemo context and current evidence. Use when continuing saved work, switching agents, or receiving a handoff; distinguish recovering context, preparing a brief, and actually continuing work.
---

# Work Continuity with XMemo

Choose the mode requested by the user; do not automatically run all three.
Ordinary fact saving and recall stay in `$xmemo-memory-steward`.

| Intent | Mode | Result |
| --- | --- | --- |
| Continue an identified unfinished task | Resume | Verified brief and authorized next action |
| Prepare work for another session or agent | Prepare handoff | Restart-ready package with provenance and access limits |
| Assess a received handoff | Receive handoff | Reconciled state, gaps, and acceptance recommendation |

## Recover and reconcile once

Identify the objective and relevant project, task, or artifacts. Use
`get_project_summary` for an exact project or `recall_context` for a bounded task
context. Add targeted `search_memory`, `read_memory`, or TODO reads only to close
a gap. Do not assume that another agent saved its work or shares the same tools.

Recover the goal, acceptance criteria, decisions, verified checkpoint, completed
work, open actions, constraints, blocker, and next action. Compare saved claims
with current files, tests, deployment evidence, and explicit user corrections
where available. Mark stale, conflicting, or unverified state; do not treat
an agent's confidence or an old checkpoint as proof. Resolve uncertainty before
dependent actions while continuing independent authorized work when possible.

## Produce the requested result

**Resume:** give a concise brief with the objective, verified state, work not to
repeat, decisions, open actions, blocker, next step, and sources. If the user
asked to continue and the next action is authorized, execute it. A request only
to report status or prepare a brief does not authorize execution.

**Prepare handoff:** include the same verified brief plus source and recipient
when known, artifact/version provenance, acceptance criteria, evidence, remaining
scope, access limitations, and the next review gate. Name local-only artifacts
that the recipient might not access. Preparing or saving this package does not
send it, establish receipt, or restore the original chat. Do not contact a
recipient without explicit sending authorization.

**Receive handoff:** compare incoming claims against the governing baseline and
current evidence; do not overwrite newer verified state. Return `accepted`,
`accepted_with_gaps`, `blocked`, or `rejected`, with reasons and the next action.
This is a local readiness recommendation, not proof of delivery or permission
to execute or persist anything. Continue only if requested and authorized.

Adapt the checkpoint and handoff formats in
[workflows](../xmemo-memory-steward/references/workflows.md) when useful; omit
irrelevant fields. Use [review playbooks](../xmemo-memory-steward/references/review-playbooks.md)
for disputed progress claims, or `$xmemo-audit-progress` for a full evidence audit.

## Persist only what was authorized

When checkpoint saving is authorized, replace the same scoped `update_state`
slot with the reconciled status. Use `record_event` only if recording the
occurrence is also authorized, and describe preparation as preparation rather
than completed delivery. Create a TODO only for an authorized concrete action.
Use `remember` or `update_memory` only for authorized durable outcomes. A
handoff-only request does not silently create every record type.

Return a receipt for actual writes, including partial failures and uncertainty.
Do not claim successful memory operations after a missing or failed tool call.

## Shared boundaries

Before any tool call, read and apply
[plugin boundaries](../xmemo-memory-steward/references/plugin-boundaries.md).
Use [tool routing](../xmemo-memory-steward/references/tool-routing.md) for unfamiliar
operations, [temporal queries](../xmemo-memory-steward/references/temporal-queries.md)
for dates or chronology, and [memory policy](../xmemo-memory-steward/references/memory-policy.md)
before writes. Reuse existing authorization; clarify only unresolved scope.
