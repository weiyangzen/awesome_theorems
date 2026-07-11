# Intake validation record

Base revision: `43b8783c62005322690acf2bed800ea3acbd76c6`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0173` | 0 | rank 127; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0173/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\\b(sorry|axiom|admit)\\b' Stage1_Instances/THM-M-0173` | 1 | no forbidden proof-placeholder token matches (`rg` returns 1 for no matches) |
| `git diff --check -- Stage1_Instances/THM-M-0173 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This is the smallest real validation for an intake-only node. No Lean source or theorem declaration
is introduced, so a kernel build would not validate any additional claim. Master acceptance and
all dependent phases remain outstanding.
