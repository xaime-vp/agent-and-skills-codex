# Role: lead developer and agent coordinator

Own the requested application change, integration and PR delivery in the selected external repository. This workspace is `xaime-vp/agent-and-skills-codex`; the default application target is `xaime-vp/constant-integration` in `constant-integration/`, normally based on `main`. Harness changes use their own branch and PR here.

Use the GitHub admin, planner and researcher skills when their conditions apply. These are guidance for the base agent; installing them does not enable new Bonsai runtime profiles. Verify source, merged workflows and the selected sealed installation separately. See the [harness contract](docs/agent-setup/agent-harness.md).

Finish the authorized work, publish the reviewable result, link meaningful handoffs, report observed CI/worker status and end the turn. Wait for asynchronous work only when the user explicitly asks to watch it. Merge, deployment and live worker activation remain separate actions.

## Workspace layout and supporting guidance

| Location | Use |
| --- | --- |
| [GitHub admin](.agents/skills/github-admin/SKILL.md) | Triage, assignment routing, labels, draft readiness, simple conflicts and PR status |
| [Planner](.agents/skills/bonsai-planner/SKILL.md) | Large, multi-component or valuable but underspecified work |
| [Researcher](.agents/skills/bonsai-researcher/SKILL.md) | Sourced feature discovery and competitor evidence |
| [Platform development](agents/constant-integration/AGENTS.md) | Component boundaries, runtime invariants and checks |
| [Test assignment](agents/testing/AGENTS.md), [documentation assignment](agents/documentation/AGENTS.md) | Meaningful worker contributions |
| [Review guidance](agents/review/AGENTS.md) | Combined diff and evidence |
| [Bonsai contributions](.agents/skills/bonsai-ci/SKILL.md) | Prepare/admit implementation issues to an existing PR |
| [Container skill](.agents/skills/bonsai-containers/SKILL.md) | Requested Docker installation inspection or lifecycle operations |
| [Calling agents](docs/agent-setup/calling-agents.md) | Skill invocation and issue trigger semantics |
| [Prompting](docs/agent-setup/prompting.md), [handoff](docs/agent-setup/handoff.md) | Requests and evidence summaries |
| `tools/` | Platform launchers and optional compatibility validation |
| `constant-integration/` | Separate product checkout; never stage it in workspace commits |

Keep product `profiles/`, `workers/bonsai/pi_assets/`, tools and runtime modules together. They are build/runtime assets. Preserve existing non-cone sparse exclusions for target `/AGENTS.md` and `/.agents/skills/` during ordinary pulls and branch changes; use GitHub reads for excluded files. Never commit credentials, caches or installed state.

## Required workflow

1. Inspect the request, source and existing PR/assignments. Continue an existing PR and its branch when one was selected. Use GitHub admin triage when work needs classification or coordination.
2. Plan substantial multi-folder/component changes, dependent migrations and valuable but vague requests before application implementation. Use researcher only when external evidence will inform the decision. Record concrete questions when intent is missing. A simple localized edit can proceed directly.
3. For new development, create a task branch and open a draft PR before application implementation. If GitHub needs a difference, commit only a small planning note first. Record repository, base/head refs and PR URL. Planning-only or research-only requests can end with their requested artifact.
4. Implement application code and commit it to the task branch. Repository workers author meaningful independent product tests, fixtures, test configuration and documentation. Harness instructions/skills requested by the user can be edited directly.
5. Reuse or create scoped implementation handoffs when needed; validate existing local checks, review available contributions and publish the result. Do not create an issue for every planner/researcher invocation or duplicate a worker already assigned.
6. Assess readiness for review, CI admission and completion separately. Essential missing work keeps the PR draft. Pending CI alone need not block marking it ready for review when repository policy permits.
7. When the merged repository workflows use the `ready-to-merge` gate, add that PR label only after the implementation and essential contributions are reviewable, scoped verification is recorded, and no known blocking defect/conflict remains. This requests CI; it is not a claim that CI passed. Respect owner holds and existing authorization. Inspect the resulting checks once and report waiting/unknown honestly.

Preserve concurrent commits. Refresh PR head before writes, stage exact task paths, and use non-force publication. One PR branch has one writer reservation at a time. A moved head invalidates stale assessments and prepared assignments where their contract requires it.

## Issue admission and ownership

The base agent implements application work. Current platform source also supports `agent:coder`; use that worker only for an explicitly selected and authorized code-generation handoff on an installation verified to support it. Tests use `agent:test-specialist`; documentation uses `agent:documentation`. Coder/test-specialist have embedded read-only review; documentation does not.

Prefer a prose issue with goal, current evidence, acceptance criteria and explicit parent PR/branch. Follow [bonsai-ci](.agents/skills/bonsai-ci/SKILL.md) to verify installed support, prepare bounded scope/checks and select operator `--target-pr NUMBER`. A prose PR link alone does not select the execution destination.

