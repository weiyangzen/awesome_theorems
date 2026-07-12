# Anchor-audit validation record

Item: `S56-M-0988-ANCHOR_AUDIT`  
Base revision: `b781ef440e9de69e6413b608ce5542eed8c0070e`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact terminal
declaration `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub`. It matches every frozen
binder and material clause, including the finite second moment, family independence, identical
distribution, centered `sqrt n` normalization, target Gaussian variance, source/target measures,
and the zero-variance case. `AnchorAudit.lean` independently restates the proposition and elaborates
the direct bridge. Its axiom report is `propext`, `Classical.choice`, and `Quot.sound`, with no
`sorryAx`.

The bounded external search found an exact chapter-facing alias in
`lean-hansen-econometrics@b05e2b8...`; it delegates to the same pinned mathlib declaration and adds
no independent proof body. `atlas-lean@34ffed3...` instead states a triangular-array
Lindeberg-Feller result whose analytic dependency contains explicit `sorry` bodies, so it is both a
different target and `M5`. Neither should become a new dependency. The Sourcegraph search hit its
100-result cap, so its inventory is not presented as proof of global completeness.

This identifies an `M0-L` candidate already inside the immutable local closure. The classification
is deliberately pending the downstream obligation, proof, trust, provenance, validation, and
release gates; this phase does not claim theorem completion.

## Commands and results

All commands used the existing pinned artifacts. No Lake update/build, dependency fetch/clone, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0988` | 0 | rank 268, planned, legacy artifacts unaccepted, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg` over repo-local and all pinned dependency Lean sources | 0 | exact terminal body occurs in mathlib; local S1-M-267/S1-M-268 wrappers delegate to it |
| Sourcegraph public search for the exact declaration, central-limit phrase, and Lindeberg | 0 | 100 capped matches in Hansen, Atlas, and automath; response SHA-256 `651e60...1ea` |
| immutable raw inspection of Hansen `Chapter6Asymptotics.lean` | 0 | exact redundant alias; source SHA-256 `99fe197d...18e3`; same Lean/mathlib pins |
| immutable raw inspection of Atlas `LindebergFeller.lean` | 0 | distinct triangular-array theorem with transitive `sorry`; source SHA-256 `c2a38afa...02b7` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0988/AnchorAudit.lean` | 0 | exact bridge and four mathlib probes elaborated; no `sorryAx` in axiom report |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0988/Statement.lean` | 0 | frozen statement and four mutation shapes re-elaborated |
| `python3 Stage1_Instances/THM-M-0988/check_anchor_audit.py` | 0 | pin, module hash, target clauses, status boundary, and four candidate classes agreed |
| `git diff --check -- Stage1_Instances/THM-M-0988 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The node is self-tested pending master acceptance. It supplies no human-source `H0`, accepted proof
node, hermetic replay, independent receipt, or theorem-completion credit.
