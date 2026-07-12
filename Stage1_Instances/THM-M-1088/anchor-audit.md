# Lean 4 anchor audit

Item: `S56-M-1088-ANCHOR_AUDIT`  
Audit date: 2026-07-12 (Asia/Shanghai)  
Repository base revision: `e04c2cdd0b505f199d5c9e5f6841fb27d2236a73`

## Exact target fingerprint

The audited target is `Stage1Instances.THM_M_1088.BorellTISTarget` in `Statement.lean`: a
countable, nonempty, centered real Gaussian process with an explicitly measurable and integrable
pointwise supremum representative, positive variance supremum `sigma2`, and the strict upper-tail
event for every `u >= 0`. The checked expansion is
`Stage1Instances.THM_M_1088.target_iff_expandedSourceShape`. An anchor must prove this exact target
or provide checked transports covering all of those choices.

## Pinned mathlib audit

The reused Lake manifest pins mathlib at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (commit date 2026-03-30) and Lean at
`v4.29.0`. A case-insensitive source scan of the pinned mathlib `Mathlib`, `Archive`, and
`Counterexamples` trees found no Borell--TIS declaration. The apparent `Borell` hits were unrelated
Lie-theoretic `borelLower` identifiers, and the `Tsirelson` hits were the unrelated CHSH inequality.

The nearest usable APIs are:

| Module | Declaration | Audited role | Exact target? |
|---|---|---|---|
| `Probability.Distributions.Gaussian.IsGaussianProcess.Def` | `ProbabilityTheory.IsGaussianProcess` | finite-dimensional Gaussian-process predicate already used by the target | no |
| `Probability.Distributions.Gaussian.IsGaussianProcess.Basic` | `ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_eval` | coordinate Gaussian-law infrastructure | no |
| `Probability.Distributions.Gaussian.IsGaussianProcess.Independence` | `ProbabilityTheory.IsGaussianProcess.indepFun_of_covariance_eq_zero` | independence infrastructure under covariance hypotheses | no |
| `Probability.Distributions.Gaussian.Fernique` | `ProbabilityTheory.IsGaussian.exists_integrable_exp_sq` | exponential-square integrability for Gaussian measures on complete normed spaces | no |

`AnchorAudit.lean` imports and kernel-elaborates these names; `Statement.lean` separately elaborates
the exact target because the dossier is outside the Lake source tree and is checked by file path.
Fernique's theorem concerns a Gaussian measure on a normed space and yields integrability; it does not yield the
supremum tail inequality or its sharp variance constant. No searched declaration has the target's
event, variance supremum, or process-supremum conclusion. A source scan of the relevant Gaussian
modules found no `sorry`, explicit `axiom`, or `unsafe` declaration. This is not a transitive
foundation audit and grants no proof-body credit.

## External Lean 4 candidates

External discovery used GitHub repository search and then immutable archive inspection. No external
dependency was cloned, fetched, installed, or added to `.lake`.

### LSLT

- Repository: `saulcodeman160/LSLT`
- Audited immutable commit: `7b82b1323c80f0c21ca449fd12e1c24315ae9782`
- Toolchain: `leanprover/lean4:v4.27.0-rc1`
- Pinned mathlib in its manifest: `d68c4dc09f5e000d3c968adae8def120a0758729`
- Module/declaration: `SLT/GaussianLipConcen.lean`,
  `GaussianLipConcen.gaussian_lipschitz_concentration_one_sided`
- Type shape: for positive finite dimension and positive Lipschitz constant, a Lipschitz real
  function under finite-dimensional standard Gaussian measure has
  `P(t <= f - integral f).toReal <= exp (-t^2/(2*L^2))`, for `t > 0`.
- Placeholder scan: no `sorry`, explicit `axiom`, or `unsafe` token in this module.
- Provenance: the declaration has a local `by` proof reducing to a CGF bound and
  `chernoff_bound_subGaussian`; its terminal transitive declaration closure was not independently
  built or audited here.
- Classification: credible related theorem, but not an exact anchor. It is finite-dimensional,
  assumes a Lipschitz function of a standard Gaussian vector, uses a non-strict event and positive
  tail parameter, and returns a `toReal` probability bound. No checked bridge from an arbitrary
  countable Gaussian-process supremum to this theorem is present. It is also toolchain and mathlib
  revision incompatible with the current pinned environment until integration is demonstrated.

### Other inspected discovery results

The immutable archives below contained related Gaussian or concentration material but no textual
match for Borell--TIS, Tsirelson--Ibragimov--Sudakov, `IsGaussianProcess`, or an exact Gaussian-process
supremum concentration declaration:

| Repository | Immutable commit | Result |
|---|---|---|
| `dududuguo/HighDimProb` | `8d4eec8bc06d80e8436ab3505000fca999b46546` | generic sub-Gaussian and concentration APIs; no exact candidate |
| `mrdouglasny/gaussian-hilbert` | `4d055b0bf3722c73bd6c327eeabd8a8a72ab4c7e` | Gaussian chaos concentration; documented upstream non-core axioms in part of its chain; no exact candidate |
| `bjoernkjoshanssen/hypothesis` | `9d03ba566ca31b72a5d01abb4d8080b7fefee362` | elementary probability/statistics and many `sorry` placeholders; no candidate |

GitHub repository searches for `"Borell-TIS" Lean`, `Borell inequality Lean`,
`Gaussian process Lean4`, and `Borell TIS theorem prover` returned zero repositories. Repository
search is not a completeness proof over all private, unindexed, or non-GitHub formalizations; the
claim is limited to the recorded services and immutable public revisions inspected.

## Classification and disposition

No exact repo-local, pinned-mathlib, or inspected external Lean 4 closure was found. Consequently
there is no external anchor to pin/import and no `repo_local_integration_debt` created by this audit.
The root remains `M3` formalization debt: the exact statement elaborates, while its proof is absent.
The human-source status remains `H2`, since this phase did not inspect primary mathematical editions
or promote the discovery citations. Readability remains `R4`. No `M0`, `H0`, audit completion, or
theorem completion is claimed.

The next proof architecture should treat the finite-dimensional Gaussian Lipschitz concentration
route as a related decomposition candidate only. It must separately discharge the finite-index
supremum Lipschitz representation, covariance/variance normalization, countable approximation,
measurability and integrability, limit passage, strict-event transport, and the `u = 0` boundary.

## Validation receipt

All commands ran in the worker clone. Network use was discovery-only; `.lake` was not mutated.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard valid; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1088` | 0 | rank 530, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Borell\\|Tsirelson\\|Ibragimov\\|Sudakov\\|Gaussian.*(concentr\\|isoper)\\|concentr.*Gaussian' Formalizations/Lean/.lake/packages/mathlib/{Mathlib,Archive,Counterexamples}` | 0 | only unrelated Borel/CHSH hits and Gaussian infrastructure; no Borell--TIS candidate |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1088/Statement.lean` | 0 | exact target and checked expansion elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1088/AnchorAudit.lean` | 0 | four related pinned declarations elaborated |
| immutable GitHub repository queries plus `codeload.github.com/<owner>/<repo>/tar.gz/<commit>` archive scans | 0 | revisions and dispositions recorded above; no dependency installation |
| `rg -n 'sorry\\|axiom\\|unsafe'` on pinned Gaussian process/Fernique modules and the LSLT candidate module | 1 | expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1088 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This node is self-tested evidence pending the rev-5.6 master's node-specific acceptance receipt.
