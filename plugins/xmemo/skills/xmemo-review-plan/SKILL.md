---
name: xmemo-review-plan
description: Review a proposed plan against XMemo's saved goals, decisions, constraints, lessons, project state, and acceptance criteria. Use for architecture, implementation, migration, or launch plans produced in ChatGPT, Codex, or another agent. Return a formal verdict and review gate; never mistake a proposal for approved work or implemented progress.
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
2. **Verdict** — `approved`, `changes_requested`, `blocked`, or `rejected`
3. **Critical findings**
4. **Required changes**
5. **Risks and assumptions**
6. **Missing evidence or decisions**
7. **Acceptance gate** — exact evidence required before approval or execution

Separate blocking findings from optional improvements.

## 5. Preserve the outcome carefully

Do not save the proposal as approved unless the user approves it. After
approval, save durable rationale with `remember` or `update_memory`, create
concrete actions with `todo`, preserve unresolved blockers and execution start
with `update_state`, and record material approval with `record_event`.

Preview multi-record writes and return a receipt. Never claim implementation or
deployment merely because a plan passed review. Read
`../xmemo-memory-steward/references/review-playbooks.md`,
`../xmemo-memory-steward/references/memory-policy.md`, and
`../xmemo-memory-steward/references/tool-routing.md` for detailed rules.
