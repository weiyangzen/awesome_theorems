# Intake validation record

Base revision: `70b89a1e28caca9edea8a7a51212cfb326ba834a`.

Validation covers target membership, the planned dossier's structured invariants, the pinned Lean
tool's availability, and whitespace. There is deliberately no Lean declaration to elaborate: the
first failed gate is selection of a truth-valued mathematical statement, not tool availability.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, execution skill present, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0574` | 0 | Rank 620; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-0574/intake.json` | 0 | Valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0574/task-dag.json` | 0 | Valid JSON |
| scoped Python intake assertions | 0 | `intake invariant check: ok` |
| `rg -n '\\bsorry\\b|\\baxiom\\b|\\bplaceholder\\b' Stage1_Instances/THM-M-0574` | 1 | No forbidden proof tokens; exit 1 means no match |
| `git diff --check -- Stage1_Instances/THM-M-0574 .stage1-worker-selftest.json` | 0 | No whitespace errors |

Known failures are intentional and fail-closed: canonical statement, formal target, expression and
environment fingerprints, source acceptance, anchor audit, obligation registry, proof,
composition, hermetic replay, and independent review remain open. Master acceptance is also
outstanding. This validates only the intake node and does not claim theorem completion.

