# Intake validation

Date: `2026-07-12` (Asia/Shanghai)  
Base revision: `b4a9f9e80f3579c12ae2c4dd14b53440530042ec`

These checks validate only the planned intake dossier, scope map, and source-statement crosswalk.
They do not elaborate a Lean target, validate a proof, accept an `H0` source record, or establish
theorem completion. The pre-existing untracked `Formalizations/Lean/.lake` link was not modified.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok` with 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok` with 1546 unique ranks `1..1546`, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0163` | 0 | Rank 662; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0163/check_intake.py` | 0 | `check_intake: ok (THM-M-0163 planned scope, source crosswalk, and open gates validated)` |
| `python3 -m json.tool Stage1_Instances/THM-M-0163/intake.json >/dev/null` | 0 | Intake JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0163` | 0 | No whitespace errors |
| `sha256sum Stage1_Instances/THM-M-0163/{intake.json,README.md,source_statement_crosswalk.md,check_intake.py}` | 0 | SHA-256: `855c0e...689`, `4cfdf2...a32`, `d7eaeb...d87`, `c58935...f05` respectively |
| `git status --short` | 0 | Reported pre-existing `?? Formalizations/Lean/.lake` and owned `?? Stage1_Instances/THM-M-0163/`; no other changes |

The item is ready only for provisional worker state `[_]` and master review. First failed theorem
gate remains the dependent exact-statement gate. Root vector remains `[H2, M4, R3]` and
`theorem_complete` remains false.
