# Update the workspace and verify compatibility

Start by identifying which repository the request names. This developer harness
is `xaime-vp/agent-and-skills-codex`; its default application target is
`xaime-vp/constant-integration`. The standalone synthetic evaluation harness is
`xaime-vp/CI-testing-and-improvement`. Confirm the checkout's remote before
pulling or creating a PR. Changes belong in the repository that owns the affected
instructions or code; an ambiguous reference to "the harness" needs context.

## Refresh source without disturbing ongoing work

From the developer workspace, inspect both repositories:

```powershell
git remote get-url origin
git status --short --branch
git -C constant-integration remote get-url origin
git -C constant-integration status --short --branch
```

When this workspace is clean and already on its intended base branch, update
with `git pull --ff-only origin main`. Otherwise fetch and use an isolated task
checkout; preserve local edits and ongoing PR branches. Inspect the new base
before deciding what to change: compatibility guidance may already have merged.
Follow the [root branch/PR workflow](../../AGENTS.md) for any new implementation.

Fetching the platform does not change its worktree. To inspect latest platform
source while its normal checkout contains staged edits or an ongoing task:

```powershell
git -C constant-integration fetch origin main
git -C constant-integration rev-parse origin/main
git -C constant-integration worktree add --detach ../../constant-integration-compat origin/main
```

This example creates a sibling of the developer workspace. Choose an unused path
and record its exact commit; detached worktrees are for inspection/validation,
while implementation uses the task's working branch. Preserve the platform's
non-cone exclusions for `/AGENTS.md` and `/.agents/skills/`; do not disable sparse
checkout to update source. Keep target worktrees out of workspace commits.

## Compare source and installed behavior separately

| Evidence | What to verify |
| --- | --- |
| Updated workspace | Workspace SHA and applicable skills/assignment guides |
| Platform source | Exact SHA, [role contract](https://github.com/xaime-vp/constant-integration/blob/main/docs/AGENT_ROLES.md), task parser and protected-check documentation |
| Selected installation | Bound repository, image revision, sealed release, enabled profiles, protected check argv and limits |
| Delivered contribution | Parent PR/branch, actual commit/diff, worker observations and exact-head target CI |

Read [runtime discovery](../../.agents/skills/bonsai-ci/references/runtime-and-issue.md)
and use the [container skill](../../.agents/skills/bonsai-containers/SKILL.md) for
read-only installation inspection. Select the container bound to the actual task
repository; do not assume the default container serves every repository. Image
revision alone does not establish the volume's sealed release.

Current source supports `agent:coder`, `agent:test-specialist` and `agent:documentation`. The workspace keeps application work with the base developer unless coder delegation is explicitly selected. A historical
installation can still require `agent:generalist`, explicit token fields, or a
legacy envelope without free-form preparation support. Verify those facts against
its sealed parser/configuration before authoring executable work. Do not silently
rewrite approvals or enable a new route. Unknown support stays unready; selecting
a supported older route does not authorize an upgrade.

For legacy schema validation, explicitly select the source revision under review:

```powershell
py -3 tools/validate_task.py --platform-root ../constant-integration-compat --repository owner/target --body-file path/to/issue.md
```

The isolated latest source checkout proves only latest-source parsing. For an
older installation, separately validate against its matching reviewed source or
sealed parser and match its configured checks/limits. A successful parse does not
verify approval, installed readiness or delivery. Prose preparation uses its
separate [preparation workflow](free-form-issues.md), not this legacy validator.

Report the workspace/platform/installed revisions separately, commands and actual
results, failed or unrun checks, and any required owner action. Offline parsing,
unit tests and synthetic evaluations do not establish live issue-to-PR delivery.
Pulling source does not stop, start, upgrade or reconfigure an installed worker.

## Compatibility-only authoring and removal

Normal work starts as prose with the [harness routing](agent-harness.md). Only
load [legacy envelope preparation](../../.agents/skills/bonsai-ci/references/task-preparation.md),
[single-task schema](../../.agents/skills/bonsai-ci/references/runtime-and-issue.md#legacy-issue-envelope)
or [ordered execution](../../.agents/skills/bonsai-ci/references/plans.md) when a
verified installed release or explicitly selected format needs them. Their
examples are not evidence that the same approval grammar applies to current source.

Keep `tools/validate_task.py` for those callers. Current prose preparation itself
uses `TaskEnvelope.from_issue` internally, so deleting the parser would break it.
See the [removal audit](agent-harness.md#legacy-removal-audit) for exact source
dependencies and migration prerequisites before retiring runtime compatibility.

Workspace skills do not enable the proposed admin/planner/researcher issue routes.
Verify the implemented registry, merged CI workflows and installed capabilities
before treating design PRs or labels as active automation.
