# Agent and skills for Codex

Developer-agent setup for working on external GitHub repositories through GitHub MCP. The setup is maintained in [xaime-vp/agent-and-skills-codex](https://github.com/xaime-vp/agent-and-skills-codex).

Adapted from the `xaime-vp/agent-and-skills` harness. This variant keeps Codex
focused on application code and PR delivery, with tests and product documentation
assigned to repository workers.

The root [AGENTS.md](AGENTS.md) defines the workflow: Codex implements and publishes application changes, while repository workers author tests and documentation through scoped issues targeting that same PR. Codex runs relevant existing checks, leaves concrete worker guidance, reports pending work and finishes **without waiting for CI or other agents**. The external Bonsai supervisor owns execution and publication for its workers.

## Default Codex delivery

- Codex owns application code, integration, commits and PR delivery. It does not write tests, fixtures, test configuration or product documentation.
- Meaningful test/documentation work gets a linked worker issue with implementation evidence, branch context, acceptance criteria and delivery instructions. Existing assignments are reused.
- Worker preparation, admission, branch reservations and approval rules still apply. A dependent or unverified handoff stays guidance-only without execution labels or an executable envelope; Codex reports the next step and finishes.
- CI, worker results and automatic reviews are asynchronous. Codex reports one observed status snapshot without polling or waiting. Later results can be handled in a follow-up task.
- Application delivery and merge readiness are separate. Essential missing work keeps the PR draft; pending CI or optional follow-ups alone do not prevent review when repository rules permit it. Merge and deployment require separate authorization.

For example:

```text
Implement [application change] and deliver the PR. Keep tests and documentation
with repository workers; create or reuse scoped handoff issues with useful guidance.
Run relevant existing checks, report pending CI/worker work, and finish without waiting.
```

Updates to this instruction workspace, including this README and its skills, are
made directly when requested. The worker ownership boundary covers product changes.

For an existing PR, continue its branch with [pr-repair](.agents/skills/pr-repair/SKILL.md).
Review-only requests report findings; review-and-implement requests carry scoped
corrections through validation and delivery. Supporting skills cover impact analysis,
delegation triage and validation when needed. For several PRs, add
[multi-pr-review](.agents/skills/multi-pr-review/SKILL.md) to keep worktrees and
evidence separate. Review support also covers
[implementation completeness](.agents/skills/implementation-completeness/SKILL.md),
[bug reproduction](.agents/skills/bug-reproduction/SKILL.md),
[integration paths](.agents/skills/integration-path-validation/SKILL.md) and
[state recovery](.agents/skills/state-recovery-validation/SKILL.md).

Start with [using skills and calling agents](docs/agent-setup/calling-agents.md)
for available skills, named invocation or direct-file fallback, and a
copyable contribution request. This is the general developer workspace; the
`pi-constant-integration-ui` branch carries UI-specific setup.

Issue handoffs support [free-form preparation](docs/agent-setup/free-form-issues.md)
as well as legacy executable envelopes. Prose issues need no hand-written JSON:
an operator selects evidence and the parent PR, then the owner approves the sealed
proposal digest. Legacy envelopes retain their own schema and standalone approval.
Verify installed support before execution; issue creation alone does not dispatch
approved work.

Current Constant Integration source routes test/fixture work to
`agent:test-specialist` and documentation to `agent:documentation`. The former
includes an embedded read-only review; documentation has no model reviewer.
Generalist/tests are retired source routes. The root developer still owns
application-code changes. Check the installed sealed release before choosing
labels or validating an executable assignment; merged source is not deployment.

Shared capacity supports 1/2/3 slots (missing setting: one). Separately enabled
automatic PR commit reviews are read-only advisory comments, not implementation
handoffs. See [current worker routing and evidence](.agents/skills/bonsai-ci/references/runtime-and-issue.md)
for bounded review retries, local telemetry export and compatibility limits.

## Workspace layout

| Path | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Primary Git developer contract |
| [agents/](agents/) | Platform, testing, documentation and review assignment guides |
| [.agents/skills/](.agents/skills/) | Existing/multiple-PR review, reproduction, integration/recovery validation, completeness, impact analysis, delegation, Bonsai handoffs, containers, submission and Codex CLI MCP |
| [tools/](tools/README.md) | Offline task validation and platform CLI launchers |
| [docs/agent-setup/](docs/agent-setup/prompting.md) | Relocated prompting and manual handoff templates |
| `constant-integration/` | Separately cloned product source; ignored by this repository |

## Codex CLI and existing GitHub MCP

The [Codex CLI MCP skill](.agents/skills/codex-cli-mcp/SKILL.md) explains how to run Codex with a local checkout, connect approved GitHub MCP servers from an existing local `mcp.json` into Codex's own MCP configuration, and create or update issues and draft PRs under the root workflow. A workspace `mcp.json` is not automatically loaded by Codex CLI. Never commit local MCP credentials.

## Update and check compatibility

Follow [workspace updates and compatibility](docs/agent-setup/compatibility.md)
before treating a local checkout as current. Refresh the instruction workspace
and platform source separately, preserve ongoing work, and verify the selected
worker's sealed release before preparing executable handoffs. The separate
synthetic evaluator is `CI-testing-and-improvement`; its application changes
belong in that repository.

## Start a workspace

Clone this repository, then clone the current platform target into its dedicated subfolder:

```sh
git clone https://github.com/xaime-vp/agent-and-skills-codex.git
cd agent-and-skills-codex
git clone https://github.com/xaime-vp/constant-integration.git constant-integration
```

Python 3.12+ is required for the workspace tools. On Windows, use `py -3`; on Linux use a configured Python interpreter. For example:

```powershell
py -3 tools/check.py --component orchestrator
py -3 tools/validate_task.py --repository xaime-vp/constant-integration --body-file path/to/issue.md
```

The launchers use `constant-integration/` without copying or relocating its runtime modules. The validator accepts `--platform-root` for a different source checkout. A successful offline parse does not verify an installed worker, its checks or owner approval. CLI installation and worker startup are separate operational actions.

To keep the upstream target contract out of local instruction discovery, this workspace's existing checkout uses optional non-cone sparse rules. Apply the same rules inside a fresh target checkout if desired:

```powershell
@'
/*
!/AGENTS.md
!/.agents/skills/
'@ | git -C constant-integration sparse-checkout set --no-cone --stdin
```

This changes only the local worktree; the product retains its short committed `AGENTS.md` because Bonsai requires it before processing target tasks.

## Repository boundaries

Constant Integration retains `profiles/`, sealed Pi skills under `workers/bonsai/pi_assets/`, its runtime tools, and product documentation for installation, task schemas, approvals, delivery, CI and recovery. Those are dependencies of the worker. Developer skills, detailed coding-agent setup and prompt/handoff templates live here.

The extraction cleanup in Constant Integration must be merged after this setup is preserved on this repository's base branch. PR links document that dependency; they do not enforce merge order.

Keep `.env*`, `.mcp.json`, credentials, worker state, logs, caches and nested target checkouts out of commits. The ignore rules protect local configuration; connect GitHub MCP in the agent client without publishing credentials. Changes to this setup use a PR in `agent-and-skills-codex`; application changes use a PR in the selected target repository. Neither workflow authorizes merging or deployment by itself.
