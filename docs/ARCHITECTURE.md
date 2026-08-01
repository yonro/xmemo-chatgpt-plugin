# Architecture and ownership

XMemo for ChatGPT and Codex is one product with two deployment units.

## Public plugin repository

This repository owns:

- plugin identity, marketplace metadata, icons, screenshots, and starter prompts;
- reusable XMemo skills and workflow guidance;
- public submission snapshots and review evidence;
- package validation, semantic versioning, and release artifacts.

## Hosted runtime

The private `memory-os` repository owns:

- `https://xmemo.dev/mcp` and OAuth Dynamic Client Registration;
- signed client-profile selection and server-enforced authorization;
- MCP tool implementations, input/output schemas, annotations, and aliases;
- ChatGPT widget source, build output, and hosted UI resources;
- persistence, indexing, audit, privacy, and deployment operations.

## Contract rule

The production MCP endpoint is authoritative. A plugin release may expose only capabilities that are already deployed and verified on the public ChatGPT/Codex profile. The submission snapshot records what was reviewed; it is not a second server configuration.

## Why runtime code is not copied here

Duplicating the MCP or widget runtime would create two sources of truth and make security fixes, tool schemas, and deployed behavior drift. This repository packages and documents the integration while the runtime repository remains the single implementation boundary.
