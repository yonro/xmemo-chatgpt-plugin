---
name: xmemo-distill-session
description: Distill a session into concise decisions, durable context, actions, and resumable state for XMemo. Use when extracting outcomes or saving important session results; a summary-only request does not authorize persistence.
---

# Distill a Session to XMemo

Preserve what remains useful after the conversation disappears. Follow
**collect → classify → deduplicate → preview → write → receipt**.

## 1. Identify the durable boundary

Determine the subject, project or scope, and whether the user wants a summary,
a durable save, or both. Do not infer consent for sensitive or ambiguous
writes.

## 2. Extract outcomes, not chronology

Classify:

- final decisions and material rationale;
- stable preferences, rules, constraints, and definitions;
- verified facts, procedures, fixes, and lessons;
- concrete commitments and follow-up actions;
- unresolved questions, choices, or blockers;
- current verified state and exact next action.

Exclude raw transcripts, repeated explanations, long logs, large code blocks,
credentials, private traces, and speculative ideas that were not accepted.

## 3. Deduplicate and preview

Use `search_memory` or `recall_context` when duplicate or superseding content is
plausible. Prefer `update_memory` for a changed concept and `remember` for a
genuinely new durable concept.

When classification, replacement, or project placement is unresolved, preview
the affected candidates and clarify that scope. An explicit request to save a
clear batch already authorizes it. Label tentative and verified items separately.

## 4. Route confirmed outcomes

- new durable concept → `remember`;
- corrected durable concept → `update_memory`;
- concrete action → `todo`;
- unresolved blocker or unfinished state → `update_state`;
- significant milestone or handoff → `record_event`.

Use only routes supported by actual outcomes. Return saved, updated,
checkpointed, skipped, and unresolved counts plus the exact next action. Read
`../xmemo-memory-steward/references/workflows.md`,
`../xmemo-memory-steward/references/memory-policy.md`, and
`../xmemo-memory-steward/references/tool-routing.md` for details.

## Shared boundaries

Before any tool call, read and apply
[plugin boundaries](../xmemo-memory-steward/references/plugin-boundaries.md).
Use [tool routing](../xmemo-memory-steward/references/tool-routing.md) for unfamiliar
operations, [temporal queries](../xmemo-memory-steward/references/temporal-queries.md)
for dates or chronology, and [memory policy](../xmemo-memory-steward/references/memory-policy.md)
before writes. Reuse existing authorization; clarify only unresolved scope.
Report failed or unconfirmed operations without claiming success.
