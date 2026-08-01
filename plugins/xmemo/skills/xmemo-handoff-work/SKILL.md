---
name: xmemo-handoff-work
description: Prepare or receive a professional XMemo handoff between ChatGPT, Codex, Claude, and other compatible AI agents. Use when switching agents, transferring unfinished work, reconciling a received handoff, or preserving a restart-ready package with provenance, evidence, blockers, and one exact next action.
---

# Handoff Work with XMemo

Transfer verified continuity, not confidence or chat history. Follow
**scope → verify → package → persist → receive → acknowledge**.

## 1. Establish the transfer

Identify objective, source, recipient, project or scope, artifacts, direction,
and whether work is paused or complete. Never assume the recipient exposes the
same tools or can access local-only artifacts.

## 2. Verify outgoing state

Recover context with `recall_context` or `get_project_summary`, then compare it
with current files, diffs, tests, deployment state, or user confirmation. Treat
another agent's completion statement as a claim until evidence supports it.

## 3. Build the handoff package

Include:

1. **Objective and acceptance criteria**
2. **Source, recipient, and artifact/version provenance**
3. **Verified current state**
4. **Completed work not to repeat**
5. **Decisions and rationale**
6. **Evidence and relevant artifacts**
7. **Constraints and safety boundaries**
8. **Remaining work and open TODOs**
9. **Blocker or required input**
10. **Exact next action**
11. **Next review or acceptance gate**

Exclude credentials, authorization data, private traces, raw logs, raw
transcripts, and irrelevant internal identifiers.

## 4. Persist deliberately

- replace the scoped checkpoint with `update_state`;
- record the transfer with `record_event`;
- add a `todo` only for a concrete follow-up;
- save durable decisions or constraints with `remember` or `update_memory`.

Preview multi-record handoffs and return a receipt with changed records and
unresolved items.

## 5. Receive and reconcile

Recall relevant state, compare incoming claims with current evidence, and
resolve conflicts by scope, recency, provenance, and verification. Do not
overwrite newer verified state with an older handoff. Return `accepted`,
`accepted_with_gaps`, `blocked`, or `rejected`, plus the exact next action.

XMemo preserves shared context only for agents connected to the same authorized
account and scope. It does not guarantee another agent saved its work, exposes
the same tools, or can reopen the original conversation. Read
`../xmemo-memory-steward/references/workflows.md`,
`../xmemo-memory-steward/references/review-playbooks.md`,
`../xmemo-memory-steward/references/memory-policy.md`, and
`../xmemo-memory-steward/references/tool-routing.md` for detailed rules.
