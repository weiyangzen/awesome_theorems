# THM-M-1065 anchor-audit validation

Item: `S56-M-1065-ANCHOR_AUDIT`  
Base revision: `4344dc4263d0bcc8c386ec0ae1ad4e508c910b1e`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The exact comparison target is
`Stage1Instances.THM_M_1065.KMTStrongApproximationTarget`. The repository and pinned mathlib searches
found no Lean proof of the KMT common-space coupling with its uniform `C log n + x` discrepancy and
exponential tail. Mathlib revision `8a1783...a95` supplies the checked Gaussian-law, `HasLaw`, and
`iIndepFun` interfaces used by the statement, but these are substrate rather than a terminal proof.

Two GitHub repository-search queries returned zero repositories. This is recorded as bounded
discovery evidence, not as a global nonexistence result; unauthenticated repository metadata search
does not provide exhaustive public code search. No external dependency was fetched or added.

The exact root therefore remains `M3`: its statement and required interfaces elaborate, but no
terminal exact formal candidate was located. The primary-source theorem/page and errata crosswalk
also remains open, so this phase does not establish `H0`, audit completion, or theorem completion.

## Commands and exact outcomes

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1,546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1065` | 0 | rank 507; planned; L0/rework-required; theorem incomplete |
| `rg -n -i 'Koml[oó]s\|Tusn[aá]dy\|KMT\|strong approximation\|strong invariance' . --glob '*.lean' --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1065/**'` | 0 | only incidental references to a distinct Komlos martingale theorem; no KMT proof declaration |
| same bounded query in `Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | no matching KMT or strong-approximation source |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| GitHub repository API query `\"Komlos-Major-Tusnady\" lean` | 0 | `total_count: 0`, `incomplete_results: false` |
| GitHub repository API query `\"strong approximation\" lean4` | 0 | `total_count: 0`, `incomplete_results: false` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1065/AnchorAudit.lean` | 0 | substrate declarations and both negative-completion guards elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1065/Statement.lean` | 0 | exact comparison target re-elaborated and printed |
| `python3 Stage1_Instances/THM-M-1065/check_anchor_audit.py` | 0 | immutable pin, clean package, source declarations, and fail-closed `M3` decision verified |
| `python3 -m json.tool Stage1_Instances/THM-M-1065/anchor-audit.json` | 0 | structured ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1065 .stage1-worker-selftest.json` | 0 | no whitespace errors |

All Lean commands used the existing pinned Lake artifacts. No `lake update`, build, dependency
clone/fetch, or `.lake` mutation was performed.

## Status boundary

This is self-tested anchor-audit evidence pending master acceptance. It completes the bounded
candidate inventory for this node only. It does not change the generated checklist/DAG, claim
`AUDIT-Z`, prove KMT, or claim theorem completion.
