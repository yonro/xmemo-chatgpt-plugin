# Temporal queries

Use this reference for relative dates, latest/oldest results, timeline reads,
TODO due dates, or checkpoint expiry. Check the current connected schema first.

## Memory retrieval

`recall`, `search_memory`, and `recall_context` expose `since`, `until`,
`time_order`, and `query_mode` alongside their query and result limits.

- Convert a stated date/window to absolute RFC 3339 timestamps with timezone
  offsets in the user's known local timezone. Ask if a missing timezone or
  ambiguous period changes the answer. Do not use the server's timezone.
- Windows are half-open `[since, until)`: use the next local midnight for an
  inclusive end date, not 23:59:59. Respect daylight-saving offsets separately
  at each endpoint. `until` must be later than `since`; paired bounds may span
  at most 90 days. For longer requests, use bounded windows and disclose any
  result limits; do not claim exhaustive coverage from capped results.
- Set `time_order="desc"` for latest/newest and `"asc"` for oldest-first.
  Latest alone is ordering, not an invented date cutoff. Clarify an ambiguous
  "recently" period when needed, or state the assumed window.
- Use `query_mode="topic"` for topical retrieval. Use `"activity_log"` only
  for an event feed, always with both explicit bounds; unbounded activity
  requests must first be scoped.
- These retrieval schemas do not expose `owner_timezone`, `reference_time`,
  or `temporal_axis_mode`. Use timezone knowledge to calculate timestamps,
  not as an extra argument. Do not promise updated-time sorting or event-time
  semantics that the response does not establish.

Examples below are call arguments, not evidence that calls were executed.
For the yesterday example, the known current date is 2026-11-01 in Asia/Tokyo.

```json
{"tool":"search_memory","arguments":{"query":"XMemo decisions","since":"2026-10-31T00:00:00+09:00","until":"2026-11-01T00:00:00+09:00","time_order":"desc","query_mode":"topic","limit":10}}
```

```json
{"tool":"recall_context","arguments":{"query":"XMemo checkpoint","time_order":"desc","max_items":5,"max_tokens":2000}}
```

```json
{"tool":"recall","arguments":{"query":"project milestones","query_mode":"activity_log","since":"2026-10-25T00:00:00+09:00","until":"2026-11-01T00:00:00+09:00","time_order":"asc","limit":20}}
```

## Other temporal operations

- `todo`: `due_at` is an ISO timestamp; `due_before` filters list results.
  Listing uses the real IANA `owner_timezone` unless a saved profile provides
  it. Do not confuse TODO due dates with memory retrieval windows.
- `update_state`: `ttl_seconds` controls expiry, from 0 through 2592000;
  zero means no expiry. TTL is not an event timestamp or scheduled reminder.
- `record_event` exposes no `occurred_at` argument. If recording a historical
  occurrence is requested, describe its actual time in content and distinguish
  it from the record's creation time; do not claim to backdate the event.
- `analyze_memory_text` accepts `since` and `until` for stored-text counts,
  but not retrieval ordering or query-mode arguments. Other tools have their
  own date fields; never copy a retrieval call's arguments into them.
