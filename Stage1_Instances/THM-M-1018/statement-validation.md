# Statement validation record

Item: `S56-M-1018-STATEMENT`  
Base revision: `f552b1fbe91904b0d46dad9e5e29e9075fc93c1e`

## Frozen target

`Statement.lean` elaborates the intake-selected interval-mass form of Levy inversion. The root
quantifies a Borel probability measure on `Real` and ordered atom-free endpoints `a < b`; it states
convergence, along the real `atTop` filter, of symmetric Lebesgue integrals over `[-T,T]` to
`mu (Set.Ioc a b)`. The equality lives in `Complex`, with the measure value converted through
`ENNReal.toReal`.

Mathlib defines `charFun mu t` with the positive exponential `exp (inner x t * I)`. Accordingly,
the interval kernel uses negative exponentials. Its value at zero is fixed to `b - a`, the removable
limit. The normalization is `1 / (2 * Real.pi)`.

The only direct import is
`Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic`. It supplies the characteristic
function and, through its transitive pinned imports, the measure restriction, Bochner integral,
filters, complex exponential, and real Borel instances used by the expression. Removing the
previously tested explicit Bochner-set import did not change successful elaboration.

`target_iff_expanded` checks the canonical definition against an independently written
binder-explicit expression. Three separately elaborated mutations record material scope changes:
removing endpoint atom hypotheses, reversing the characteristic-function frequency, and replacing
the half-open target interval by a closed one. They are probes, not alternate theorem claims.

## Environment fingerprint

| Component | Value |
|---|---|
| Lean | `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| Lake | `5.0.0-src+98dc76e` |
| `lean-toolchain` SHA-256 | `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |
| `lake-manifest.json` SHA-256 | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| Validation cwd | `Formalizations/Lean` |
| Network | not used |

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard valid; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | rank 494, planned, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-1018/Statement.lean` (from `Formalizations/Lean`) | 0 | all definitions, checked transport, mutations, and printed exact root elaborated |
| `lake env lean --version` (same cwd) | 0 | pinned Lean version reported above |
| `lake --version` (same cwd) | 0 | pinned Lake version reported above |
| `git diff --check -- Stage1_Instances/THM-M-1018` | 0 | no whitespace errors |

The first exploratory Lean run failed because this pinned mathlib exposes `integral` with the
measure argument first. Reordering the arguments fixed the type error; the recorded validation run
above is the succeeding rerun. No dependency update, fetch, build, or `.lake` mutation was used.

## Boundary

This receipt establishes exact Lean elaboration only. It does not prove or anchor the target, does
not upgrade the open human-source gate, and does not claim theorem completion. Primary-source
pinpointing and the distribution-function/law transports remain future phase obligations.
