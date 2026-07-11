# Intake validation record

Base revision: `7a8e792e568c85805fef02f4071bcc4b5ac9e09d`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1202` | 0 | rank 396, planned, L0/rework-required, no accepted legacy artifacts, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1202/intake.json` | 0 | structured intake is valid JSON |
| `rg -n --glob '*.lean' 'sorry|admit|sorryAx|axiom' Stage1_Instances/THM-M-1202` | 1 | no Lean files or prohibited Lean proof constructs found (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-1202 .stage1-worker-selftest.json` | 0 | no whitespace errors in the owned dossier or handoff manifest |

This is the smallest real validation for an intake-only node. No Lean declaration or proof is added,
so elaboration, kernel, axiom-closure, and theorem gates remain open. Master acceptance is pending.
