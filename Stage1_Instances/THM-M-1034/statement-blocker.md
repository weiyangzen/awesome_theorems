# Exact-statement gate: blocked

Item: `S56-M-1034-STATEMENT`  
Theorem: `THM-M-1034`  
Base revision: `7bb9791718f936324f1ed7ca6a7909e9b257895b`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The repository source provides only
"construction of the Ito integral." The intake expands that phrase into a classical Brownian
construction, but deliberately leaves the time model, filtration conventions, predictable-process
completion, and `L2` quotient representation provisional. Its primary-source row identifies Ito's
1944 paper but explicitly records that the scan, exact equation/page mapping, assumptions, and
notation audit remain open. Choosing concrete versions of those unresolved data would select one
of several non-definitionally-equivalent construction theorems rather than elaborate an identified
source-exact claim.

In particular, the statement cannot yet freeze whether the result is a terminal random variable or
a process, whether agreement and uniqueness are in an almost-everywhere quotient or are stated on
representatives, which measure on time and sample space defines the integrand `L2` space, or which
Brownian-motion and filtration augmentation conventions apply. These choices determine the Lean
domains, binders, hypotheses, conclusion, and the meaning of the zero-time and null-representative
boundary cases. Section 5 of the rev-5.6 standard forbids silently choosing a nearby formulation.

## Pinned Lean boundary

The pinned environment uses Lean `4.29.0` and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `StatementProbe.lean` elaborates the closest independent
substrate: filtrations, predictable processes, Gaussian processes, independent increments, `Lp`,
and `MemLp`. A scoped source search found no stochastic-integral, Ito-integral, or Brownian-motion
construction declaration in the pinned mathlib tree. Thus the snapshot supplies useful components
but no canonical object model that resolves the intake's open choices.

The historical `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_227.lean` is discovery material, not
an exact target. Its model is discrete (`Nat` time and finite sums), not the intake's continuous-time
Brownian construction. More importantly, `ItoIntegralConstructionData` accepts the simple-process
isometry, convergence, candidate-limit property, approximation independence, and extension
compatibility as unconstrained `Prop` fields. `StatementShape` then assumes most of those essential
construction obligations. Reusing it would substitute a weaker circular interface for the claimed
construction.

## Validation record

Commands ran inside this worker clone. Lean used the existing pinned Lake environment; no update,
build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1034` | 0 | rank 227; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-1034/StatementProbe.lean` from `Formalizations/Lean` | 0 | all six pinned substrate types elaborated |
| `lake env lean AwesomeTheorems/Stage1/S1_M_227.lean` from `Formalizations/Lean` | 0 | historical discovery module elaborated; it proves no construction target |
| `rg -n -i 'stochastic.?integral\|ito.?integral\|brownian.?motion' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching pinned mathlib source declaration |
| `git diff --check -- Stage1_Instances/THM-M-1034` | 0 | no whitespace errors |

## Gate result and retry condition

First failed gate: exact statement identity. Without a source-exact formulation and concrete Lean
object model, there can be no honest canonical expression hash, checked alternate transport, or
meaningful removed-hypothesis/domain/binder-scope/boundary mutation suite. Machine debt remains
`M3`.

Retry after an immutable primary-source transcription and audit freeze the construction theorem's
time horizon, filtration/Brownian conventions, integrand completion, result representation,
equality mode, ordered binders, and degenerate cases. Concrete Lean definitions must then express
the construction rather than accepting convergence, isometry, or uniqueness as caller-supplied
propositions.

The assigned statement phase is not self-tested as complete, so no
`.stage1-worker-selftest.json` is emitted. This artifact claims no statement-node acceptance,
proof, audit completion, or theorem completion.
