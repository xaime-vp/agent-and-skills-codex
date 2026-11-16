# Prompting the base agent and Bonsai roles

Follow the [root workflow](../../AGENTS.md). Pick the requested outcome first; load the relevant skill when it helps. A skill invocation is not runtime admission.

## GitHub administration

```text
Use $github-admin to triage [issue/PR URL] in [owner/repo].
Inspect the actual request/diff, existing assignments, current head and checks.
Route small code work directly; request planning for broad or valuable vague work.
Request sourced research if external facts affect the feature decision.
Apply appropriate existing change-type labels under this task's authorization;
propose missing labels with name, description, color and reason.
When pre-CI work is reviewable and no owner hold remains, mark the draft ready
and apply ready-to-merge if the merged workflows use that CI gate.
Report complex conflicts and required decisions. Distinguish CI requested,
waiting, incomplete, ready for review and complete. Do not merge automatically.
```

For a status-only request, replace metadata actions with proposed actions and keep the assessment read-only.

## Planning

```text
Use $bonsai-planner for [request or issue/PR].
Repository/source revision: [owner/repo and SHA]
Problem and evidence of value: [known requirement, owner priority or user evidence]
Constraints: [existing contract, boundaries and dependencies]
Return proposed steps/paths/owners, acceptance criteria, existing checks and gaps.
If the request is vague, give specific product choices/questions.
Use researcher when external evidence matters. This request is planning-only.
```

Omit the planning-only sentence when implementation is also authorized; routine resolved choices can proceed within that scope.

## Research requested by admin or planner

```text
Use $bonsai-researcher to investigate [feature/competitor question] for PR [URL].
Explain which claims are sourced facts, vendor claims or your inferences.
Return dated source links, relevant comparisons, tradeoffs and implications for
this repository. Keep private repository content out of public search queries.
Return the brief to the admin/planning decision without changing approved scope.
State if the required web capability is unavailable.
```

The base client may use its authorized web tools. Autonomous Bonsai research needs a sealed Pi web extension; current offline preparation does not supply it.

## Prose implementation handoff

```text
Use $bonsai-ci to prepare a prose [test-specialist | documentation] issue for
[owner/repo], contributing to parent PR [URL], branch [exact branch], head [SHA].
Goal/evidence: [observable change, source links, repro]
Acceptance and boundaries: [assertions/claims, dependencies]
Search for an existing matching assignment. Verify selected sealed installation.
Resolve exact scope/checks with preparation and operator --target-pr NUMBER.
Leave blocked/unready or guidance-only when prerequisites are missing.
Do not invent executable JSON or post owner commands. Return next action and finish.
```

Legacy task and ordered-plan templates are no longer the default entry point. For an installation that actually needs those formats, read [compatibility](compatibility.md) and the maintained schema references there. Planner output is a proposal, not an executable schema-3 envelope.
