# Intake validation record

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

Commands run from the repository root on 2026-07-12:

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0111` | 0 | rank 24, `planned`, `L0`, rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0111/intake.json` | 0 | intake record is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0111` | 0 | no whitespace errors |

No Lean build is claimed: intake deliberately does not accept or modify the
legacy abstract statement. Exact elaboration belongs to the dependent statement
node. The smallest real validation for this phase is repository conformance,
manifest membership, dossier JSON parsing, and whitespace validation.
