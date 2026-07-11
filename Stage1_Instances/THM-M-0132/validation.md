# Intake validation record

Base revision: `478034dee4145f887a572a3c645a3a2ea81bc883`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all rework-required |
| `python3 scripts/stage1_target.py show THM-M-0132` | 0 | Rank 49 target confirmed as planned, L0, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0132/intake.json` | 0 | Intake JSON parsed successfully |
| `rg -n "sorry\|axiom\|placeholder\|theorem_complete.*true" Stage1_Instances/THM-M-0132` | 0 | One prose occurrence of `axioms`; no forbidden proof construct or completion claim |
| `git diff --check` | 0 | No whitespace errors |

These are the smallest real checks for the intake phase. No Lean build is credited because exact
statement elaboration is deliberately owned by the dependent statement phase. Known failures:
exact statement, source hashing, environment fingerprint, checked transports, and kernel proof
closure are open by design.
