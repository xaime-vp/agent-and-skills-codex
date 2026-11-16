# Use workspace skills and call a Bonsai agent

Use this guide from the developer workspace. Application issues/PRs belong to the selected target; harness changes belong to `agent-and-skills-codex`. Read the [root contract](../../AGENTS.md) and [harness flow](agent-harness.md).

## Choose and invoke a skill

In a client supporting named invocation use `$name`; otherwise ask it to read the linked `SKILL.md`. A skill supplies instructions to the base agent. It does not start a separate process or enable a runtime profile.

| Skill | Use | Example |
| --- | --- | --- |
| [github-admin](../../.agents/skills/github-admin/SKILL.md) | Classify work, route assignments, labels, draft readiness and status | `Use $github-admin to triage PR <URL>, propose its next action and appropriate labels.` |
| [bonsai-planner](../../.agents/skills/bonsai-planner/SKILL.md) | Large, multi-component or valuable but vague requests | `Use $bonsai-planner to scope this change before implementation.` |
| [bonsai-researcher](../../.agents/skills/bonsai-researcher/SKILL.md) | Sourced feature/competitor evidence | `Use $bonsai-researcher to compare options relevant to PR <URL> and return sources.` |
| [bonsai-ci](../../.agents/skills/bonsai-ci/SKILL.md) | Scoped worker implementation issues | `Use $bonsai-ci to prepare regression coverage for PR <URL>.` |
| [pr-repair](../../.agents/skills/pr-repair/SKILL.md) | Review or authorized corrections | `Use $pr-repair to review and implement scoped repairs in PR <URL>.` |
| [pr-completion](../../.agents/skills/pr-completion/SKILL.md) | Finish a PR or assess readiness | `Use $pr-completion to finish PR <URL> and report remaining gates.` |
| [pr-submission](../../.agents/skills/pr-submission/SKILL.md) | Publish/update the parent PR | `Use $pr-submission to deliver the current branch with validation evidence.` |
| [bonsai-containers](../../.agents/skills/bonsai-containers/SKILL.md) | Requested Docker worker lifecycle | `Use $bonsai-containers to inspect the target-bound installation.` |
| [skill-maintenance](../../.agents/skills/skill-maintenance/SKILL.md) | Maintain harness instructions | `Use $skill-maintenance to update routing for this capability.` |

Supporting review, impact, validation and multi-PR skills are listed in [root skill routing](../../AGENTS.md#skill-routing-for-existing-pull-requests). Use available connected tools directly; do not start another client or worker just because a skill is invoked. Review/status-only requests remain read-only.

## Select the worker role

| Runtime assignment | Verified current source route | Invocation |
| --- | --- | --- |
| Explicitly delegated code generation | `agent:coder` | Validated/admitted implementation issue; base developer remains the default code owner |
| Tests/fixtures/test configuration | `agent:test-specialist` | Validated/admitted implementation issue |
| Documentation | `agent:documentation` | Validated/admitted implementation issue |
| Reviewer | No implementation issue route | Embedded assessment or trusted automatic PR review setting |
| Supervisor | Trusted program | Controls admission, isolated processes, state and Git |
| Admin/planner/researcher | No registered runtime issue route yet | Workspace skills now; future runtime depends on implemented/installed proposal |

Issue creation and descriptive labels do not trigger implementation by themselves. Current admission needs a validated current issue/proposal, exactly one supported role label, `ready`, no `blocked`, matching checks and available reservations. Older installed contracts require explicit compatibility inspection.

## Request a contribution

```text
Use $bonsai-ci to create or reuse a [test-specialist | documentation] handoff.
Repository: [owner/repo]
Parent PR / delivery branch / current head: [URL, exact branch, SHA]
Goal: [observable behavior and evidence]
Acceptance: [assertions or documentation claims]
Boundaries and dependencies: [known paths and prerequisites]

Prefer prose preparation and explicitly select operator --target-pr NUMBER.
Verify sealed installed role/checks; leave unverified or dependent requests as
guidance without execution labels. Do not post owner commands or start workers.
Preserve concurrent commits and contribute to this same PR branch.
Return issue links, delivered SHAs already present, checks and exact next action.
Finish without waiting for preparation, worker delivery or CI.
```

For explicitly delegated application work, select coder and the authorized scope instead of a test/docs role. Use [prompting](prompting.md) for planning/research requests, [free-form preparation](free-form-issues.md) for operator steps and [compatibility](compatibility.md) only for old formats. There is no need to author an envelope for a normal prose request.

## Admission, review presentation and CI

`ready` on an issue enables validated worker admission. Marking a draft PR ready changes review presentation. `ready-to-merge` on a PR requests CI after the proposed gate merges. These are independent operations.

When pre-CI work is reviewable, GitHub admin may mark the draft ready and add the CI label under existing authorization. Required CI can still be pending then. Completion requires actual current evidence; skipped jobs on an unlabeled PR are not test passes. Check merged workflows, owner holds and policy before metadata writes.

## Follow automatic PR review

Verify effective installed policy rather than inferring it from labels. Deployment templates currently enable automatic review by default; a missing installed `automatic_pr_reviews` remains off. Advisory reviews do not execute tests or enable implementation. Report review evidence already available at the actual commit and finish; do not reset consumed records or wait for another review.
