---
name: bonsai-planner
description: Plan substantial multi-folder or dependent changes and turn valuable but vague issues or PRs into bounded steps and acceptance criteria before implementation.
---

# Planner

Use the [root workflow](../../../AGENTS.md) and [harness contract](../../../docs/agent-setup/agent-harness.md). This is advisory guidance for the base agent, not an enabled issue route.

Plan when the change spans meaningful components/folders, changes a contract/schema/deployment behavior, requires dependent steps, or has owner priority/concrete user evidence but insufficient acceptance criteria. Incidental generated/test folders alone need not force planning for a trivial patch.

Read the pinned source/PR, relevant consumers, applicable instructions and existing checks. State the problem, success conditions and unknowns; compare options only where there is a real choice. Use [researcher](../bonsai-researcher/SKILL.md) when external facts affect the choice. A local code question needs repository inspection rather than web research.

Return a reviewable proposal:
- Repository, source/PR head and issue revision; problem and evidence of value.
- Recommended approach, assumptions and specific unanswered product questions.
- Ordered steps with proposed exact paths/components, dependencies and role ownership.
- Observable acceptance criteria, existing verification commands and their evidence.
- Material risks, compatibility/recovery needs and scope requiring owner decision.

If product intent is missing, return `needs_clarification` with bounded choices. Do not invent requirements or call a design executable. The base developer can continue within existing authorization once the plan resolves routine choices; new scope requires owner authorization.

Planning-only requests stop with the proposal. Implementation requests can proceed after checking dependencies and scope. Runtime plan execution requires supervisor validation and installed admission; a planning artifact is not a schema-3 executable task, owner slash command or permission to start a worker.
