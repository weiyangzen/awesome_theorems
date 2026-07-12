# Exact-statement gate: blocked

Item: `S56-M-1197-STATEMENT`  
Base revision: `61ca1390cc0fcf06937f303c775c22372db31ad7`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
complete mathematical wording is `双曲型方程的能量方法` ("the energy method for hyperbolic
equations"). This names a proof technique and a broad family of estimates, not one proposition. It
does not determine:

- a scalar equation or system, its order, or a notion of hyperbolicity;
- the spatial domain, dimension, time interval, or initial and boundary conditions;
- coefficient, forcing, data, and solution regularity assumptions;
- the solution concept and the energy functional or Sobolev order;
- conservation, equality, differential inequality, or integrated estimate as the conclusion;
- the estimate's constants and dependencies, boundary flux terms, or endpoint and degenerate cases.

These choices produce inequivalent theorems. Choosing the homogeneous wave equation energy
identity, a symmetric-hyperbolic a priori estimate, or Gronwall's inequality would substitute a
familiar theorem for the unidentified source claim. The rev-5.6 statement gate forbids that
substitution. The Stage0 entry independently marks precise definitions, hypotheses, proof,
axioms, and machine artifacts as `待补充` (to be supplied), while the label `已验证` is explicitly
untrusted metadata and is not source or kernel evidence.

The accepted intake dependency preserves exactly this ambiguity at `[H4, M4, R4]` and identifies
no primary source. Consequently the phase fails at canonical human-claim identity, before minimal
imports, fixed binders and universes, an elaborated-expression fingerprint, checked alternate
encodings, or meaningful removed-hypothesis/domain/binder/boundary mutation tests can exist.

## Pinned Lean boundary

The existing pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. A narrow repository-local search of mathlib's Lean
sources found no occurrence of `energy estimate`, `EnergyEstimate`, `energy method`, or either
ordering of `wave` and `energy`. This is only a discovery boundary, not an anchor audit and not
evidence that no relevant theorem can be expressed from lower-level APIs. No target-specific Lean
module was created because any declaration would invent the missing mathematical choices.

No `lake update`, `lake build`, dependency fetch, or mutation of the canonical `.lake` artifact was
performed. The worker clone's `Formalizations/Lean/.lake` is the scheduler-provided symlink to the
canonical pinned artifact; its appearance as untracked is therefore an environment condition, not
a target edit or release evidence.

## Required unblock

An accountable source reviewer must identify a stable primary source by edition, theorem/page, and
exact wording, then freeze the equation, hyperbolicity notion, domains, coefficients, data,
solution class, energy, all assumptions, quantitative conclusion, constant dependencies, boundary
flux policy, and endpoint/degenerate behavior. A later statement execution can then encode that
claim, minimize pinned imports, preserve and hash its elaborated expression, and run all four
required mutation classes.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1197` | exit 0; rank 391, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean version and commit recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib revision recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n 'energy estimate\|EnergyEstimate\|energy method\|wave.*energy\|energy.*wave' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 1; no matching source occurrence (the expected no-match status) |
| `rg -n 'sorry\|admit\|sorryAx\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-1197` | exit 1; no forbidden proof escape or axiom match (the expected no-match status) |
| `git diff --check -- Stage1_Instances/THM-M-1197` | exit 0; no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | exit 0; incomplete phase emitted no self-test manifest |

First failed gate: section 5 canonical source-statement identity. Known failures are exact Lean
target elaboration, minimal imports, expression fingerprint, checked transports, and structural
mutation tests. The assigned phase is not self-tested or complete, so no
`.stage1-worker-selftest.json` is emitted. No downstream-node or theorem-completion credit is
claimed.
