# Use workspace skills and call a Bonsai agent

Use this guide from the `agent-and-skills-codex` developer workspace on `main`.
The default external target is `xaime-vp/constant-integration`, checked out in
`constant-integration/`; use another target only when the user selects it.
Application issues and PRs belong to that selected repository. Changes to this
instruction workspace use their own branch and PR in `agent-and-skills-codex`.

## Choose and invoke a skill

In a client supporting named skill invocation, request the skill with `$name`.
If discovery is unavailable, ask the client to read the linked `SKILL.md` and its
relevant references. Start from this workspace and identify the external checkout
explicitly. Invocation loads guidance; it does not itself launch a worker or
authorize GitHub writes, installation changes, merging or deployment.

| Skill | Use it for | Example request |
| --- | --- | --- |
| [pr-completion](../../.agents/skills/pr-completion/SKILL.md) | Finish under this harness delivery rules | `Use $pr-completion to finish PR <URL>.` |
| [skill-maintenance](../../.agents/skills/skill-maintenance/SKILL.md) | Maintain this harness without changing its role | `Use $skill-maintenance to adapt this skill for the current client.` |
| [pr-repair](../../.agents/skills/pr-repair/SKILL.md) | Coordinate existing-PR review, authorized implementation and repairs | `Use $pr-repair to review PR <URL> and implement scoped corrections.` |
| [multi-pr-review](../../.agents/skills/multi-pr-review/SKILL.md) | Review several PRs in separate worktrees with evidence for each | `Use $multi-pr-review to review PRs <URL> and <URL> independently.` |
| [implementation-completeness](../../.agents/skills/implementation-completeness/SKILL.md) | Compare promised behavior with implementation and assertions in every substantive review | `Use $implementation-completeness to compare PR <URL> with its acceptance criteria.` |
| [bug-reproduction](../../.agents/skills/bug-reproduction/SKILL.md) | Reproduce a suspected defect with isolated state and targeted failure injection | `Use $bug-reproduction to verify this suspected startup failure in PR <URL>.` |
| [integration-path-validation](../../.agents/skills/integration-path-validation/SKILL.md) | Exercise changed startup/import/packaging and CI dependency boundaries | `Use $integration-path-validation to check startup and the clean CI environment for PR <URL>.` |
| [state-recovery-validation](../../.agents/skills/state-recovery-validation/SKILL.md) | Check interrupted writes, retries, checkpoint consistency and duplicate delivery | `Use $state-recovery-validation to verify checkpoint recovery in PR <URL>.` |
| [change-impact-analysis](../../.agents/skills/change-impact-analysis/SKILL.md) | Trace changed defaults, concurrency and contracts to consumers | `Use $change-impact-analysis to assess the changed runtime defaults in PR <URL>.` |
| [delegation-triage](../../.agents/skills/delegation-triage/SKILL.md) | Check ownership and existing assignments before issuing specialist work | `Use $delegation-triage to identify documentation gaps not covered by the active workers for PR <URL>.` |
| [pr-validation](../../.agents/skills/pr-validation/SKILL.md) | Select checks and assess evidence for the combined PR revision | `Use $pr-validation to verify PR <URL> against its final head and required checks.` |
| [bonsai-ci](../../.agents/skills/bonsai-ci/SKILL.md) | Prepare and track test/documentation contributions to a parent PR | `Use $bonsai-ci to prepare regression coverage for PR <URL> in <owner/repo>.` |
| [bonsai-containers](../../.agents/skills/bonsai-containers/SKILL.md) | Inspect or perform requested worker lifecycle operations | `Use $bonsai-containers to inspect the installation bound to <owner/repo> and report its sealed revision and enabled profiles.` |
| [pr-submission](../../.agents/skills/pr-submission/SKILL.md) | Prepare/update the parent PR with validation and contribution evidence | `Use $pr-submission to update PR <URL> from its current diff and observed checks.` |
| [codex-cli-mcp](../../.agents/skills/codex-cli-mcp/SKILL.md) | Requested local Codex CLI work and existing approved GitHub MCP connections | `Use $codex-cli-mcp for <task> in <checkout>, using the already-connected GitHub tools.` |

Use connected GitHub tools directly when already available; skill invocation does
not require starting another coding client. Installation/startup and worker
approvals retain their own authorization requirements. Follow the
[root workflow](../../AGENTS.md) and the selected target's instructions.

