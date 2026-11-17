# Codex developer adapter

This workspace targets `xaime-vp/constant-integration` in `constant-integration/`
by default. Honor another target selected by the user. Use connected GitHub tools
when sufficient and local Git/checkout execution when needed. Discover actual
capabilities; standalone Codex skills live under `.agents/skills/`.

Use the [shared developer workflow](docs/agent-setup/developer-workflow.md).
The developer owns implementation, tightly coupled regression tests and small
documentation updates. Delegate substantial independent work, specialist expertise
or explicit assignments. Never overlap an active writer's scope.

Inspect existing work, create a task branch, implement and commit a meaningful
initial change, then open a draft PR before any specialist dispatch targeting it.
Do not manufacture planning-only files or commits. Reuse existing PR branches.
Review-only requests are read-only, including issues, metadata and review posts.

Honor the target repository's applicable instructions and native checks. Root
target AGENTS.md is optional. Runtime roles, capacity and admission come from
the selected source and installed release, not this client adapter. The Bonsai
supervisor retains worker scope, credentials, protected checks, review, sealed
resources and publication authority. Merge/deployment/worker operation requires
its own task authorization. Preserve concurrent commits and private data.

Shared copies are recorded in [harness-source.json](harness-source.json). Run
`python tools/check_harness_export.py` and `python tools/harness_check.py`.
For changes to shared content, update the canonical source and regenerate using
[shared exports](docs/agent-setup/shared-exports.md); keep local policy here.

## Asynchronous delivery override

Finish authorized scoped work, validate locally, publish the draft PR and any
selected specialist handoffs, inspect asynchronous status once, then end the turn.
Do not wait for CI, workers or reviews, poll, sleep or launch background watchers
unless the user explicitly asks to watch. This override also applies to finish-PR
requests and supersedes waiting instructions in generated supporting skills.
Report pending work honestly and keep required incomplete work in draft.
