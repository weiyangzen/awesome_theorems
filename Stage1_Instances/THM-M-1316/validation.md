# Intake Validation

Base revision: `337a6bea341c0f1616a624ad03e440cb829e61e3`.

The exact commands and results below were run from the repository root on 2026-07-12.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `ok` with 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1316` | exit 0; rank 479, planned, theorem incomplete, hard anchor/wrapper lane |
| `python3 -m json.tool Stage1_Instances/THM-M-1316/intake.json >/dev/null` | exit 0; JSON parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-1316` | exit 0; no whitespace errors |

This is structural and dossier-level validation only. No Lean command is appropriate to
claim because intake deliberately nominates no Lean module or declaration; statement
elaboration is the dependent `S56-M-1316-STATEMENT` phase.
