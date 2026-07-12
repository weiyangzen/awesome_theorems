# Exact-statement gate: blocked

Item: `S56-M-0585-STATEMENT`  
Base revision: `e562dd8e1c84c4ba651e8fc451dabc0401e3af8f`

## Decision

The exact Lean 4 target cannot be truthfully frozen from the accepted intake. The complete source
wording available in the repository is "Seiberg-Witten theory" / "new invariants of
four-manifolds." This names a theory and does not identify a single proposition. The intake
therefore deliberately leaves the exact source result, hypotheses, chamber conventions, and
codomain open and assigns machine status `M4`.

Choosing a proposition now would invent missing mathematics. Plausible choices include existence
and compactness of a monopole moduli space, definition of a zero-dimensional signed count,
metric/perturbation independence when `b2+ > 1`, a chamber-change formula when `b2+ = 1`,
diffeomorphism invariance, a nonvanishing result, or a vanishing result. They differ in manifold
and Spin-c hypotheses, homology orientations, expected dimension, reducible solutions,
perturbations, chambers, codomains, quantifier order, and conclusions. None may be substituted for
the repository label without a pinpoint source decision and crosswalk.

The discovery source recorded at intake, Edward Witten, *Monopoles and four-manifolds*,
Mathematical Research Letters 1 (1994), 769-796, DOI `10.4310/MRL.1994.v1.n6.a13`, has not been
accepted at the granularity of one exact result, definitions, assumptions, conventions, errata,
and independent source review. The historical attribution to Nathan Seiberg and Edward Witten does
not itself select a rigorous invariant theorem.

Consequently no ordered binders, canonical expression, expression fingerprint, checked alternate
encoding, or meaningful removed-hypothesis/domain/scope/boundary mutation can be recorded. No
statement credit, proof credit, audit completion, or theorem completion is claimed.

## Pinned Lean boundary

`StatementProbe.lean` imports only
`Mathlib.LinearAlgebra.CliffordAlgebra.SpinGroup` and checks mathlib's algebraic `lipschitzGroup`,
`pinGroup`, `spinGroup`, and `spinGroup.toUnits` declarations. This is the closest name-specific
substrate found by a narrow pinned-mathlib search. It is a Clifford-algebra spin group, not a
Spin-c structure on a smooth four-manifold. Narrow searches found no pinned declarations for a
Spin-c structure, gauge connection, gauge group, Dirac operator, Seiberg-Witten monopole equation,
monopole moduli space, or Seiberg-Witten invariant. The repository's only other match,
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_252.lean`, explicitly records a proposition-valued
missing package and states that it is not theorem evidence.

The probe uses Lean `4.29.0` and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` through the existing canonical `.lake` artifacts. No
dependency update, build, clone, or fetch was performed.

## Validation evidence

Commands were run from the worker clone on 2026-07-12.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0585` | exit 0; rank 626, planned, L0/rework_required, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0585/StatementProbe.lean)` | exit 0; printed the elaborated types of `lipschitzGroup`, `pinGroup`, `spinGroup`, and `spinGroup.toUnits` |

## Required unblock

An accountable source reviewer must select and transcribe one pinpoint primary theorem and freeze
all domain, Spin-c, analytic, dimension, compactness, orientation, reducible, `b2+`, chamber,
codomain, and invariance conventions. Only then can a statement worker encode the same proposition,
minimize its imports, and run the required mutations.

Because the assigned statement phase is blocked rather than self-tested complete, no
`.stage1-worker-selftest.json` is emitted.
