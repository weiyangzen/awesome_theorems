# Immutable Lean anchor audit

Item: `S56-M-1067-ANCHOR_AUDIT`  
Base revision: `572e7c7867998f8fe7bfe532eb37bc4b341b34ef`  
Audit date: 2026-07-12

## Exact target used for comparison

The comparison target is
`Stage1Instances.THM_M_1067.BrownianLocalTimeTarget` from `Statement.lean`: for every
Wiener measure on based continuous real paths, construct a nonnegative random field `L(w,t,x)`
whose point evaluations are almost-everywhere measurable and which, on one common full-measure
event, is jointly continuous in `(t,x)` and satisfies the occupation-density formula for every
nonnegative time and every measurable `ENNReal`-valued test function. A Brownian construction,
path-continuity theorem, quadratic variation, or stochastic-integral API alone is not an exact
candidate.

## Pinned mathlib audit

The repository manifest pins `leanprover-community/mathlib4` at immutable commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; the checked package checkout has that same HEAD and
the project uses `leanprover/lean4:v4.29.0`.

No exact or partial local-time declaration was found. A full Lean-source search of mathlib for
`Brownian`, `Wiener`, `local time`, `occupation density`, `occupation time`, and `Tanaka` found only
an unrelated analytic-number-theory mention of Wiener-Ikehara. There is no
`Mathlib/Probability/BrownianMotion/Basic.lean` at this revision. The nearest reusable modules are:

| Module | Relevant declarations | Audit result |
|---|---|---|
| `Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def` and `.Basic` | `ProbabilityTheory.IsGaussianProcess`, Gaussian laws of evaluations, sums, and increments | Infrastructure only; neither Wiener-process existence nor local time |
| `Mathlib.Probability.Process.Kolmogorov` | `IsKolmogorovProcess`, `IsAEKolmogorovProcess`, `mk`, `ae_eq_mk` | Continuity-modification infrastructure only |
| `Mathlib.Probability.Process.FiniteDimensionalLaws` | projective finite-dimensional-law and map-equality lemmas | Could bridge process laws, but constructs no occupation density |
| `Mathlib.MeasureTheory.Integral.Lebesgue.Basic` | `lintegral` infrastructure used by the frozen statement | Integral syntax and lemmas only |
| `Mathlib.Probability.Distributions.Gaussian.Real` | `gaussianReal` used by `IsWienerMeasure` | One-dimensional Gaussian measure only |

Thus pinned mathlib contains useful prerequisites but no declaration whose terminal proof body
closes, or nearly closes, the exact target. No mathlib anchor receives machine-proof credit.

## External Lean 4 audit

GitHub repository discovery identified one credible domain-specific Lean 4 project:
`RemyDegenne/brownian-motion`. It was inspected at immutable commit
`bdf5ea0c34f9e6d75bce5f0609a968d6e9e99e8e` (commit timestamp 2026-07-01). Its manifest pins
mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` (`v4.31.0`) and its toolchain is Lean 4.31.0,
so it is not dependency-compatible with this repository's pinned Lean 4.29.0 environment without
a separately reviewed port.

The strongest relevant declarations are in
`BrownianMotion/Gaussian/BrownianMotion.lean`:

- `IsPreBrownianReal.exists_continuous_modification` constructs a locally Holder continuous
  modification of a pre-Brownian process.
- `IsPreBrownianReal.isBrownianReal_mk` packages that modification as Brownian motion.
- `brownian`, `isBrownianReal_brownian`, and `wienerMeasure` construct a canonical Brownian process
  and Wiener measure.

`BrownianMotion/StochasticIntegral/QuadraticVariation.lean` defines `quadraticVariation` for a
locally square-integrable cadlag martingale. These are valuable prospective prerequisites, not
local-time results: a full archive scan found no occurrence of `local time`, `occupation density`,
`occupation time`, or `Tanaka`, and no declaration constructs a level-indexed jointly continuous
field or proves the occupation-density identity.

Trust and provenance also prevent proof credit. The immutable archive contains 42 source lines
matching `sorry`, including admitted declarations in stochastic-integral dependencies such as
`LocalMartingale.lean`, `DoobMeyer.lean`, `SquareIntegrable.lean`, and `OptionalSampling.lean`.
The Brownian construction is a source anchor only; its transitive terminal proof provenance was
not shown placeholder-free, it is not imported into the pinned environment, and it does not state
the exact theorem. Repository searches for other Lean-language Brownian projects found only
`banr1/tailored-brownian-motion`, a 2026 project with no demonstrated local-time declaration;
generic `local time lean4` discovery returned no credible mathematical formalization. These
negative searches are dated discovery evidence, not a claim about all future external projects.

## Candidate decision and debt

| Candidate | Exact type | Immutable revision | Toolchain feasible now | Placeholder-free terminal body | Decision |
|---|---|---|---|---|---|
| pinned mathlib | no declaration | yes | yes | not applicable | prerequisite APIs only |
| `RemyDegenne/brownian-motion` | no; Brownian/Wiener construction only | yes | no, Lean 4.31 vs 4.29 | not established; archive has 42 `sorry` lines | source anchor only |
| `banr1/tailored-brownian-motion` | no candidate identified | repository discoverable | not assessed | not assessed | reject as exact anchor |

The audit is complete for the current immutable candidate set, but theorem closure is not. The
root remains `[H2, M3, R4]`: this phase does not inspect the primary mathematical books deeply
enough for `H0`, and it finds no exact Lean proof for `M0`. The first machine blocker is absence of
any audited declaration constructing jointly continuous Brownian local time with the simultaneous
occupation-density formula. Downstream proof work must either formalize that construction from
pinned prerequisites or pin and validate a future exact external theorem, including its complete
placeholder/axiom provenance and a Lean 4.29-compatible integration.

## Commands and exact results

All local checks used existing dependency artifacts. No `lake update`, build, clone, fetch, or
other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i --glob '*.lean' 'Brownian|Wiener|local[ _-]?time|occupation[ _-]?(density|time)|Tanaka' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | one unrelated Wiener-Ikehara comment; no stochastic candidate |
| `test -e Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/BrownianMotion/Basic.lean` | 1 | Brownian module absent at the pinned revision |
| GitHub API repository/commit/tree inspection for `RemyDegenne/brownian-motion` | 0 | immutable commit and complete, non-truncated tree obtained |
| streamed GitHub tar archive scan at commit `bdf5ea0c...` with `rg` | 0 | no local-time/occupation/Tanaka match; Brownian and Wiener declarations found; 42 `sorry`-matching source lines |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1067/Statement.lean` | 0 | exact comparison target still elaborates and prints |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1067` | 0 | rank 509; L0/rework-required; planned; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1067 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is self-tested, audit-only evidence pending master acceptance. It claims completion only of
`S56-M-1067-ANCHOR_AUDIT`, not proof, validation, release, audit completion for the whole theorem,
or theorem completion. No `H0`, `M0`, `R0`, accepted receipt, or authoritative checklist state is
claimed.
