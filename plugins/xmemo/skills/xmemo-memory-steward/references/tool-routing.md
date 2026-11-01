# XMemo public tool routing

Use only tools available in the connected XMemo plugin. Never substitute a
nonexistent legacy or full-profile tool.

## Connection and memory lifecycle

| Intent | Tool |
| --- | --- |
| Check connection or account identity | `get_mcp_identity` |
| Save a new durable concept | `remember` |
| Correct or revise an existing concept | `update_memory` |
| Soft-delete by default or explicitly hard-delete an exact target | `forget` |
| Restore an eligible soft-deleted memory | `restore_memory` |
| Explain why a memory exists or matched | `explain_memory` |

## Recall and analysis

| Intent | Tool |
| --- | --- |
| Quick recall | `recall` |
| Strict targeted memory search | `search_memory` |
| Bounded multi-memory or resume context | `recall_context` |
| Read a page from one identified memory or Document | `read_memory` |
| Requested memory overview, statistics, or activity | `memory_overview` |
| Count an exact word or phrase across stored visible memories | `analyze_memory_text` |

## Progress and structured work

| Intent | Tool |
| --- | --- |
| Save or replace resumable working state | `update_state` |
| Record a completed milestone, decision occurrence, or handoff event | `record_event` |
| Create, update, complete, or list action items | `todo` |
| Manage transactions or subscriptions | `ledger` |
| Create or mutate an authorized project entity | `project` |

Formal project creation requires:

```text
project(entity="project", action="create", name="<project name>")
```

Omit `project_id` during project creation. For later project mutations, use the
authorized project identifier required by the selected action. Existing
`Projects / <name> / ...` memory paths attach to the formal project; a path must
not silently create one.

## Visual and project surfaces

| Intent | Tool |
| --- | --- |
| Open the interactive TODO Board | `open_todo_board` |
| Open the interactive Ledger workspace | `open_ledger` |
| Get a short project status or next-action answer | `get_project_summary` |
| Open Project Workspaces Home or one project workspace | `open_project_workspace` |

Visual tools are for opening interactive UI. Do not call them when the user
only needs a concise text answer.

## Public-surface boundary

The ChatGPT public tool surface does not expose a dedicated restart-snapshot
restore operation. Reconstruct a resumed session from `recall_context`,
`get_project_summary`, relevant TODOs, and recorded events. Do not claim that
XMemo can reopen the original ChatGPT thread.


## Parameter and mutation discipline

Read the connected schema before a call; tool availability is not proof of
runtime success. Use only exposed parameters. Search scope in query text is
not an authorization filter. For temporal reads, follow
[temporal-queries.md](temporal-queries.md).

- `todo`: create needs `client_mutation_id`; update needs `todo_id`,
  `expected_version`, and `client_mutation_id`. List needs the real IANA
  `owner_timezone` unless the saved owner profile supplies it. Do not send
  mutation-only fields to list; use `item_status` for its status filter.
- `project`: edits/unlinks need the matching reference and `expected_version`;
  memory edits use `memory_ref`, not `memory_id`. Inspect action-specific
  requirements; the session's declaration may abbreviate its union schema.
- `open_todo_board` and `open_ledger` need the real IANA `owner_timezone`.
- Reconcile uncertain write results before retrying. Return partial failures
  honestly; do not imply a multi-call transaction or successful delivery.
