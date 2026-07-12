# Statement validation record

Item: `S56-M-1067-STATEMENT`  
Base revision: `4344dc4263d0bcc8c386ec0ae1ad4e508c910b1e`

## Frozen target

`Stage1Instances.THM_M_1067.BrownianLocalTimeTarget` quantifies over standard Wiener measures on
continuous real paths indexed by nonnegative time and starting at zero. `IsWienerMeasure` uses all
finite linear combinations of evaluations, with centered Gaussian law and covariance `min(s,t)`;
it does not assume local time.

The witness is a nonnegative field `L(w,t,x)`. Outside one `W`-null set, `(t,x) |-> L(w,t,x)` is
jointly continuous and the occupation-density identity holds simultaneously for every
`t : R>=0` and every measurable `f : R -> R>=0 infinity`. Both sides are Lebesgue integrals; the
time measure is explicitly transported to `R>=0`. This fixes the occupation-density normalization
and avoids a hidden Tanaka factor of two.

The direct imports are:

- `Mathlib.MeasureTheory.Integral.Lebesgue.Basic`
- `Mathlib.Probability.Distributions.Gaussian.Real`

`target_iff_expandedSourceShape` kernel-checks a complete direct expansion. Three separately
elaborated mutations expose prohibited fixed-level, fixed-test-function, and circular assumed-local-
time substitutions.

## Commands and results

Commands ran in the existing pinned environment; no Lake dependency state was changed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1067/Statement.lean` | 0 | exact target, direct expansion, equivalence, and three mutations elaborated; explicit target printed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1067/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `00c33b...7480`, `651c8a...b1d2`, `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | rank 509; L0/rework-required; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1067 .stage1-worker-selftest.json` | 0 | no output |

## Status boundary

This is self-tested statement evidence pending master acceptance. It proves only the definitional
equivalence of the named target and its expansion, not existence of Brownian local time. Exact
primary-source pinpointing and upstream candidate review remain open for anchor audit. No `H0`,
`M0`, `R0`, audit completion, or theorem completion is claimed.
