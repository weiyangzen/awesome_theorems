# Intake validation record

Base revision: `7ea3aa8c0960c44b00d62639e9ddf1321848e342`.

All commands ran from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1313` | 0 | rank 478, planned, L0/rework_required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1313/intake.json` | 0 | valid JSON |
| `test "$(find Stage1_Instances/THM-M-1313 -maxdepth 1 -type f \| wc -l)" -eq 3` | 0 | the three intake artifacts existed before this validation record was added |
| `rg -n 'THM-M-1313\|S56-M-1313-INTAKE' Stage1_Instances/THM-M-1313` | 0 | dossier identifiers and merge targets resolved |
| `git diff --check` | 0 | no whitespace errors |

These are structural intake checks, not Lean elaboration or theorem validation. Known open gates are
the source identity, exact source statement, Lean declaration/environment fingerprint, source and
candidate audits, obligation registry, proof, and all release gates.
