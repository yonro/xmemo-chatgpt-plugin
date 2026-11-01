---
name: xmemo-review-plan
description: Review a proposed plan against saved XMemo goals, decisions, constraints, and current evidence. Use for a plan critique or acceptance recommendation, not implementation progress verification.
---

# Review a Plan with XMemo

Test a proposal against durable context before execution. Follow
**scope → baseline → decompose → challenge → verdict → gate**.

## 1. Define the review contract

Identify the plan version, outcome, project or scope, decision owner, risk
tolerance, and required depth. Distinguish draft, proposed, approved, and
implemented states.

## 2. Recover the authoritative context

Use `recall_context` for the bounded decision set, `search_memory` for exact
constraints, `get_project_summary` for current project state, and `todo` for
active commitments. Retrieve only context that can affect the review.

Resolve conflicts by current user instruction, verified evidence, recency, and
scope. Use `explain_memory` when a decisive match or its provenance is unclear.

## 3. Decompose and challenge the plan

Map goals, assumptions, dependencies, sequencing, ownership, rollback,
verification, acceptance criteria, and unresolved choices. Check:

- alignment with saved goals and constraints;
- contradictions with settled decisions;
- missing evidence, dependencies, migration, or recovery paths;
- security, privacy, data-loss, compatibility, and operational risks;
- testability, observability, and release gates;
- duplicated completed work or ignored lessons;
- cross-agent ownership and handoff boundaries.

## 4. Return a formal review

Use:

1. **Plan and baseline reviewed**
2. **Verdict** — `recommended`, `changes_requested`, `blocked`, or `rejected`
3. **Critical findings**
4. **Required changes**
5. **Risks and assumptions**
6. **Missing evidence or decisions**
7. **Acceptance gate** — exact evidence required before approval or execution

Separate blocking findings from optional improvements. A favorable review is
a recommendation, not user approval or authorization to execute.

## 5. Preserve the outcome carefully

Keep the verdict and user approval distinct. If saving the review is authorized,
save its durable rationale with `remember` or `update_memory`. Use `todo`,
`update_state`, or `record_event` only for the separately authorized outcomes.
Approval of the plan alone does not authorize any of these writes.

Clarify unresolved write scope and return a receipt for authorized writes. Never
claim implementation or deployment merely because a plan passed review. Read
`../xmemo-memory-steward/references/review-playbooks.md`,
`../xmemo-memory-steward/references/memory-policy.md`, and
`../xmemo-memory-steward/references/tool-routing.md` for detailed rules.

## Shared boundaries

Before any tool call, read and apply
[plugin boundaries](../xmemo-memory-steward/references/plugin-boundaries.md).
Use [tool routing](../xmemo-memory-steward/references/tool-routing.md) for unfamiliar
operations, [temporal queries](../xmemo-memory-steward/references/temporal-queries.md)
for dates or chronology, and [memory policy](../xmemo-memory-steward/references/memory-policy.md)
before writes. Reuse existing authorization; clarify only unresolved scope.
Report failed or unconfirmed operations without claiming success.
