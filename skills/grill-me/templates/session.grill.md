# Grill Session: <topic>

> Template only. Create or update a real file only where recording is allowed.
> A preference is not permission; interview closure is not task completion.
> In planning-only interviews, needs and explanations are the main content.
> Omit action-authorization questions; optional execution records below are
> relevant only to a separately requested execution task, not prompts to ask permission.

- mode: <profile | decision | knowledge>
- intensity: <light | standard | heavy>
- round: 0
- updated_at: <actual date>
- interview_status: in-progress
- execution_status: not-started

These initial values apply only to a fresh session. Preserve a legacy `done`
label as history; without action evidence set `execution_status: unknown`,
not `not-started` or `done`. Resume only when explicitly requested, and
recompute open questions before asking another round.

## Needs and constraints

- Clarified needs: <known goals, scenarios and constraints>
- Still vague: <hypotheses to explore; a complete plan is not required initially>

## Understanding gaps

- Q<id>: needs-explanation | <question and terms to explain next round>
- Preserve other answered questions; requesting help is not choosing a business option.
- Explain the queued question first, then re-ask it plainly with the help option retained.
- Never infer a durable personal trait from confusion.

## Decisions

| id | status | choice | reason / user evidence |
|---|---|---|---|
| D1 | tentative | <choice or deferred> | <not yet confirmed> |

## Authorization

| action | target / scope | authorization | evidence | native_gate |
|---|---|---|---|---|
| <specific action> | <exact target> | unknown | <none or exact user instruction> | <not-requested / pending / approved / denied / not-required> |

Record each action separately. A blank or skipped field grants nothing and
revokes nothing already authorized. Re-check the latest scope before action;
the table is a record, not a substitute for the host's actual approval state.

## Open threads / parking lot

- <missing decision, prerequisite, owner, reason for deferral>

## Memory writes

- <none | draft | pending | applied with verification; only under existing memory rules>

## Closure / execution evidence

- Interview conclusion: <not confirmed / confirmed by user>
- Remaining approvals: <specific missing grants, if any>
- Proposed next action: <does not itself grant execution permission>
- Actual actions / verification: <none until actually performed and checked>
