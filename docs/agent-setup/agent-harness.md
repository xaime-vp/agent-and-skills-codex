# Agent harness, issue routing and retirement plan

These skills are usable guidance for the base coding agent. Autonomous runtime profiles are proposed in [Constant Integration #369](https://github.com/xaime-vp/constant-integration/pull/369); the CI gate is proposed in [#370](https://github.com/xaime-vp/constant-integration/pull/370). Inspect merged source/workflows and the selected sealed installation before relying on either. This harness PR does not enable new runtime issue routes.

## Responsibilities and flow

| Role | Function | Handoff |
| --- | --- | --- |
| Base developer | Own application implementation, integration and PR delivery | Reuse admin/planning/research skills; admit meaningful worker tasks only through verified contracts |
| [GitHub admin](../../.agents/skills/github-admin/SKILL.md) | Triage, route work, labels, draft readiness, simple conflicts and completion assessment | Request planner/researcher or existing implementation/review roles |
| [Planner](../../.agents/skills/bonsai-planner/SKILL.md) | Bound large or vague valuable changes before implementation | Plan with paths, steps, dependencies, checks and unresolved choices |
| [Researcher](../../.agents/skills/bonsai-researcher/SKILL.md) | Feature and competitor evidence using available web tools | Sourced brief to admin/planner; runtime requires sealed Pi web capability |
| Test specialist/documentation | Execute approved product contributions | Supervisor-owned publication into the existing PR |
| Reviewer/supervisor | Independent assessment / trusted deterministic enforcement | Preserve isolation, process stop, scope, approvals, state and Git |

Default sequence: request → admin triage → optional research/planning → scoped application change → essential test/documentation delivery → review readiness → CI admission → completion assessment. A planning/research-only request ends at its requested artifact. Continue an existing PR rather than generating another.

## What still needs an issue?

Implementation issues remain the durable work and admission record for external Bonsai workers. Keep them for approved code generation, test writing and documentation assigned to those workers. They bind repository, current issue revision, parent PR/branch, scope, checks and execution evidence. Reuse existing matching issues and serialize writers on one PR branch.

Read-only admin triage, planner proposals, research briefs and readiness assessments do not each need an implementation issue. They can run as skills inside the user's current request and attach their output to the selected PR. This reduces repeated envelopes and handoffs without bypassing runtime admission. A future admin scheduler must deduplicate by event, revision, head SHA and assignment type before dispatch.

| Signal | Current effect | Intended harness use |
| --- | --- | --- |
| Issue created/edited | No automatic implementation authorization | Admin may classify; prepare/refresh bounded scope separately |
| Exactly one supported `agent:coder`, `agent:test-specialist` or `agent:documentation` | Select implementation role on a verified installation | Only implementation issue labels |
| Issue `ready`, no `blocked`, valid proposal/envelope and prerequisites | Admit current validated revision under `admission_mode: ready` | Keep until replaced by an equally explicit admission contract |
| `feature`, `refactor`, `documentation`, etc. | Descriptive metadata | Apply existing labels; propose absent labels |
| PR draft/non-draft | Review presentation | Admin can mark a reviewable draft ready within authorization |
| PR `ready-to-merge` | CI job gate after #370 merges | Request applicable CI after pre-CI readiness, not after CI has already passed |
| `agent:github-admin`, `agent:planner`, `agent:researcher` | Unsupported in current implementation registry | Do not create executable routes from design names |
| Automatic PR Reviewer | Separate trusted installation setting | Advisory review; labels do not enable it |

Free-form preparation still requires installed owner/operator prerequisites and an explicit `--target-pr NUMBER`. A PR link supplies context only. Prose preparation's internal “research” reads a bounded committed corpus; it is distinct from the proposed web researcher.

## CI and completion without a circular gate

1. Implement approved work, integrate essential tests/docs, run appropriate existing local checks and address known blocking findings/conflicts.
2. Under authorized PR administration, mark the draft ready when it is reviewable and respect owner holds.
3. Verify the repository has the label-gate workflows; apply `ready-to-merge` to request CI. Pending CI must not prevent this admission step.
4. Inspect current checks once and report waiting/unknown/failure or complete. Do not call skipped unlabeled jobs passing CI.
5. A later head change requires a fresh assessment. The proposed gate reruns checks on commits while the label remains; newly discovered blockers require reporting and policy-driven withdrawal of this automation's admission label.

The label policy does not enforce merging, stop an already running job or invalidate an earlier check result. Branch/ruleset enforcement would be a separate task. Path filters can make a check not applicable; cite the actual policy rather than treating any missing check as success. Merge and deployment retain separate authorization.

## Legacy removal audit

Evidence below is from Constant Integration source `b155abc295b9b69d16b41735895eefa37564f4b9`, not an installed-state inventory.

| Candidate | Dependency / evidence | Disposition |
| --- | --- | --- |
| Repeated manual envelope examples in root/calling/prompting guidance | Duplicated legacy-first onboarding obscures prose preparation | Remove from default instructions in this PR; keep specialized compatibility references |
| Stale test/docs-only source registry and 1/2/3-slot claims | `runtime_profiles.py` includes coder; source supports 1..10 slots | Correct harness claims and distinguish source from installed defaults |
| Podman adapters and Pi extension | Dedicated cleanup [agent-and-skills-codex #3](https://github.com/xaime-vp/agent-and-skills-codex/pull/3) | Keep deletion in that existing PR; do not duplicate or restore its adapters |
| `tools/validate_task.py` | Calls the selected platform's real `TaskEnvelope.from_issue`; referenced by compatibility/schema guides | Retain as an optional compatibility tool, outside the default prose flow |
| `TaskEnvelope` and schema-2 parsing | `workers/bonsai/preparation_runtime.py:envelope_for` synthesizes schema 2 and calls `TaskEnvelope.from_issue` | Active internal dependency: deleting it breaks prose preparation |
| Issue intake, `ready` and supported role labels | `orchestrator/intake.py` verifies current revision, role and admission; controller consumes proof | Keep; GitHub admin is a proposed front end, not replacement authority |
| Schema-3 plan engine | `workers/bonsai/plans.py` and `specialist_plan.py` execute approved steps and preserve checkpoints | Keep; a planner produces a proposal, not an execution/recovery engine |
| Old approval grammar / legacy external envelopes | Old installations or saved tasks may still depend on their release's contract | Remove from default authoring; retire runtime support only with migration evidence |

### Runtime deletion prerequisites

A future removal PR must:
- Inventory enabled installed release/parser versions and queued, active, unknown and resumable tasks; do not erase state to make migration pass.
- Separate validated internal task objects from public issue-fence parsing, then migrate prose preparation to that internal API.
- Choose whether existing external schema-2/3 requests are converted or explicitly rejected with an actionable upgrade message.
- Preserve task identities, consumed approvals, publication reservations and checkpoint/recovery semantics across migration.
- Cover prose preparation, role routing, stale issue/head changes, pending legacy tasks, recovery and current completion reporting with offline regression checks.
- Remove the old validator/templates only after their last callers and supported installations have a replacement.

No runtime code is deleted by this harness update: the audited candidates still have consumers. The cleanup removes duplicated onboarding and stale assumptions now, while naming the concrete conditions for subsequent code deletion.
