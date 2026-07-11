# Intake validation record

Base revision: `5997161aebf527e8a1e05724d4fbd4ce07dfd815`.

This record covers dossier structure only. The clone contains no `lean-toolchain`, Lake manifest,
or mathlib checkout, so no Lean elaboration was possible or claimed during intake.

Commands are run from the repository root. Exact results are appended after validation.

| Command | Exit | Result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0413` | 0 | rank 68, planned, hard_mathlib_anchor_and_wrapper, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0413/intake.json` | 0 | intake JSON parses successfully |
| `rg -n "/home/\|slot17\|sorry\|axiom\|placeholder\|fake results" Stage1_Instances/THM-M-0413` | 0 | one prose occurrence each of `axioms` and `placeholders` in the list of future audit checks; no absolute path, worker-slot reference, Lean placeholder, or fake result |
| `git diff --check` | 0 | no whitespace errors |

Known limitation: these are intake self-tests, not an exact-type or kernel check. The dependent
statement phase remains blocked on selecting and pinning a Lean/mathlib environment and verifying
the candidate declaration names.
