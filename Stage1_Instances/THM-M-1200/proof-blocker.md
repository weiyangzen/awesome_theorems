# THM-M-1200 proof-phase blocker

Item: `S56-M-1200-PROOF`. Base revision:
`c370639c4481be6bdcec40b9aa3553046d6f7572`. Date: 2026-07-12.

## Blocker

The frozen statement requires `ContDiff Real top phi`. In the pinned mathlib
revision, the differentiability order is `WithTop ENat`: `top` elaborates to
`omega`, while a `ContDiffBump` supplies order `infinity` (`∞ : ENat`). Thus the
obligation tree's proposed nonzero smooth compactly supported bump does not
inhabit the frozen test-function class. This is a statement/architecture
mismatch, not a missing tactic.

Moreover, the stronger `omega` order is the analytic endpoint. A nonzero
compactly supported real-analytic test function cannot be obtained by replacing
the bump construction: real-analytic unique continuation forces such a
function to vanish. Consequently the requested nonzero-trace package cannot be
truthfully implemented against the current frozen statement. The statement
must be returned to the statement phase and use the smooth order `∞` rather
than `top`; changing that statement in this proof-phase worker would violate
the no-substitution rule.

## Commands and exact results

All Lean commands used the existing pinned toolchain and reused the canonical
`.lake` artifacts. No update, build, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | rank 394, planned, L0/rework-required, theorem incomplete |
| pinned Lean module-path recipe elaborating `Statement.lean` and `ObligationTree.lean` | 0 | frozen target and conditional child-to-root composition elaborate; composition axioms are `[propext, Classical.choice, Quot.sound]` |
| pinned Lean elaboration of the attempted bump implementation | 1 | exact mismatch: `ContDiffBump.contDiff spacetimeBump` has type `ContDiff Real infinity spacetimeBump` but expected `ContDiff Real omega spacetimeBump` |
| `git diff --check -- Stage1_Instances/THM-M-1200` | 0 | no whitespace errors |

Temporary `.olean`/`.ilean` artifacts produced only to resolve the local module
path were removed after the check.

## Status boundary

The proof phase is blocked and is not self-tested. No proof body, root closure,
M0 claim, theorem completion, or worker self-test receipt is supplied. The
first failed gate is exact proof implementation for `M1200-C-TEST`; the
remaining root cut set is `M1200-C-TEST`.
