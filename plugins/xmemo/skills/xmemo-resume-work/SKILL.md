---
name: xmemo-resume-work
description: Resume a project or unfinished task from XMemo by recovering the latest verified checkpoint, relevant decisions, TODOs, blockers, and exact next action. Use at the start of a new ChatGPT or Codex session, after an interruption, or when continuing work previously handled by another compatible agent. Reconcile saved state with current evidence before acting.
---

# Resume Work with XMemo

Reconstruct actionable continuity without replaying chat history. Follow
**identify → recover → reconcile → brief → continue → checkpoint**.

## 1. Identify the work precisely

Establish project, task, artifact, branch, environment, or authorized scope.
If several candidates match, present them instead of guessing.

## 2. Recover the minimum complete context

Prefer `get_project_summary` for a known project and `recall_context` for a
task-oriented pack. Add `search_memory` or `todo` reads only to close a specific
gap. Recover objective, acceptance criteria, latest verified checkpoint,
completed work not to repeat, decisions, constraints, artifacts, open actions,
blocker, and exact next action.

## 3. Reconcile before trusting

Compare saved state with the live workspace, newer evidence, and the user's
current correction. Mark statements current, stale, conflicting, or
unverified. Never continue from an uncertain checkpoint.

## 4. Produce a Resume Brief

Return:

1. **Objective**
2. **Verified current state**
3. **Completed work not to repeat**
4. **Active decisions and constraints**
5. **Open TODOs**
6. **Blocker or required input**
7. **Exact next action**
8. **Evidence and artifact references**

Separate remembered context from freshly verified evidence.

## 5. Continue and refresh continuity

If the user asked to continue and the action is safe, execute it without
repeating completed work. If blocked, name the missing authority, evidence, or
external change.

Use `update_state` after verified progress, a new blocker, or a meaningful
pause. Use `record_event` only for a milestone, `todo` for concrete actions,
and `remember` for durable knowledge. Resume restores useful context, not the
original conversation. Read `../xmemo-memory-steward/references/workflows.md`,
`../xmemo-memory-steward/references/memory-policy.md`, and
`../xmemo-memory-steward/references/tool-routing.md` for full checkpoint
contracts.