For existing PRs, start with `pr-repair`; it loads supporting skills only when
their conditions apply. A plain "review PR" stays read-only. "Review and implement"
also requests scoped corrections under the ownership rules. Continue the existing
PR/branch and select quick, standard or deep investigation based on the diff and
risk; all modes retain required repository checks. See
[existing-PR routing](../../AGENTS.md#skill-routing-for-existing-pull-requests).

When several PRs are named, also use `multi-pr-review` to isolate their checkouts
and evidence. The review skills include four standard-library Python helpers;
see [review tools](../../tools/README.md#review-evidence-tools) for their paths and
CLI entrypoints. They do not publish reviews, repair PRs or start Bonsai workers.

## Select the worker role

Codex implements application code and opens its parent draft PR before requesting
contributions. Workers author tests, fixtures, test configuration and product
documentation. Codex leaves useful issues and finishes without waiting for worker
execution, CI or automatic reviews. Verify the selected repository's sealed
installation supports the route before executable admission; source support does
not establish deployment. Unverified/dependent handoffs may be left as guidance-only
issues without execution labels or envelopes and with an exact next dispatcher action.

| Assignment / Role | Current source role / issue label | Delivery evidence & scope |
| --- | --- | --- |
| Regression coverage | `agent:test-specialist` | Exact tests/fixtures/test configuration, protected check outcomes, embedded read-only review |
| Documentation | `agent:documentation` | Exact documentation changes and protected check outcomes; no embedded model reviewer |
| Commit / candidate review | `reviewer` (no issue label; `workers/bonsai/reviewer.py`) | Read-only review distinguishing substantive blockers from optional suggestions without expanding approved scope; embedded for `test-specialist` or automatic PR commit `COMMENT` when `automatic_pr_reviews: true` |
| Coordinator | `supervisor` (no issue label; `workers/bonsai/supervisor.py`) | Deterministic authority, scope, freeze, termination, and honest evidence; initial front-end assignment/prompting only, no backend review role |
| Admission control | `ready` / `blocked` labels | `ready` + no `blocked` + single matching `agent:*` label admits current revision (`admission_mode: ready`) |

Generalist/tests are retired source routes, not aliases. Runtime roles are
launched by the supervisor after admission, not by invoking a role name in chat
or spawning a duplicate local subagent. The developer owns application repairs.

## Request a contribution

Replace the bracketed values and give the coding client this prompt:

```text
Use $bonsai-ci to create or update a [test-specialist | documentation] handoff.
Repository: [owner/repo selected for this task]
Parent PR: [URL and number]
PR base: [exact base branch]
Required delivery branch: [exact parent PR head branch]
Implementation commit: [current SHA]
Goal and evidence: [observable behavior, source paths, reproduction/PR links]
Acceptance: [test assertions/edge cases or documentation claims/examples to verify]
Scope and dependencies: [known candidate files, boundaries and prerequisites]

Search for an existing matching issue first. Verify the target-bound sealed
installation and select agent:test-specialist for tests/fixtures/test configuration
or agent:documentation for documentation. Keep application code with the developer.
Preserve all parent-branch commits and contribute to this existing PR.

Use prose preparation when exact scope or protected checks need research. Select
the matching role label (agent:test-specialist or agent:documentation) and keep
blocked until finalized/prepared; use operator --target-pr NUMBER.
For a verified legacy schema-2/3 envelope, use numeric pull_request instead.
On current source (admission_mode: ready), admit verified issues/proposals by
removing blocked and adding ready (older releases require /approve-agent).
Do not post owner preparation or approval commands for me. If prerequisites or
branch reservations prevent dispatch, leave guidance-only issues without execution
labels or an executable envelope and state the dependency and next dispatcher action.
Return issue links, verified facts, gaps and exact next owner/operator action.
Report already-delivered SHAs, actual check outcomes and observed final-head CI
separately. Finish without waiting for preparation, admission, delivery or CI.
```

Test assertions should be independently authored; report application defects
instead of widening scope. Documentation acceptance includes verifying paths,
links, commands and supported behavior. Use the
[assignment guides](../../AGENTS.md#workspace-layout-and-supporting-guidance)
and [handoff template](handoff.md) for contribution-specific detail.

## Turn the request into executable work

1. Finalize the issue, verify prerequisites, keep `blocked`, and select exactly
   one matching role label (`agent:test-specialist` or `agent:documentation`).
   A label or PR mention alone neither authorizes work nor selects delivery.
2. For prose issues, the configured owner posts standalone `/prepare-agent` after
   the final edit. The operator follows [free-form preparation](free-form-issues.md)
   with committed evidence and `--target-pr NUMBER`. Preparation is exclusive and
   requires confirmed-stopped processes; it does not stop a listener itself.
3. Inspect the sealed role, exact scope, protected checks, limits and pinned PR
   destination (`inspect-preparation KEY`), and resolve any gaps.
4. For a complete verified legacy envelope, validate with the
   [offline validator](../../tools/README.md).
5. On current source (`admission_mode: ready`), admit the verified proposal or
   legacy envelope by removing `blocked`, adding `ready`, and retaining the
   single matching `agent:*` label (no `/approve-agent` comment is needed;
   older installed releases still require `/approve-agent <full-digest>` or
   standalone `/approve-agent`). The already authorized listener admits work;
   loading a skill does not authorize starting or upgrading it.
6. Serialize tests and documentation targeting one PR. Leave dependent work as
   guidance for a later dispatcher; do not wait for reservations or dispatch a
   second writer concurrently. That dispatcher verifies actual delivered commits
   and reprepares stale proposals after head changes. Keep failed/unrun checks,
   applicable model review and final-head CI distinct. Use `pr-submission` to report
   available evidence and pending work, then finish. Merge remains an owner decision.

## Follow automatic PR review

There is no issue implementation label or owner slash command for this reviewer.
On a compatible installation, trusted `automatic_pr_reviews: true` enables polling
of unseen commits on open PRs in its bound repository. It defaults off. Inspect
existing configuration read-only; use `bonsai-containers` for separately authorized
configuration/lifecycle changes. A contribution request does not enable reviews.

With the opt-in already enabled, report any review already available for the actual
PR commit. Do not wait for a review to appear. Fixes belong to the developer or a separately scoped
test/documentation assignment. Preserve review records, attempts and publication
markers; do not reset them to retrigger a commit. See the
[retry and evidence reference](../../.agents/skills/bonsai-ci/references/runtime-and-issue.md#automatic-commit-reviews-and-telemetry).
