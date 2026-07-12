# Exact-statement gate: blocked

Item: `S56-M-1032-STATEMENT`  
Base revision: `232e05465bc32d3eed740568f9c81dc848219de3`

## Decision

The exact Lean 4 target cannot be truthfully frozen from the repository source record. Its complete
mathematical wording is only `随机过程的链式法则` ("the chain rule for stochastic processes"). It
does not specify a theorem variant or the hypotheses needed to distinguish one. In particular, it
does not choose:

- a continuous semimartingale, Brownian-motion, or another process domain;
- one dimension or a finite-dimensional state space;
- a time-independent `C^2` formula or a time-dependent `C^{1,2}` formula;
- the time interval and initial-time convention;
- pathwise, almost-sure, or time-by-time almost-everywhere equality;
- the stochastic-integral and quadratic-covariation conventions; or
- the filtration, adaptedness, local-integrability, and continuity assumptions.

These choices produce different propositions. The intake dossier accordingly labels its modern
finite-dimensional continuous-semimartingale formulation as provisional and leaves exact variant
selection open. Selecting that variant here would invent mathematics absent from the source record,
contrary to the rev-5.6 exact-statement gate and the skill's hard-stop rule.

The legacy module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_225.lean` was inspected only as discovery input.
Its `StatementShape` is not a source-faithful substitute. It quantifies over an `ItoFormulaData`
record containing unconstrained proposition fields such as `processSemimartingale`,
`localIntegrabilityHypotheses`, derivative-agreement and well-definedness flags, and a
`scalarProcessSemimartingaleTarget`. The corresponding hypotheses merely assume those flags, while
the conclusion requires the independently supplied target flag and formula identity. The module's
own documentation calls this a future theorem boundary and states that its stochastic-calculus
objects are abstract. Thus elaboration of that module does not establish an exact encoding of the
source claim, a checked transport, or theorem proof credit.

Consequently the first failed gate is canonical human-claim identification. No canonical Lean
declaration, elaborated-expression fingerprint, minimal-import claim, meaningful hypothesis/domain/
binder/boundary mutations, checked alternate encoding, machine-status improvement, or theorem
completion is claimed. No `.stage1-worker-selftest.json` is emitted because the assigned statement
phase is not complete.

## Required unblock

An accountable source decision must identify an immutable primary-source theorem and exact
location, then freeze the process class, dimension, regularity, time domain, equality semantics,
integral and covariation conventions, and all filtration/integrability hypotheses. A later statement
worker can encode that proposition, minimize its pinned imports, serialize the elaborated
expression, and mutation-test each frozen choice.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12. The Lean commands ran from
`Formalizations/Lean` against the existing pinned environment. No update, build, fetch, clone, or
other mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1032` | 0 | rank 225; `planned`, `L0`, `rework_required: true`, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean AwesomeTheorems/Stage1/S1_M_225.lean` | 0 | the legacy abstract boundary elaborated and printed its audit checks; this is discovery evidence only, not exact-statement evidence |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |

Known failure: the canonical human proposition is unidentified. Therefore the assigned statement
deliverable and its node-specific receipt cannot be self-tested pending the source decision above.
