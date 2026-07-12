# THM-M-0721 anchor-audit validation

Item: `S56-M-0721-ANCHOR_AUDIT`  
Base revision: `4c5f3b4e2345949e13133860c3bbafd5be5d557b`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies the exact TM2
polynomial-time structure used by the frozen statement, but no NP, SAT, Cook-Levin, or
NP-completeness endpoint. Its nearby `TM2ComputableInPolyTime.comp` is `proof_wanted`, and
`Mathlib.Computability.Reduce.ManyOneReducible` is ordinary computable rather than polynomial-time
reducibility. These are statement substrates, not root proof anchors.

Three immutable external candidates were inspected. `AEjonanonymous/Cook-Levin-Lean` proves
fixed-tableau CNF properties but has no NP or universal-reduction statement. The Dominic Breuker
project has a headline `NPcomplete SAT`, but its own immutable README reports `sorryAx`, remaining
gaps, vacuous proof-path definitions, and a reduction contract that bounds output size rather than
runtime. Atlas has `CookLevin.cook_levin : IsNPComplete SATLang` at the same Lean/mathlib pins, but
root-relevant tableau, decision, and polynomial-reduction declarations contain `sorry`; it also
uses a different NTM/formula encoding and has no checked transport to the frozen TM2 binary-word
target. Neither headline is eligible for integration.

The root remains `M2`, not kernel-closed. This completes the bounded immutable candidate audit only;
it makes no theorem-completion claim.

## Commands and exact outcomes

No dependency operation or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | rank 578, planned, L0/rework-required, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact pin `8a178386...ea95` |
| scoped `rg` over pinned mathlib Lean source | 0 | TM2 polynomial-time substrate and computable many-one reduction found; no NP-completeness/Cook-Levin root found |
| GitHub repository search for quoted Cook-Levin plus Lean | 0 | two named repositories returned; immutable heads resolved to `f564ae98...ea7b` and `4c0ad8c...380` |
| Sourcegraph Lean search for NP-completeness/Cook-Levin spellings | 0 | 100-match bound reached across four repositories; limitation explicitly retained in the ledger |
| immutable raw-file inspection at the three recorded revisions | 0 | exact declarations, hashes, toolchains, pins, scope gaps, and placeholder evidence matched the ledger |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0721/Statement.lean` | 0 | frozen target and statement-boundary checks re-elaborated in the pinned environment |
| `python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | local revisions/hashes and all immutable candidate assertions matched; root remained `M2` |
| `python3 -m json.tool Stage1_Instances/THM-M-0721/anchor-audit.json` | 0 | structured ledger is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0721 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

The node is self-tested pending master acceptance. The bounded external search is not global absence
evidence. This node supplies no H0, accepted obligation/proof node, hermetic replay, independent
receipt, or theorem-completion credit.
