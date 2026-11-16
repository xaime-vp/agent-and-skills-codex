---
name: bonsai-ci
description: Prepare and track scoped Bonsai implementation contributions to an existing PR through prose issue preparation, verified installed admission and supervisor-owned delivery.
---

# Bonsai contributions to the parent PR

Support the [root developer](../../../AGENTS.md). Use issues for meaningful work executed by external Bonsai workers; advisory [admin](../github-admin/SKILL.md), [planner](../bonsai-planner/SKILL.md) and [researcher](../bonsai-researcher/SKILL.md) skills do not each need an implementation issue. Reuse active assignments and do not duplicate local/runtime workers.

The base developer owns application code and PR delivery. Product test/fixture/test-configuration and documentation contributions belong to their workers. Current source also supports coder; delegate application code only when explicitly selected and authorized, with installed support verified.

## Prepare and admit prose work

1. Record repository, parent PR, exact delivery branch, source/head SHA, goal, acceptance criteria and known boundaries. Verify the selected installation's target, sealed release, enabled role, protected checks and resource limits; source support is not installation evidence.
2. Search existing issues and branch reservations. Reuse matching ownership. Keep dependent/unverified handoffs guidance-only without execution labels/envelopes; record the exact next action and finish.
3. Create or update a prose issue. Do not guess exact checks or manufacture JSON merely to dispatch. Match the installed implementation role: `agent:test-specialist`, `agent:documentation`, or explicitly delegated `agent:coder`.
4. Follow [free-form preparation](../../../docs/agent-setup/free-form-issues.md): finalized issue, selected role, configured owner's request, bounded committed evidence, operator `--target-pr NUMBER`, confirmed-stopped prerequisites and inspected sealed proposal. Issue/PR prose alone does not select the execution destination. Preparation is exclusive regardless of slot capacity and does not stop the listener itself.
5. On a verified `admission_mode: ready` installation, remove `blocked`, add issue `ready` and retain exactly one matching implementation role only after scope/checks and current revision are validated. Older installation formats/approval grammar are [compatibility-only](../../../docs/agent-setup/compatibility.md); never post owner commands on their behalf.
6. Serialize contributions to one PR branch. Refresh/reprepare affected proposals when previous contributions change the head. Verify actual commits reached the parent branch, not just a closed issue or completion comment.

Test-specialist and coder have embedded read-only review; documentation has no embedded model reviewer. The separate automatic PR Reviewer is governed by installation policy, not an issue implementation label. Runtime supervisor owns approvals, state, role isolation, process stop, Git and publication.

## CI and delivery

Issue `ready` enables worker admission; PR `ready-to-merge` requests CI only under the merged label-gate workflows. Neither enables planner/researcher runtime profiles. After essential contributions and reviewable implementation, [GitHub admin](../github-admin/SKILL.md) can perform authorized label/draft actions; pending CI is not a reason to withhold the CI trigger.

Inspect delivered changes and asynchronous status once, record source/head, checks actually observed, failures/gaps, advisory findings and remaining owner/operator action. Leave pending work linked and finish without waiting unless explicitly asked to watch it. Never clear unknown state or replay consumed approvals to retry work.

For release/schema diagnosis only, load [runtime details](references/runtime-and-issue.md), [envelope preparation](references/task-preparation.md) or [ordered execution](references/plans.md). The optional `tools/validate_task.py` parses the selected source's envelope schema offline; it is not the default prose workflow and proves no installed readiness.
