# Anchor audit

## Verdict

The node-scoped search found **no exact Lean 4 closure** of
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget`. Pinned mathlib supplies a precise
`SchauderBasis` object model, finite-rank partial-sum projections, convergence of those projections,
and their uniform boundedness in a Banach space. All of these declarations take an existing basis
as input; none constructs Enflo's space or proves that a basis cannot exist.

This leaves `formalization_debt`, not discovered `repo_local_integration_debt`. The vector remains
`[H1, M3, R4]`; neither audit completion nor theorem completion is claimed.

## Immutable candidates

| Candidate | Immutable revision | Exact declarations | Result |
|---|---|---|---|
| mathlib Schauder API | `leanprover-community/mathlib4@8a178386ffc0f5fef0b77738bb5449d50efeea95` | `GeneralSchauderBasis`, `GeneralSchauderBasis.proj`, `.range_proj_eq_span`, `.finrank_range_proj`; `SchauderBasis.proj`, `.tendsto_proj`, `.exists_norm_proj_le` | Valuable object-model and bridge substrate; no root closure |
| repository Grothendieck artifact | repository base `8014740e5a37eff82745f6fd2bc69f0ee45e67c9` | `CompactConvergenceApproximationProperty`, `SequentialApproximationWitness`, `finiteDimensional_hasSequentialApproximationWitness` | Adjacent local vocabulary and finite-dimensional special case only; explicitly not a terminal approximation theorem |
| gaussian-field nuclear infrastructure | `mrdouglasny/gaussian-field@d63a28568a75d99f6cb27af1f888a49a69855a66` | `GaussianField.NuclearFactorization.clm_image_growth`, `.nuclear_clm_representation` | External anchor only; uses Schauder expansion as input and does not prove Enflo's counterexample |

The mathlib source file
`Mathlib/Analysis/Normed/Module/Bases.lean` has SHA-256
`5daee171c6a9d29bba8c7c7f2683bfeea76b893c137fdc2d2330ca62b8526092` in the pinned tree. Its
Schauder API first entered that tree at commit
`58f63c64f7207514bdd291f66d1b67e62e6f8a20` (`feat(Analysis/Normed): Schauder basis definition and
characterization via projections (#34209)`), which is an ancestor of the audited pin.

## Search boundary

Repository-local Lean and pinned mathlib were searched for `Enflo`, `SchauderBasis`,
`ApproximationProperty`, and the phrase `approximation property`. The only target-adjacent local
implementation is `S1_M_215.lean`, and pinned mathlib has no `Enflo` or approximation-property
terminal declaration. GitHub repository-metadata searches for `Enflo language:Lean`,
`SchauderBasis language:Lean`, and `"approximation property" Banach Lean` each returned zero
repositories on 2026-07-12.

The external negative result is deliberately bounded. Unauthenticated GitHub code search returned
HTTP 401, grep.app returned HTTP 429, and HTML search timed out. These failures are limitations, not
evidence that no such code exists anywhere. The immutable gaussian-field source was inspected
because the repository already identified it as nearby Lean 4 nuclear-space infrastructure; its
types do not match the target.

## Exact local validation

Run from the repository root:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; standard reports 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; manifest ranks and target set pass |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0324/AnchorAudit.lean` | exit 0; every listed mathlib anchor elaborates in the pinned environment |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0324/Statement.lean` | exit 0; the canonical target still elaborates against that same pinned environment |
| `python3 -m json.tool Stage1_Instances/THM-M-0324/anchor-audit.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0324` | exit 0 |

No `lake update`, build, clone, fetch, or `.lake` mutation was performed. The existing untracked
`Formalizations/Lean/.lake` link/artifact was present before this phase and was used read-only.
