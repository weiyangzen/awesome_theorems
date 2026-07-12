# Exact-statement gate: blocked

Item: `S56-M-0999-STATEMENT`  
Base revision: `b15861ce0ba012fa04e8c728e6bacbc35a359aea`

## Decision

The exact logarithmic Sobolev target cannot yet be truthfully frozen or elaborated. The accepted
intake records only the repository phrase "an upper bound for entropy" and a provisional
Gross/Gaussian candidate. It deliberately leaves unresolved the primary-source theorem and page,
Gaussian covariance and density normalization, dimension, admissible function class, classical or
weak gradient, integrability conditions, and the convention at zero. These choices determine the
binders, hypotheses, entropy expression, energy, and sharp constant, so selecting them here would
invent missing mathematics rather than elaborate the exact assigned target.

In particular, the common finite-dimensional formula

`Ent_gamma(f^2) <= 2 * integral ||grad f||^2 d gamma`

is only a candidate recorded by intake, not an accepted source transcription. A smooth compactly
supported version, a Sobolev-space closure, a normalized `integral f^2 = 1` version, an abstract
Wiener-space theorem, and a semigroup formulation are not interchangeable exact statements without
checked transports and a source crosswalk. None may be silently chosen as the root.

The historical module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_279.lean` was inspected and
elaborated as negative boundary evidence. Its `StatementShape` quantifies over an arbitrary
measurable space, measure, abstract energy functional, and constant. It does not select a Gaussian
measure or define a gradient Dirichlet energy, and its own module documentation says that it is only
a statement shape. Consequently it is a broadened interface, not the exact Gross/Gaussian theorem,
and receives no rev-5.6 statement credit.

## Pinned-environment boundary

The legacy boundary elaborates with the existing pinned environment and these direct imports:

```lean
import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.MeasureTheory.Measure.WithDensity
import Mathlib.Probability.Moments.Variance
```

A scoped search of pinned mathlib found no terminal logarithmic Sobolev declaration or matching
entropy-gradient theorem. Mathlib does provide Gaussian-distribution and general measure/integral
substrates, but those do not resolve the source-level normalization and function-class choices. No
dependency update, build, fetch, or `.lake` mutation was performed.

## Validation record

Commands ran in this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean AwesomeTheorems/Stage1/S1_M_279.lean` | 0 | The historical abstract statement shape and its generic bridges elaborated; this is negative boundary evidence, not an exact-target elaboration |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum lean-toolchain lake-manifest.json AwesomeTheorems/Stage1/S1_M_279.lean` | 0 | SHA-256 values `651c8acc...b1d2`, `321626c8...2d81`, and `717ae769...d3a6` |
| `rg -n -i 'logarithmic[ -]sobolev\|logsobolev\|logSobolev\|entropy.*gradient\|gradient.*entropy' .lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching terminal theorem in the pinned mathlib source tree; exit 1 is ripgrep's no-match result |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard projection passed: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0999` | 0 | Rank 279, planned, `hard_mathlib_anchor_and_wrapper`, legacy artifacts unaccepted, theorem incomplete |

## Gate result and retry condition

First failed gate: rev-5.6 exact source-statement identification, inherited from the intake and
confirmed here. The canonical Lean declaration, elaborated-expression hash, minimal exact import
list, checked alternate transports, and meaningful mutation suite remain absent. Machine status
therefore remains `M4`, and no later phase or theorem-completion state advances.

Retry only after a stable primary-source copy is pinned and hashed, the exact theorem and pages are
transcribed, every assumption and normalization is crosswalked, and errata are reviewed. The
statement phase can then choose concrete Gaussian, entropy, derivative, and function-space APIs and
run kernel elaboration and mutation checks against that accepted claim.

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked rather
than self-tested complete.
