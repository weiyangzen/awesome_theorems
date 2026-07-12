# Anchor-audit validation record

Item: `S56-M-0526-ANCHOR_AUDIT`  
Base revision: `dcaabb0eb5eb8036a02b4784805fa67640916f71`

The repo-local search inspected pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The external search used GitHub repository metadata
and immutable commit archives, not moving branch contents. Archives were unpacked only under `/tmp`;
no dependency was cloned, fetched, built, or added to `.lake`.

## Result

No exact Seifert-van Kampen theorem, implication candidate, or terminal proof body was found.
Pinned mathlib supplies `FundamentalGroup.map`, fundamental-groupoid functoriality, and a generic
categorical pushout predicate. These are substantive support anchors but do not prove the frozen
target. The similarly named categorical `IsVanKampenColimit` is a false positive. Four immutable
external inventories were inspected and excluded for the precise reasons recorded in
`anchor-audit.json`.

Consequently the honest classification is `not_repo_local_closed` with `formalization_debt`, not
`external_upstream_anchor_only` or M0. There is no discovered external closure that would create
repo-local integration debt.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage valid |
| `python3 scripts/stage1_target.py check` | 0 | ordered manifest valid |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'seifert.?van.?kampen|van.?kampen|vankampen' Formalizations/Lean/.lake/packages/mathlib/Mathlib/AlgebraicTopology` | 1 | no match; expected negative search |
| `lake env lean ../../Stage1_Instances/THM-M-0526/AnchorAudit.lean` (cwd `Formalizations/Lean`) | 0 | all supporting declarations resolved; axiom reports printed |
| `python3 Stage1_Instances/THM-M-0526/check_anchor_audit.py` | 0 | pinned revision matched; zero exact-name matches; four external inventories validated |

This phase is self-tested pending master acceptance. It makes no theorem-proof, audit-completion,
source-fidelity, or release claim.
