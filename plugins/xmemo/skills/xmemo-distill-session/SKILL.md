---
name: xmemo-distill-session
description: Turn an important ChatGPT, Codex, or cross-agent work session into concise, retrieval-ready XMemo outcomes. Use when summarizing key points, preserving decisions and rationale, extracting TODOs and unresolved questions, or saving unfinished progress. Do not archive raw transcripts, filler, secrets, or tentative ideas as confirmed facts.
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

Before multiple writes, uncertain classification, overwrite, or project
placement, present decisions, durable context, TODOs, unresolved items,
working checkpoint, and skipped content with reasons. Label tentative and
verified items; obtain confirmation for the batch.

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
