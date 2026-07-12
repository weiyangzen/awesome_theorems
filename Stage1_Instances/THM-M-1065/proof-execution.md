# THM-M-1065 proof-phase attempt

Item: `S56-M-1065-PROOF`  
Attempt date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `ceb0a98b07364cde2a40a2bae3b24317916319ef`

## Verdict

`blocked`; no proof body was added and no proof credit is claimed.

The exact target `Stage1Instances.THM_M_1065.KMTStrongApproximationTarget` re-elaborates in the
pinned Lean environment. The existing checked declarations establish only its direct definitional
expansion, the `n = 1` event boundary, and the equivalence between the root and a named complete
witness package. In particular, `kmtTarget_iff_couplingData` does not inhabit `CouplingData`; it
only repacks all of the still-open mathematical fields.

The prerequisite candidate audit found Gaussian-law, `HasLaw`, and independence interfaces in
pinned mathlib, but no exact KMT coupling or strong-invariance proof body. A fresh bounded search of
the pinned Lean sources again returned no KMT, author-name, strong-approximation, or
strong-invariance declaration. The first unavailable frozen construction is `M1065-C-SPACE`.
The quantitative finite-block coupling `M1065-L-BLOCK-COUPLING` and uniform exponential
maximal-tail package `M1065-L-MAXIMAL-TAIL` are also open, so no witness can reach
`M1065-T-COMPOSE` or the root.

Introducing the coupling as an axiom or premise, or replacing the running-maximum exponential
bound with a terminal-time or asymptotic invariance principle, would be a prohibited placeholder or
substituted theorem. The root therefore remains open at `M4`, with conservative cut set
`M1065-C-SPACE`, `M1065-L-BLOCK-COUPLING`, and `M1065-L-MAXIMAL-TAIL`.
Because the assigned proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately
absent.

## Narrow validation evidence

All commands ran in this worker clone using the existing pinned Lake artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1065` | 0 | rank 507; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1065/check_statement.py` | 0 | expression digest `b257ceb1...cebd0`; all four registered mutations distinguished |
| `python3 Stage1_Instances/THM-M-1065/check_anchor_audit.py` | 0 | immutable mathlib pin and substrate declarations verified; no terminal candidate credited |
| `python3 Stage1_Instances/THM-M-1065/check_obligation_tree.py` | 0 | 18 obligations and 75 typed edges passed; denominator `d5e21a3a...91ac2`; root open `M4` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1065/Statement.lean` | 0 | exact canonical target, expansion, and boundary body elaborated; only unused-variable linter warnings in mutation declarations |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1065/ObligationTree.lean` | 0 | definitional witness/root equivalence elaborated at its frozen type |
| `rg -n -i '\\b(Koml[oó]s\|Tusn[aá]dy\|KMT\|strong[ _-]approximation\|strong[ _-]invariance)\\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | expected no-match result; no KMT proof source found in pinned mathlib |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx\|unsafe' Stage1_Instances/THM-M-1065 --glob '*.lean'` | 1 | expected no-match result; no prohibited Lean declaration token found |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `sha256sum Stage1_Instances/THM-M-1065/{Statement.lean,ObligationTree.lean,obligation-registry.json}` | 0 | `7f3b249e...edaf1`; `9aa9a38f...b5873`; `79eb5a4c...7b44` |

## Reopen condition

Resume after implementing the frozen common-space, coupling, and maximal-tail packages without
placeholders, or after locating an immutable compatible Lean 4 proof whose exact type, terminal
bodies, dependency closure, axioms, license, and provenance can all be validated in the pinned
environment.
