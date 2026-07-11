# Intake validation

Base revision: `dbd29db42090d2fce49f69d84d4631769ef7e9c3`.

Commands executed from the repository root:

```text
python3 Docs/tools/check_stage1_standard.py
# exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
# exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)

python3 scripts/stage1_target.py show THM-M-1042
# exit 0: rank 235; baseline L0; rework_required true; lifecycle planned; theorem_complete false
```

These are intake checks, not Lean kernel evidence. Dossier JSON parsing, local-reference checks, and
whitespace validation are recorded by the worker self-test after artifact creation.
