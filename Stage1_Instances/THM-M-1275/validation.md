# Intake validation record

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

Commands were run from the repository root on 2026-07-12 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1275` | 0 | Rank 448; planned; hard_mathlib_anchor_and_wrapper; theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1275/intake.json >/dev/null` | 0 | Intake JSON parses |
| `python3` dossier reference check recorded below | 0 | IDs, lifecycle, completion boundary, required files, and README references agree |
| `git diff --check -- Stage1_Instances/THM-M-1275` | 0 | No whitespace errors |

The dossier reference check loaded `intake.json` and asserted: theorem ID `THM-M-1275`, item ID
`S56-M-1275-INTAKE`, lifecycle `planned`, `theorem_complete` is false, every
`public_merge_targets` path exists, and both dossier filenames referenced by `README.md` exist.

This is intake-only validation. No Lean elaboration or kernel proof was available or claimed; that
is the explicit first open dependent gate.
