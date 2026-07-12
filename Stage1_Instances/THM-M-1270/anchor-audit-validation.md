# THM-M-1270 anchor-audit validation

Item: `S56-M-1270-ANCHOR_AUDIT`  
Base revision: `3a3bd9b5ae3837526b6a41daf06c7587654c209d`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The canonical statement and all inspected repo-local partial anchors elaborate
against mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
The legacy module contains proof-bearing transports from an *assumed* maximal
descent point or complete-metric descent package, but it does not construct
either object and does not prove its `StatementShape`. Mathlib supplies lower
semicontinuity, compact-set minimum attainment, Cauchy-sequence, and completeness
infrastructure, not a terminal Ekeland or Caristi theorem.

Case-insensitive source search of every materialized pinned Lake dependency found
no named terminal candidate. Bounded GitHub repository searches returned zero
repositories for the recorded queries. Public code search was not fully
available, so the audit makes no exhaustive external-search claim.

The exact root remains `M3` and is not kernel-closed. This completes candidate
classification for this anchor-audit phase only; it does not claim proof,
validation, release, or theorem completion.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | passed: 15 assurance groups, 41 legacy rows, 300 slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | passed: 1546 unique targets and ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1270` | 0 | rank 163, planned, L0/rework-required, theorem incomplete |
| `git rev-parse HEAD` | 0 | `3a3bd9b5ae3837526b6a41daf06c7587654c209d` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{tree}` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `rg -n -i 'Ekeland|Caristi|VariationalPrinciple|variational principle|approximate minimizer|epsilon minimizer|strict perturbed minimizer' Formalizations/Lean/.lake/packages -g '*.lean' -g '*.md'` | 1 | no match in any materialized pinned dependency source tree |
| five read-only GitHub repository search API queries recorded in `anchor-audit.json` | 0 | each returned `total_count: 0` and `incomplete_results: false` |
| read-only grep.app code searches | 22 | HTTP 429; recorded as a limitation, not negative evidence |
| read-only Loogle query for `Ekeland` | 0 | service page reported that all workers were busy; recorded as a limitation |
| `lake env lean ../../Stage1_Instances/THM-M-1270/Statement.lean` from `Formalizations/Lean` | 0 | canonical target, premise transport, and mutations elaborated |
| `lake env lean AwesomeTheorems/Stage1/S1_M_163.lean` from `Formalizations/Lean` | 0 | legacy conditional scaffold and its mathlib anchors elaborated directly from source |
| `lake env lean ../../Stage1_Instances/THM-M-1270/AnchorAudit.lean` from `Formalizations/Lean` | 0 | classified mathlib infrastructure probes elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-1270/anchor-audit.json` | 0 | structured ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1270 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, dependency clone/fetch, or `.lake` mutation was performed.
