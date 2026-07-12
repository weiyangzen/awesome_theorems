# Anchor audit

## Scope and verdict

At the `2026-07-12T12:01:29Z` cutoff, the bounded rev-5.6 search found no Lean 4
declaration proving the exact complex Lebesgue-space target
`Stage1Instances.THM_M_0353.HermiteCompletenessTarget`. The exact proposition and
normalization interfaces elaborate, while only adjacent formal results were located, so the
machine classification is `M3`. This phase inventory is self-tested pending master acceptance;
`audit_complete=false` and `theorem_complete=false` remain unchanged.

Search aliases included Hermite functions, Hermite polynomials, Gaussian Hilbert space, Wiener
chaos, orthogonality, completeness, dense span, `HilbertBasis`, and the probabilists'/physicists'
normalization relation. Searches followed repo-local, pinned mathlib, public Lean repositories,
and Formal Conjectures order.

## Pinned mathlib

Mathlib is immutable at commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The two Hermite source files have SHA-256
`c5cf084030004a05182a1d7ffd6b8580515bd05c8f08da05c29f713e49099124` (`Basic.lean`)
and `9f3c7a4651990a1b4d524919fc45b25ad144bacd766b2b50052af6fcd5fc896f`
(`Gaussian.lean`). A complete name/content search of the pinned `Mathlib` tree found Hermite
polynomial declarations only.

| Candidate | Checked scope | Decision |
|---|---|---|
| `Polynomial.hermite_monic` | Fixes the monic probabilists' polynomial convention. | Normalization anchor only. |
| `Polynomial.deriv_gaussian_eq_hermite_mul_gaussian` | Identifies Hermite polynomials as Gaussian derivative factors. | Analytic infrastructure only; no integrability, inner product, density, or basis conclusion. |

`AnchorAudit.lean` checks both through typed wrappers. Lean reports the standard mathlib profile
`[propext, Classical.choice, Quot.sound]` for each wrapper. Neither wrapper mentions or proves the
frozen `Lp Complex 2 volume` conclusion.

## External candidates

| Project and immutable revision | Candidate | Exact comparison and decision |
|---|---|---|
| `mrdouglasny/gaussian-hilbert@4d055b0bf3722c73bd6c327eeabd8a8a72ab4c7e` (tree `8baca4420e31d91520078aad484fa25d087cde05`) | `GaussianHilbert.hermiteMulti_orthogonality`, `GaussianHilbert.hermiteMulti_dense` in `GaussianHilbert/HermitePolynomials.lean` | Credible Lean 4 partial infrastructure for real multivariate polynomials in Gaussian-weighted `L2`. It does not state the complex, unweighted Lebesgue Hermite-function `HilbertBasis`; a measure-changing isometry, normalization transport, complexification, `MemLp`, and basis packaging are absent. The project uses Lean 4.30.0 and unpinned repo dependencies, while this target uses Lean 4.29.0. Reject as terminal proof and do not create `M1` integration debt. Inspected file SHA-256: `4ed2be959da3c6afb9c781ec45ce89caeb1a47b51097967b9e8f1e55e86f7d38`. |
| `lukemantle/hermite@1bbb79a1cc1909d37170fd9ea0559a81006fc855` (tree `917daf6790763565794e6bb955ccad24b28b2959`) | `src/orthogonal.lean` | Lean 3.50.3 scratch file; theorem attempts contain `sorry` and no completeness declaration. Reject. File SHA-256: `d5561b02cca9e8fae63b8c5d01ecc66a51e7d40faef1294ca3a6bfeb76a71b79`. |
| `google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` (tree `40d17fde4b874af651386e646081f453377ea020`) | complete recursive path inventory | No Hermite path or relevant analysis basis statement; the two path matches for `Basis` are additive combinatorics. Tree-response SHA-256: `76fa3f96fc2ff7fc85addfd1e85852dae3fcb5022fc1ef35b030a3dc1e3efc61`. |

GitHub repository search also returned `GaussianWhoWhere` (an unrelated analytic uniqueness
project) and `lean-normal-forms` (Hermite matrix normal form), both rejected by domain and source
inventory. GitLab project search returned zero projects. GitHub code search returned HTTP 401 and
grep.app returned HTTP 429; these access failures bound the negative result and are not treated as
proof of global absence. No dependency was cloned, fetched, updated, or added to `.lake`.

## Validation ledger

All local checks used repository base `7780ee2963f599a6bf06f39a12c6fddb7eafc914` and the existing
pinned Lake artifacts.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0353/AnchorAudit.lean` | 0 | Both wrappers elaborated; axiom reports were `[]` and `[propext]`. |
| `python3 Stage1_Instances/THM-M-0353/check_anchor_audit.py` | 0 | Structured invariants, candidate count, hashes, and no-placeholder conditions passed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0353` | 0 | Rank 846, planned, theorem incomplete. |
| `python3 -m json.tool Stage1_Instances/THM-M-0353/anchor-audit.json` | 0 | Structured audit parsed. |
| placeholder/declared-axiom scan over target Lean files | 1, expected | No `sorry`, `admit`, or declared `axiom` found. |
| `git diff --check -- Stage1_Instances/THM-M-0353` | 0 | No whitespace errors. |

The next phase should represent the external Gaussian-density route as optional construction
research, not proof credit, and freeze local obligations for integrability, orthonormality,
density/complexification, and `HilbertBasis` assembly. Human-source status remains `H1`, readability
remains `R4`, and no exact external closure exists to justify `M1` or any `M0` state.
