---
name: pr-completion
description: Complete the application portion of an existing Codex PR, validate available evidence and prepare worker handoffs without waiting for CI or agents. Use for finish PR or final readiness requests; readiness-only stays read-only.
---

# Complete an existing PR

Read the [root contract](../../../AGENTS.md) and continue the requested PR's current
branch. Use [pr-repair](../pr-repair/SKILL.md) for conflicts and scoped corrections,
[implementation-completeness](../implementation-completeness/SKILL.md) to compare
promises with delivered behavior, and [pr-validation](../pr-validation/SKILL.md)
for revision-bound checks. Load other supporting skills only when needed.

A readiness/status-only request stays read-only: no source edits, issue creation,
PR metadata updates or posted reviews. A finish request authorizes scoped repairs
under repository ownership; merge, deployment and live worker activation remain
separate. An already-complete PR needs verification, not another commit.

Record the actual repository, PR URL, base/head refs and full SHAs, current draft
state and mergeability. Inspect existing reviews, linked assignments and available
checks. Confirm the local checkout matches that head; use an isolated worktree
when it contains unrelated work. Preserve concurrent commits and never force-push
over another contributor. A closed issue is not delivery evidence: inspect the
actual commit and files on the parent branch.

Own scoped application repairs and review contributions already delivered. Create
or reuse meaningful specialist issues with exact branch context and acceptance
criteria; never author worker-owned product tests or documentation. Run relevant
existing local checks, inspect remote status once and finish without polling,
sleeping or starting a watcher. A finish request alone does not request a CI watch.
Leave essential missing work in draft; report application delivery separately
from pending workers or checks. Only an explicit watch request changes this rule.

Use connected GitHub tools when sufficient. Discover live schemas and capabilities;
do not assume a Codex-only agent role or Pi-only nested-tool API exists. If an
authorized subagent is available, assign one executor per PR and reuse its evidence;
otherwise execute directly. Do not launch duplicate local and repository workers.

Before writing, refresh the head. Review the final combined diff, retain author
provenance and revalidate affected work if the head moved. Update authorized PR
descriptions through [pr-submission](../pr-submission/SKILL.md). Keep required missing
work in draft. Unknown mergeability and missing or pending checks are not passes.

Report URL, branch, reviewed/published SHA, repairs or findings, checks actually
run, observed asynchronous status, linked worker issues and remaining work.
Separate application delivery, review readiness and verified merge readiness.
