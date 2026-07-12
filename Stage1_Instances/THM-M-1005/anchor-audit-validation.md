# Anchor-audit validation record

Item: `S56-M-1005-ANCHOR_AUDIT`  
Base revision: `d1f51b88124ac7e1027cf7a0effa59c31030de04`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The exact frozen target is the strong finite-horizon `L^p` estimate for the absolute running
maximum of a real martingale. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` does not contain that terminal theorem. Its closest
declaration is `MeasureTheory.maximal_ineq`, a weak threshold/set-integral inequality for a
nonnegative submartingale. The immutable source itself says the `L^p` corollary is future work.
`AnchorAudit.lean` checks a direct wrapper of this related theorem; the axiom report is `propext`,
`Classical.choice`, and `Quot.sound`, with no `sorryAx`.

The legacy target file reaches the same boundary: its exact `DoobLpMomentEstimateStatement` is only
a proposition definition, while its proved wrappers terminate at the weaker mathlib theorem. A
search across repo-local and every materialized pinned dependency Lean source found no other exact
candidate. Anonymous GitHub repository metadata returned zero repositories for the narrow query,
but GitHub code search required authentication, grep.app rate-limited all three queries, and the
attempted Sourcegraph endpoint returned 404. Those lanes are recorded as access failures rather
than false negative claims.

The exact root therefore remains `M3`: relevant checked interfaces exist, but the target itself has
only a statement shape and no terminal body or checked reduction. This completes the bounded
anchor-audit phase only; it does not claim exhaustive discovery or theorem completion.

## Commands and results

All Lean commands used the existing pinned `.lake` artifacts. No dependency update, build, clone,
fetch, or installation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1005/AnchorAudit.lean` | 0 | related weak theorem and five pinned interfaces elaborated; wrapper axiom report contained no `sorryAx` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1005/Statement.lean` | 0 | exact frozen target and four mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-1005/check_anchor_audit.py` | 0 | target fingerprint, manifest pin, installed HEAD, module hash, three candidates, and status boundary agreed |
| scoped `rg` over repo-local and all materialized pinned dependency Lean sources | 0 | found the legacy statement boundary and pinned weak theorem; no exact strong `L^p` terminal declaration |
| GitHub REST repository search | 0 | `total_count=0`, `incomplete_results=false`; response SHA-256 `08c082...600b2` |
| GitHub REST code search | 0 | captured HTTP 401 response; SHA-256 `b7dbd1...e29e`; access failure only |
| three grep.app API searches | 22 | HTTP 429 each; access failures, no negative result claimed |
| Sourcegraph public API attempt | 22 | HTTP 404; access failure, no negative result claimed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1005` | 0 | rank 285, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1005/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1005 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This node is self-tested pending master acceptance. `H2`, `M3`, and `R4` remain truthful; source
review, obligation architecture, proof, hermetic validation, independent review, full `AUDIT-Z`,
and `THEOREM-Z` remain downstream.
