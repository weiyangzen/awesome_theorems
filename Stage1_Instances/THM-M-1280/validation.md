# Intake validation record

Base revision: `73a92b5e63e8eb3c93a5c95d5aead1658ca24c79`.

The worker ran these commands from the repository root after creating the dossier:

```text
python3 -m json.tool Stage1_Instances/THM-M-1280/intake.json >/dev/null
# exit 0

python3 Docs/tools/check_stage1_standard.py
# exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows,
# 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
# exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-1280
# exit 0: rank 451; baseline L0; lifecycle planned; theorem_complete false

rg -n 'THM-M-1280|S56-M-1280-INTAKE' Stage1_Instances/THM-M-1280
# exit 0: item ID occurs in intake.json; theorem ID occurs in intake.json and README.md;
# public merge targets resolve to dossier-local paths

git diff --check
# exit 0, no output
```

This is the smallest real validation for an intake-only node. No Lean file or canonical Lean
expression exists in this phase, so no elaboration or kernel proof command is claimed. The first
failed theorem gate remains the statement gate.
