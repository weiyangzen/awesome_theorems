# Intake validation

Base revision: `8e78e1b4206fc224e91466efb397811c09205b0e`.

All commands below ran from the worker clone root on 2026-07-12 and exited 0:

```text
python3 -m json.tool Stage1_Instances/THM-M-1183/intake.json >/dev/null
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1183
! rg -n '\b(sorry|axiom)\b' Stage1_Instances/THM-M-1183/{README.md,intake.json,scope-map.md,source_statement_crosswalk.md}
git diff --check -- Stage1_Instances/THM-M-1183
```

The standard validator reported 15 assurance groups and 1546 uniform-L0 targets. The target
validator reported 1546 unique targets with ranks 1 through 1546. The target query confirmed rank
380, `planned`, `L0 / rework_required`, and `theorem_complete: false`. JSON parsing, forbidden-token
scan, and whitespace validation were clean. No Lean build was applicable because intake truthfully
selects no formal expression; exact elaboration is the dependent statement-phase gate.

Known open gates: exact theorem/source selection, primary-source inspection and immutable pin,
canonical Lean target, environment fingerprint, mutation tests, proof architecture, kernel closure,
and all release evidence.
