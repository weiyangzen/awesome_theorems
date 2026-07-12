# THM-M-1246 proof-phase attempt

Item: `S56-M-1246-PROOF`  
Date: `2026-07-12`  
Base revision: `11e7ace1a3eba66e560393864e23d09e8aaf1273`

## Verdict

`blocked`: no eligible proof body for the exact Euclidean differential `L2`
Hardy inequality exists in the repository or pinned dependency closure. The
immediate root cut remains `M1246-T-ANALYTIC`. Its frozen route needs genuine
Lean proofs for the punctured-domain cutoff, the divergence identity for
`x / ||x||^2`, compact-support integration by parts, derivative and
Cauchy-Schwarz bounds, cutoff removal, and sharp-constant rearrangement.

`ObligationTree.root_of_hardyTerminal` is a real kernel-checked identity
composition, but it accepts `HardyTerminal` as a premise and does not inhabit
it. The four pinned declarations in `AnchorAudit.lean` are unweighted Sobolev
inequalities with different exponents and constants; none supplies or
definitionally transports to the frozen inverse-square weighted target.
Consequently the root remains `M3` and no proof source was added.

Adding the missing analytic package as an axiom, theorem premise, or bodyless
declaration would be a prohibited placeholder. Substituting a Sobolev analogue
would broaden or change the theorem. Because the assigned proof deliverable is
not complete, this attempt deliberately leaves `.stage1-worker-selftest.json`
absent.

## Narrow validation evidence

All commands ran in the worker clone and reused the existing canonical pinned
Lake artifacts. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1246` | 0 | Rank 426; baseline L0; lifecycle planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1246/check_statement.py` | 0 | Exact expression hash `07f1c030325dfe8d02e99a0af1a00c5241a312e6195aa4a9e2967822960048f1`; three statement mutations distinguished. |
| `python3 Stage1_Instances/THM-M-1246/check_anchor_audit.py` | 0 | Pinned hashes, four analogue classifications, forbidden-token checks, and Lean elaboration passed. |
| `python3 Stage1_Instances/THM-M-1246/check_obligation_tree.py` | 0 | 15 obligations and 61 typed edges passed; denominator `dd6e6ca1fc734ea8f477095e77a99601a3387cd914de7e599c9343b874ae2d6d`; conditional composition passed and root remained open at `M1246-T-ANALYTIC` (`M3`). |
| `rg -n -i 'hardy.?inequal\|hardy_inequal\|hardyInequality\|∫.*u.*\/.*‖x‖\|u x.*‖x‖.*fderiv' --glob '*.lean' Stage1_Instances/THM-M-1246 Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Exact-target hits were confined to this dossier; no terminal pinned declaration was found. The prerequisite anchor audit records broader bounded searches and the nearest analogues. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx\|unsafe' Stage1_Instances/THM-M-1246 -g '*.lean'` | 1 | Expected no-match result: no prohibited Lean declaration token was found. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `sha256sum Stage1_Instances/THM-M-1246/{Statement.lean,ObligationTree.lean,obligation-registry.json}` | 0 | `0388e86c...ddf41`, `794d7584...aac6`, and `55abd985...fd2e`. |

## Reopen condition

Resume only after either a placeholder-free implementation of
`M1246-T-ANALYTIC` and its frozen analytic dependencies, or discovery of an
eligible immutable Lean 4 proof that can be pinned, exact-type transported,
and checked in the repository closure. Until then `root_closed=false`, the
root remains `[H2, M3, R4]`, and theorem completion remains false.
