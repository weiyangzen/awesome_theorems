# Exact-statement gate: blocked

Item: `S56-M-1195-STATEMENT`  
Base revision: `ebd311cf50e67029e9794aa8f09ab3cee28a745f`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the repository source
record. Its complete mathematical wording is `Ricci流的熵泛函` ("the entropy functional for Ricci
flow"), under the title "Perelman entropy". The record gives no formula, result number, hypotheses,
or conclusion. Perelman's 2002 paper is an identified source family, but the accepted intake does
not select a result within it.

In particular, the wording does not decide among Perelman's F-functional, W-functional, lambda
invariant, or mu invariant; nor does it decide whether the target is a definition, first-variation
identity, monotonicity formula, or rigidity/equality statement. Those alternatives have different
binders and conclusions. Even after selecting one, the source record leaves open the manifold and
time-interval assumptions, metric-flow convention, auxiliary function or density, normalization,
scalar-curvature and Laplacian conventions, evolution equation, endpoint behavior, and equality
case. Choosing these data merely to obtain an elaborating proposition would substitute invented
mathematics for the screened target.

Consequently the phase fails at the canonical human-claim identity gate, before an exact Lean
expression, minimal exact-target imports, expression fingerprint, checked transports, or meaningful
removed-hypothesis/domain/binder-scope/boundary mutations can exist. The root remains `[H4, M4,
R4]`; no statement, proof, audit-completion, or theorem-completion credit is claimed.

## Lean boundary

`StatementSubstrateProbe.lean` elaborates with the single import
`Mathlib.Geometry.Manifold.Riemannian.Basic` and checks `Bundle.RiemannianBundle`,
`Bundle.ContMDiffRiemannianMetric`, and `IsRiemannianManifold`. This is only adjacent infrastructure. The
pinned mathlib source search finds no Perelman entropy or Ricci-flow functional declaration, and
the Riemannian API does not supply the evolving metric, curvature contractions, entropy functional,
or analytic variation formula required by any plausible target. The probe therefore receives no
canonical-statement credit, and its import is not asserted to be minimal for an unidentified target.

## Required unblock

An accountable source reviewer must select an immutable primary-source result by edition and exact
section/formula/page, transcribe it, and crosswalk every definition, binder, assumption, convention,
normalization, conclusion, equality case, and degenerate/boundary case. A later statement worker can
then encode that exact result, minimize its imports, serialize its elaborated expression and
environment fingerprint, check any alternate transports, and perform all four required mutation
classes.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. Lean reused the existing pinned `.lake`
link; no update, build, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1195` | 0 | rank 389, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1195/StatementSubstrateProbe.lean` | 0 | the three adjacent Riemannian-manifold declarations elaborated; no exact Perelman target was checked |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` respectively |
| target-local and pinned-mathlib `rg` searches for `Perelman`, `Ricci flow`, and entropy-functional variants | 0 | no target-specific artifact and no pinned mathlib entropy/Ricci-flow functional; the sole mathlib text hit is the unrelated Poincare-conjecture module |

First failed gate: exact source-statement identity. The assigned phase is blocked rather than
self-tested, so no `.stage1-worker-selftest.json` is emitted.
