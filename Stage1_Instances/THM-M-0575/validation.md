# Intake validation record

Base revision: `70b89a1e28caca9edea8a7a51212cfb326ba834a`.

The worktree already contained the untracked symlink `Formalizations/Lean/.lake` to the canonical
pinned cache before this item was edited. This intake neither modified that cache nor ran a
dependency update, build, clone, or fetch.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0575` | 0 | rank 621, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0575/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n 'Bott periodic\\|BottPeriod\\|\\bBott\\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | no matches; no relevant topological K-theory periodicity declaration was located in this bounded source search |
| `rg -n "sorry\\|admit\\|sorryAx\\|^[[:space:]]*axiom[[:space:]]" Stage1_Instances/THM-M-0575 --glob '*.lean'` | 1 | no Lean files or forbidden proof escape matches; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0575 .stage1-worker-selftest.json` | 0 | no whitespace errors |

These are the smallest real checks for an intake-only node. No Lean declaration is introduced, so
no `lake env lean` kernel result, exact-type evidence, or axiom closure is claimed. The exact source
statement, Lean statement gate, anchor audit, obligation registry, proof, release validation, and
master acceptance all remain open.
