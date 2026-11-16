---
name: github-admin
description: Triage GitHub issues and PRs, route code/review/test work, manage labels and draft readiness, assess completion and escalate conflicts. Use when coordinating repository work; status-only requests stay read-only.
---

# GitHub admin

Read the [root contract](../../../AGENTS.md) and [harness routing](../../../docs/agent-setup/agent-harness.md). This skill guides the base agent now; it does not register a Bonsai runtime route. Runtime GitHub writes go through the trusted supervisor. In the coding client use its available GitHub tools within the user's authorized task.

## Classify and route

Inspect the request, current PR head/base, changed components, existing assignments, reviews and checks. Produce a compact decision with action, reason, evidence/head SHA, owner, dependencies and blockers.

| Need | Next action |
| --- | --- |
| Concrete small application change | Base developer; `agent:coder` only if explicitly delegated and verified installed |
| Large/multi-component change or valuable vague proposal | [bonsai-planner](../bonsai-planner/SKILL.md), then scoped code generation |
| External feature/competitor question | [bonsai-researcher](../bonsai-researcher/SKILL.md), returning its brief to this decision/planner |
| Meaningful missing test coverage | [bonsai-ci](../bonsai-ci/SKILL.md) test-specialist handoff |
| Product guide change | Same skill, documentation handoff |
| Independent assessment | [pr-repair](../pr-repair/SKILL.md) read-only review or verified installed Reviewer |
| Simple conflict | One bounded repair through `pr-repair` |
| Semantic/ambiguous conflict | Report conflicting paths/hunks and the unresolved choice |

Reuse assignments; do not issue duplicate work. Planning and research can be artifacts attached to the current request/PR. Do not create fictitious issue routes for these skills.

A simple conflict is one approved file with a mechanical resolution and focused deterministic checks, without changing public contracts/security/schema. Stop if resolution needs design decisions, broader scope, failing checks or moved refs. Report escalation rather than force-pushing or guessing.

## Labels and draft readiness

Use the repository's label catalog and aliases. Add relevant `feature`/`enhancement`, `bug`, `refactor`, `documentation`, `tests`, `maintenance` or `performance` labels without replacing unrelated labels. For a missing label propose name, description, color and reason; create only under owner authorization or existing label-creation policy, after rechecking for concurrent creation.

For an authorized delivery/administration request, mark an eligible draft PR ready for review after implementation and essential tests/docs are reviewable and no known blocker/conflict remains. Respect owner holds, refresh the head immediately before the transition and confirm the resulting draft state. Pending CI may remain visible if repository policy permits.

Inspect actual merged workflows before using `ready-to-merge`. Under the proposed CI gate, apply it after pre-CI readiness is established; do not require CI success before requesting CI. A non-draft PR is not automatically CI-enabled. `ready-to-merge` is not issue `ready` or proof of merge readiness. Reassess changed heads and withdraw this automation's CI label when newly discovered blockers or an owner hold require it; do not remove someone else's labels silently. Report that removing the label does not cancel already running jobs.

## Completion report and stopping point

Report implementation, tests, documentation, review, required CI, conflicts and overall status separately, tied to the current head. Missing/unknown/pending/skipped evidence is not a pass. A path-excluded check can be not-applicable only with a verified policy reason. Use `waiting`, `incomplete`, `unknown`, `ready_for_owner_review` or `complete` honestly; confirm merged status from GitHub.

Status-only requests make no metadata writes. At delivery inspect asynchronous evidence once, report exact next action and finish. Do not poll for CI/workers, approve a PR review, merge or deploy implicitly.
