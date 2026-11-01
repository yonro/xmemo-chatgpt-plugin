# Changelog

All notable changes to XMemo for ChatGPT and Codex are documented here.

## [1.0.2] - Unreleased

- Strengthen the single Memory Steward skill to guide general saving, recall,
  correction, context application, and tool selection without requiring a project.
- Keep eight skills: Memory Steward and seven focused workflows, following the
  Claude plugin's general-entrypoint design with ChatGPT-specific tool routing.
- Make basic memory capabilities visible in the steward metadata and starter prompts.
- Fix existing-app uploads by removing the ZIP authentication override while
  preserving the MCP endpoint and saved connection; add packaging regressions.

- Add seven focused professional skills for brainstorming, project planning,
  plan review, progress audit, session distillation, work resumption, and
  cross-agent handoff.
- Keep the initial OpenAI plugin package explicitly Hook-free; all memory writes
  and checkpoints remain workflow-driven and user-visible.

## [1.0.1] - Published baseline

- Platform release inspected on 2026-11-01: one Memory Steward skill, publicly listed.
- Published package identity: `app-6a112deb1d4881919bde555b7c16b24b`.
- The earlier public repository version is not the Platform release version.

## [1.0.0] - 2026-08-01

- Establish the public XMemo OpenAI plugin repository and repository marketplace.
- Package the production XMemo MCP endpoint and OAuth-backed install flow.
- Include the XMemo Memory Steward skill for recall, distillation, checkpoints, plan review, and cross-agent handoff.
- Preserve the submitted ChatGPT app metadata, prompts, tests, and screenshots as a review snapshot.
- Add repository validation, credential scanning, and tag-driven release packaging.
