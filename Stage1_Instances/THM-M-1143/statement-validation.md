# Statement validation record

Item: `S56-M-1143-STATEMENT`  
Base revision: `c37f5c9477ecee2c5ecf444e75e52be738eff1a8`

All commands ran inside this worker clone. Lean used the existing pinned Lake closure; no package
update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1143/Statement.lean` | 0 | canonical target and five structural mutations elaborated; explicit canonical expression printed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1143` | 0 | rank 348, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1143/statement.json` | 0 | structured statement record parses |
| scoped prohibited-declaration scan of `Statement.lean` | 1 | clean; exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-1143 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The statement source SHA-256 is
`a4ed1193c0c91ec8ba4237e46e2dbee38da52d143919f549f96616c2e05589bd`. The SHA-256 of its
printed explicit expression is
`e05a7b951bf36aedbc370a3f6ad2950c86b63b4d3a8af1d0e031290b62701610`.

This evidence validates exact target elaboration only. Primary-source acceptance, anchor audit,
proof, trust closure, hermetic replay, independent verification, theorem completion, and master
acceptance remain open.
