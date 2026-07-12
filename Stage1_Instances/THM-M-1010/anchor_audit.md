# Anchor audit

Audit date: 2026-07-12. Base revision:
`2f6e19989b487204f2450ca715a29105beb445a7`. The canonical expression is
`Stage1Instances.THM_M_1010.Target`; no alternate theorem was used.

## Result

No exact root theorem was found in pinned mathlib or the pinned dependency tree. The useful
mathlib declarations are interfaces and proof ingredients, not closure:

| Candidate | Exact audited role | Root gap |
|---|---|---|
| `LevyProkhorov.eq_convergenceInDistribution` | equates weak convergence with the Levy-Prokhorov topology on separable spaces | no coupling construction, laws, or a.s. convergence |
| `LevyProkhorov.probabilityMeasureHomeomorph` | packages that topology bridge | same construction gap |
| `ProbabilityTheory.HasLaw` and `HasLaw.map_eq` | exact marginal-law interface used by `Representation` | predicate only; no representatives exist by virtue of it |
| `PolishSpace.measurableEquivOfNotCountable` | possible measurable transport for a later construction | does not preserve the original topology and is not a coupling theorem |
| `TendstoInMeasure.exists_seq_tendsto_ae` | nearby a.e.-subsequence result | starts with common-space functions and yields only a subsequence |

All paths above are immutable at mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; their exact source blob IDs and rejection reasons are
in `anchor_audit.json`. A recursive case-insensitive search of all pinned package Lean sources for
`skorokhod` and `skorohod` returned no matches.

External searches used both spellings and theorem/repository variants. GitHub repository search
returned no Skorokhod Lean repository. The one returned repository for `weak convergence` and Lean,
`BryceT233/two-properties-of-weak-convergence` at immutable commit
`3e50fe3c4d8b3ed448cc92ff1fc22a7871194ea4`, concerns weak convergence in uniformly convex normed
spaces and is not a probability coupling candidate. Unauthenticated GitHub code search was gated by
sign-in and grep.app returned HTTP 429, so the negative result is scoped to the enumerated searches;
it is not an assertion that no unpublished or unindexed formalization exists.

The classification remains `[H1, M3, R3]` with `formalization_debt`. There is no identified external
Lean proof and hence no current `repo_local_integration_debt`. The next phase must build the
obligation tree around a genuine coupling construction; none of the candidates may be promoted to
root proof credit.

## Validation

Commands ran in this worker clone and did not mutate `.lake`:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage pass |
| `python3 scripts/stage1_target.py check` | 0 | ordered target manifest passes |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | rank 290, uniform L0/rework target confirmed |
| `rg -ni 'skorokhod|skorohod' Formalizations/Lean/.lake/packages --glob '*.lean' --glob '*.md' --glob '*.tex'` | 1 expected | no match in the complete pinned dependency tree |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact expected mathlib commit printed |
| `lake env lean ../../Stage1_Instances/THM-M-1010/Statement.lean` (from `Formalizations/Lean`) | 0 | frozen target re-elaborates |
| `lake env lean ../../Stage1_Instances/THM-M-1010/AnchorAudit.lean` (from `Formalizations/Lean`) | 0 | every retained candidate elaborates in the pinned environment |
| `python3 -m json.tool Stage1_Instances/THM-M-1010/anchor_audit.json` | 0 | structured audit parses |
| `git diff --check -- Stage1_Instances/THM-M-1010` | 0 | no whitespace errors |

This is node-scoped provisional worker evidence pending master acceptance. It makes no theorem
completion claim.
