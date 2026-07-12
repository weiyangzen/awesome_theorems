# Anchor audit record

Item: `S56-M-1012-ANCHOR_AUDIT`  
Audit date: `2026-07-12`  
Base revision: `b2c5ff63ca2e762d1b24d1dc514782747d1a6e1b`

## Exact pinned candidate

The frozen known-limit target has an exact theorem in the already-pinned mathlib dependency:

| Field | Immutable audit result |
|---|---|
| Repository | `https://github.com/leanprover-community/mathlib4.git` |
| Revision | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| Module | `Mathlib.MeasureTheory.Measure.LevyConvergence` |
| Declaration | `MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun` |
| Source at revision | `Mathlib/MeasureTheory/Measure/LevyConvergence.lean:212-219` |
| Source git object | `fc0bf2a7054634763040aa9bbcaae5f2c93b8d5f` |
| Source SHA-256 | `54fa4a3baec8a8ab916524dd63c52a6da70bc919031e20318b198fa20755fff8` |
| Introducing commit | `901a41358322e44c48a679486effd3b34e6d12ed` (2026-03-09) |
| Toolchain | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| Axioms reported | `propext`, `Classical.choice`, `Quot.sound` |
| Dependency feasibility | Already in the canonical Lake closure; no fetch or new dependency |

`AnchorAudit.lean` gives the theorem an explicit type identical to the statement node's binders,
coercions, topology, sequence index, and both directions of the equivalence. Lean accepted `exact
ProbabilityMeasure.tendsto_iff_tendsto_charFun`, so this is an exact closure rather than a related
lemma. The source module contains a proof body. A scoped scan found no `sorry`, `admit`, `axiom`, or
`unsafe` token in that file.

The important supporting nodes are `ProbabilityMeasure.tendsto_of_tendsto_charFun`,
`isTightMeasureSet_of_tendsto_charFun`, and
`ProbabilityMeasure.tendsto_charPoly_of_tendsto_charFun`. Their detailed transitive proof and trust
graph belongs to the later obligation and validation phases.

## External search

All 11 repositories already pinned by the Lake closure were searched at their checked-out immutable
revisions. Only mathlib contains the exact declaration; mathlib's central-limit theorem is a consumer,
not an independent proof. Public GitHub repository-metadata searches for `Levy convergence`, `Levy
continuity`, and `characteristic function probability lean4` returned no repositories. This is not a
claim of global nonexistence: unauthenticated GitHub repository search is weaker than code search, and
the attempted grep.app code searches returned HTTP 503. No dependency was cloned, fetched, updated, or
built.

## Validation

Commands ran in this worker clone. Lean ran from `Formalizations/Lean` against the existing pinned
Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1012/AnchorAudit.lean` | 0 | exact wrapper elaborated; candidate and wrapper reported only the three listed axioms |
| `rg -n -i "levy|lévy|continuity theorem|charFun.*Tendsto|Tendsto.*charFun" Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | exact candidate located in pinned mathlib; no independent pinned-package implementation |
| `rg -n 'sorry|admit|axiom|unsafe' Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/LevyConvergence.lean` | 1 | expected no-match result |
| GitHub REST repository searches recorded in `anchor-audit.json` | 0 | zero matching repositories for all three queries |
| grep.app API searches recorded in `anchor-audit.json` | 22 | known external-service failure: HTTP 503 |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1012` | 0 | rank 291, planned, L0/rework-required, theorem incomplete |

## Status boundary

The audit discovers an `M0-L` candidate and removes any need for a new external dependency. This node
does not itself promote machine debt, prove H0 or R0, freeze the obligation graph, issue a master
receipt, or establish theorem completion. Those remain downstream gates. Primary-source
edition/theorem/page/errata review is explicitly still open.
