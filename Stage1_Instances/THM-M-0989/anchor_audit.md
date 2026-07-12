# Anchor audit

## Scope and immutable environment

This audit concerns the exact forward, unit-row-variance triangular-array target in
`Statement.lean`. It does not audit or claim the stronger converse usually associated with the
name Lindeberg-Feller. The repository pins mathlib at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, committed 2026-03-30). The local
`Mathlib/Probability/CentralLimitTheorem.lean` and the raw file at that commit both have SHA-256
`4b42bad9589ec3772fe0e884ad70789c89fd0c11566d980f3df1c862bbc7f03d`.

## Pinned mathlib inventory

Repository-wide searches of the pinned Lean sources for `Lindeberg`, `Feller`, `triangular array`,
and `truncated second` found no theorem implementing this target. The relevant module contains an
i.i.d. sequence central limit theorem, not a triangular-array Lindeberg theorem:

| Declaration | What it supplies | Exact-target result |
|---|---|---|
| `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum` | centered unit-second-moment i.i.d. sequence, normalized by `sqrt n` | Rejected as an exact anchor: requires identical distribution and a single global sequence |
| `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub` | i.i.d. sequence with general mean/variance | Rejected as an exact anchor for the same reason |
| `ProbabilityMeasure.tendsto_iff_tendsto_charFun` | Levy/characteristic-function convergence bridge | Accepted as a future proof leaf, but it does not establish the Lindeberg estimate |
| `ProbabilityTheory.charFun_gaussianReal` | characteristic function of the Gaussian | Accepted as a future proof leaf only |

`AnchorAudit.lean` elaborates these names and prints the axioms of the two CLT declarations in the
pinned environment. The output reports `[propext, Classical.choice, Quot.sound]`. This is normal
mathlib foundation use and does not close the target.

## External Lean 4 candidates

GitHub repository discovery was performed on 2026-07-12, and each candidate below was inspected at
the listed full commit rather than a moving branch.

| Candidate | Immutable revision and environment | Audit result |
|---|---|---|
| `patrickrd/CLT-lindeberg`, `Clt/Lindeberg.lean`, declarations `lindeberg_clt` and `lindeberg_central_limit` | commit `82249ccfc05c0d97b86f33fce2582f0bf4ff9c06`, tree `7d11c8e993bdecb4b072a9369ee6858db6728c61`; Lean `v4.29.0-rc3`; mathlib `bf8875c7dc7162b23cdb881f33cc97caab1c688a`; Apache-2.0; file SHA-256 `64020a1982986ca506b3623ff7b1f9a2bad2a57edb764ef0689ddda0ab43da3c` | Strongest relevant anchor. It proves the Lindeberg CLT for prefixes of one globally independent sequence with cumulative variance tending to infinity. Its directly imported proof files contain no `sorry`, `admit`, or `axiom`, but the repository default root imports unrelated files containing `sorry`. It is not the frozen row-wise triangular-array statement and is not installed or checked in this repository. |
| Same repository, `Clt/Lindeberg_v2.lean` | same commit/toolchain; file SHA-256 `83cc6a15f8a283d4c5315692eec047ef4fb4c55856dbf4abc63149171532b471` | Alternate sequence formulation deriving variance divergence from Lindeberg plus positive variance. Still not an exact triangular-array anchor. |
| `jameshstephens/lindeberg`, `Lindeberg/Basic.lean` | commit `cdba58274dfac45e826a144026feb011d4ced16b`, tree `944b5a9a869d45795b55caf1093ce76f79c51720`; Lean `v4.30.0`; mathlib `c5ea00351c28e24afc9f0f84379aa41082b1188f` | Generalized Lindeberg replacement principle for finite random vectors, not the central limit theorem. Useful technique only; no exact closure. |
| `uw-math-ai/central_limit_theorem` | commit `0ed57e943d642eaa95fe547780024b9e3a0dfbdf`, tree `579835cb128afd900d7309ac05d647a1a2fde043` | i.i.d.-style CLT experiment; `CentralLimitTheorem/main_theorem.lean` contains `sorry`. Rejected. |
| `edegeltje/FreeCLT` | commit `04b5b747538ca59e355908e16effa9b6a8d79b96`, tree `860c0f3a2a7d8d0a2d14e7c2928a8f7e1265d48a` | Free-probability CLT, mathematically different; sampled proof modules contain `sorry`. Rejected. |

The Patrick Dallaire candidate uses a sequence `X : Nat -> Omega -> Real`, global `iIndepFun X P`,
partial sums over `Fin n`, and cumulative variance normalization. The frozen target permits every row
to be a different family and assumes independence only inside each row. Consequently, applying the
external theorem would require a new coupling/product-space construction and a checked law transport;
there is no direct wrapper from its theorem type to `Stage1Instances.THM_M_0989.Statement`.

The external repository was not cloned, fetched, added to `lake-manifest.json`, or compiled: the
worker rules prohibit changing `.lake`, and this dependency is absent from the pinned closure. Its
README's "Full working proof" is therefore discovery evidence, not repo-local kernel evidence.

## Classification and boundary

No exact mathlib or external Lean 4 closure was found. The precise root remains `M3` and carries
`formalization_debt`, not `repo_local_integration_debt`: the external sequence theorem is nonexact,
so merely pinning it would not close this target. The usable future architecture is the pinned
mathlib characteristic-function/Levy infrastructure plus either a new triangular-array Lindeberg
estimate or a substantial, explicitly checked reduction to an external sequence theorem.

This completes the bounded anchor inventory only. It supplies no proof-body credit, no H0 source
credit, no obligation-tree credit, and no theorem-completion claim. Master acceptance is still
required.

## Validation record

All commands ran from base revision `8f12ecb893ab86b5c559c53ff8e856de99bdd878`.

| Command | Exit/result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0; `ok` for 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0989` | 0; rank 269, lane `hard_mathlib_anchor_and_wrapper`, L0/rework required |
| `rg -n -i 'Lindeberg|Feller|triangular array|truncated second|TendstoInDistribution' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0; only the generic convergence API and i.i.d. CLT candidates described above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0989/AnchorAudit.lean` | 0; all four declarations resolved; both CLT declarations reported only `propext`, `Classical.choice`, `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0989/Statement.lean` | 0; frozen target still elaborates |
| GitHub REST repository/tree/raw-file queries at the full commits above | 0 except grep.app returned HTTP 429 and was not used as evidence; GitHub discovery and raw immutable files succeeded |
| `git diff --check -- Stage1_Instances/THM-M-0989` | 0 |

