# Workspace tools

Run these from the workspace root with Python 3.12+ (`py -3` on Windows):

```powershell
py -3 tools/check.py --component orchestrator
py -3 tools/check.py --component worker
py -3 tools/containers.py --help
py -3 tools/validate_task.py --repository xaime-vp/constant-integration --body-file path/to/issue.md
```

`check.py` and `containers.py` launch the dedicated checkout's originals with their expected imports and working directory. Keep the checkout's `tools/` intact: container packaging, platform imports and isolated E2E fixtures depend on those paths. E2E probes remain there and should be selected deliberately using the platform CI guide.

`validate_task.py` was relocated from the retired `delegate-to-deepseek` bundle. It defaults to the sibling `constant-integration/` checkout and accepts `--platform-root` to validate against another source revision. It only parses an issue offline; success proves neither installed compatibility nor approval, readiness or protected-check configuration. Set the installed timeout ceiling with `--max-timeout-seconds` when applicable.

This validator accepts legacy executable envelopes only. A free-form prose issue
is valid input to the separate [preparation workflow](../docs/agent-setup/free-form-issues.md),
which validates and privately seals a proposal; do not add JSON merely to satisfy
this tool. Optional token fields depend on the selected parser revision. A stale
checkout can reject fields omitted legitimately under a newer installation;
select compatible source with `--platform-root` and verify installation separately.

Keep private env files and worker state outside Git. A lifecycle action that starts or upgrades an installation is an operational change; loading these tools does not authorize it.

## Review evidence tools

These helpers live with the skills that own them and require Python 3.12+.
Worktree preparation and diff inventory also require Git. Run each with `--help`
from the workspace root for its arguments:

| Helper | Purpose |
| --- | --- |
| [prepare_reviews.py](../.agents/skills/multi-pr-review/scripts/prepare_reviews.py) | Create detached worktrees and separate evidence directories from pinned PR metadata; preserve the existing checkout |
| [run_probe.py](../.agents/skills/bug-reproduction/scripts/run_probe.py) | Run a reviewed harness with temporary state, an environment allowlist, a timeout and commit-bound evidence |
| [inventory.py](../.agents/skills/implementation-completeness/scripts/inventory.py) | Inventory merge-base changes, renames and heuristic file categories without inferring completeness |
| [audit_delivery.py](../.agents/skills/state-recovery-validation/scripts/audit_delivery.py) | Inspect local history-v1-style batches/checkpoints for conflicting delivery, sequence gaps and invalid checkpoint fields |

```powershell
py -3 .agents/skills/multi-pr-review/scripts/prepare_reviews.py --help
py -3 .agents/skills/bug-reproduction/scripts/run_probe.py --help
py -3 .agents/skills/implementation-completeness/scripts/inventory.py --help
py -3 .agents/skills/state-recovery-validation/scripts/audit_delivery.py --help
```

Use a fresh evidence destination outside the tracked checkout (or an ignored
directory). The probe runner is process isolation, not a security sandbox or
dependency-clean virtual environment; timeout termination covers its direct
child only. Delivery auditing does not replace the consumer's schema validator
or business-level idempotency checks. Read each owning skill for evidence and
interpretation limits. None of these tools fetches or publishes PRs, starts a
live worker, or changes installed runtime state.
