# Exact-statement gate: blocked

Item: `S56-M-1046-STATEMENT`

## Decision

The exact Lean 4 target cannot be truthfully elaborated in the pinned dependency closure. The
intake fixes the classical finite-horizon claim for a real continuous local martingale `M`: if
`E[exp((1/2) <M>_T)]` is finite, its Doleans-Dade stochastic exponential is a martingale through
`T`. An exact encoding therefore needs definitions with their mathematical laws for all of:

- continuous local martingales and a localizing sequence tending to the horizon;
- the quadratic variation `<M>` and its relationship to `M`;
- the Doleans-Dade stochastic exponential of `M`;
- restriction of the martingale conclusion to the interval through `T`.

The pinned mathlib revision has no declarations for stochastic integration, semimartingales,
local martingales, quadratic variation, or stochastic exponentials. Introducing uninterpreted
predicates for those notions would not encode their mathematical meaning. Supplying the desired
martingale conclusion as a field of input data would assume the result. Either approach would
substitute a different proposition for Novikov's condition and is forbidden by the rev-5.6
statement-identity gate.

The legacy module `AwesomeTheorems.Stage1.S1_M_239` was inspected only as discovery input. Its
`StatementShape` quantifies over a `NovikovData` package whose `quadraticVariation` is merely a
predictable, path-continuous, monotone, nonnegative process starting at zero; it is not identified
as the quadratic variation of `process`. Its localizing sequence is not required to approach the
horizon, and its conclusion is a martingale on all `NNReal` times rather than only through the
finite terminal time. Thus that elaborated boundary is strictly not the intake-selected exact
claim and receives no statement credit.

## Lean boundary checked

`StatementProbe.lean` uses only:

```lean
import Mathlib.Probability.Martingale.Basic
import Mathlib.Probability.Process.Predictable
```

It elaborates `Filtration`, `Martingale`, `IsStoppingTime`, `stoppedProcess`, and `IsPredictable`.
This establishes the closest general process substrate available locally, not a canonical Novikov
target. A case-insensitive declaration/source search over pinned mathlib for `local martingale`,
`quadratic variation`, `stochastic integral`, `semimartingale`, `Doleans`, and `stochastic
exponential` returned no matches.

Environment: Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; base repository revision
`aa17132a199e15900d59ea24726151468fdac915`. The existing canonical `.lake` artifact was reused and
was not modified or refreshed.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1046/StatementProbe.lean` | 0 | all five available substrate declarations elaborated |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `rg -n -i 'local martingale\|quadratic variation\|stochastic integral\|semimartingale\|doleans\|stochastic exponential' .lake/packages/mathlib/Mathlib .lake/packages/mathlib/Mathlib.lean` | 1 | no matching pinned mathlib declaration or source text (`rg` exit 1 means no matches) |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1046` | 0 | rank 239, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1046` | 0 | no whitespace errors |

## Gate result and retry condition

First failed gate: section 5.1 exact statement identity. The canonical formal declaration,
expression fingerprint, checked alternate transports, and meaningful mutation tests cannot be
produced until a pinned Lean dependency supplies the missing stochastic-calculus definitions, or
those definitions and their laws are formalized locally in an earlier accepted task. The machine
status remains `M4`, and the theorem is not complete.

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase did not pass its
completion gate. Retry after the required stochastic-calculus substrate exists at an immutable
revision; do not retry by treating the legacy candidate package as the exact theorem.
