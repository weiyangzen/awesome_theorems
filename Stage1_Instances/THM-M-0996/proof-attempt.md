# THM-M-0996 proof-phase evidence

Item: `S56-M-0996-PROOF`  
Base revision: `738b0a6cf435510ea01ed9bc25c8a4d5a3eabc3a`  
Result: blocked; no self-test receipt is emitted for the assigned proof phase.

## Implemented proof body

`Proof.lean` kernel-checks the frozen zero-dimensional branch. If
`Module.finrank Real E = 0`, then `E` is subsingleton. Every continuous linear
functional `E ->L[Real] Real` is therefore zero, so its norm cannot equal one.
Consequently `IsUnitHalfspace H` is impossible and the exact enlargement
comparison follows by elimination. Both declarations are real proof bodies;
neither uses `sorry`, an axiom declaration, or an unresolved premise.

This closes only the dimension-zero subcase of `M0996-B-DIM`. It does not
close `M0996-B-DIM` itself because the positive-dimensional branch remains.

## Validation record

Commands were run from the worker clone. The Lean command used the existing
canonical pinned `.lake` symlink and did not update or mutate dependencies.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0996` | exit 0; rank 276, L0/rework_required, planned, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0996/Proof.lean)` | exit 0; both declarations elaborated; `#print axioms` reported exactly `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` |
| `rg -n '\\b(sorry|admit|axiom)\\b|sorryAx' Stage1_Instances/THM-M-0996/Proof.lean` | exit 1 with no output, the expected clean negative scan |
| `git diff --check -- Stage1_Instances/THM-M-0996` | exit 0; no output |

## First failed gate

The frozen proof route requires both `M0996-L-HALFSPACE` and
`M0996-L-GENERAL`. The pinned mathlib audit found no Gaussian isoperimetric
root theorem, and the current mathlib API does not supply the
Ornstein-Uhlenbeck construction, Gaussian semigroup gradient estimate,
interpolation theorem, and measurable-set limiting proof required for
`M0996-L-GENERAL`. No exact external Lean 4 proof body was found or pinned.

The retry condition is a kernel-checked implementation of those positive-
dimensional analytic obligations, or an immutable compatible Lean 4 upstream
containing an exact proof body that can be pinned, imported, and audited.

## Status boundary

The assigned phase is not genuinely complete. The canonical root remains M3,
theorem completion is false, and no `.stage1-worker-selftest.json` is written.
The remaining machine root cut set is `M0996-L-HALFSPACE` and
`M0996-L-GENERAL`; source, readability, trust, hermetic replay, and independent
acceptance gates also remain open.

## Current worker supersession

The historical record above is preserved byte-for-byte. At base revision
`718e166c56e53c552ebb861ee01427f9a606fc72`, the current worker added further
placeholder-free proof bodies and an isolated module-chain replay. The new
work is recorded separately in `proof-validation.md`, `proof-receipt.json`,
and `proof-blocker.json`.

This supersession changes only the scope of self-tested partial progress. It
does not retroactively alter the original result, close any frozen obligation,
or prove the canonical root. The remaining root cut is still
`M0996-L-HALFSPACE` and `M0996-L-GENERAL`, and theorem completion remains
false.