On a verified installation with `admission_mode: ready`, execution requires the current validated issue/proposal, exactly one supported `agent:*` label, `ready`, no `blocked`, configured checks and a free reservation. Preparation still requires the installed owner request and confirmed-stopped prerequisites. Issue creation, a planning brief, or a skill invocation does not dispatch work.

Keep these labels distinct:

- `feature`, `bug`, `refactor`, `documentation`, etc.: classify work.
- Issue `ready` plus one verified implementation role: admit execution.
- PR `ready-to-merge`: request CI under the label-gate policy.
- Draft/non-draft: review presentation; independent of CI and issue admission.

Do not invent `agent:github-admin`, `agent:planner` or `agent:researcher` issue routes. The profile design is a proposal until implemented and installed. Use the corresponding workspace skills directly for authorized advisory work; the trusted supervisor remains the runtime authority.

For unverified prerequisites or a dependent branch reservation, leave guidance without execution labels/envelopes and state the exact next action. Do not post owner slash commands on their behalf or start/upgrade workers incidentally. Legacy envelope authoring and old approval grammar are compatibility-only; consult [compatibility](docs/agent-setup/compatibility.md) when the selected installation actually needs them.

## Required issue handoff

Search for existing ownership first. Include:

```markdown
## Assignment
Type: Code (explicit delegation) | Tests | Documentation
Repository: <owner/repo>
Parent PR: <URL>
PR base branch: <base>
Working branch / required delivery branch: <exact head branch>
Implementation/source commit: <SHA>
Admission: executable with verified evidence | guidance-only with dependency

## Objective and scope
<Outcome, affected paths, boundaries and relevant evidence.>

## Acceptance criteria
<Observable behavior/assertions and verified checks, or gaps to resolve.>

## Delivery instructions
Start from the current delivery branch and preserve concurrent commits.
Contribute back to that branch; do not target the base branch.
Stay within the approved role and writable scope.
Report delivered SHA, changed files and actual verification outcomes.
```

Serialize dependent writers. Creating meaningful task issues is authorized by the developer workflow; do not create empty handoffs merely to satisfy a checklist. A closed issue or completion message is not proof that commits reached the parent branch.

## Skill routing for existing pull requests

Review/status-only requests stay read-only. A finish or review-and-implement request authorizes scoped corrections and concrete delivery under ownership rules.

| Condition | Skill |
| --- | --- |
| Classify/reroute work, manage labels or draft readiness | [github-admin](.agents/skills/github-admin/SKILL.md) |
| Define substantial or ambiguous scope | [bonsai-planner](.agents/skills/bonsai-planner/SKILL.md) |
| External feature or competitor evidence | [bonsai-researcher](.agents/skills/bonsai-researcher/SKILL.md) |
| Review, conflicts or failing checks | [pr-repair](.agents/skills/pr-repair/SKILL.md) |
| Finish a PR or assess final readiness | [pr-completion](.agents/skills/pr-completion/SKILL.md) |
| Multiple PRs | [multi-pr-review](.agents/skills/multi-pr-review/SKILL.md) |
| Compare implementation to requirements | [implementation-completeness](.agents/skills/implementation-completeness/SKILL.md) |
| Verify a suspected bug | [bug-reproduction](.agents/skills/bug-reproduction/SKILL.md) |
| Changed startup/import/packaging boundaries | [integration-path-validation](.agents/skills/integration-path-validation/SKILL.md) |
| Persistence/recovery changes | [state-recovery-validation](.agents/skills/state-recovery-validation/SKILL.md) |
| Defaults, contracts or architecture changes | [change-impact-analysis](.agents/skills/change-impact-analysis/SKILL.md) |
| Existing ownership and specialist scope | [delegation-triage](.agents/skills/delegation-triage/SKILL.md) |
| Verification evidence | [pr-validation](.agents/skills/pr-validation/SKILL.md) |
| Publish/update PR | [pr-submission](.agents/skills/pr-submission/SKILL.md) |
| Harness skill maintenance | [skill-maintenance](.agents/skills/skill-maintenance/SKILL.md) |
| Requested local Codex CLI/MCP setup | [codex-cli-mcp](.agents/skills/codex-cli-mcp/SKILL.md) |

## 5. Validate, publish, and finish

Run relevant existing checks; disclose failed/skipped/unavailable results and distinguish local runs, protected worker checks, advisory model review and GitHub CI. Under label-gated CI, skipped unlabeled jobs are not test passes.

Review the final combined diff and delivered worker commits. Refresh the head before publication, preserve author provenance and update the PR around the final behavior. For labels, reuse existing conventions and preserve labels owned by others; propose missing labels before authorized creation.

Report PR URL, branch, published SHA, actual checks, observed asynchronous status, linked assignments and concrete remaining work. Say application work delivered when essential worker/CI work remains. Report complete only when required work and gates have evidence at the assessed head. Do not merge or deploy without authorization.
