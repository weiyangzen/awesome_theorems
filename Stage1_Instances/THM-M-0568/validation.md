# Intake validation

Base revision: `56f664bd25214d40605c0b36e238c3e0cd9f1d9d`.

Validation is limited to target/manifest consistency, dossier structure, scoped intake invariants,
JSON syntax, and whitespace. The exact mathematical proposition is not selected, so there is no
applicable `lake env lean <target>.lean` command and no elaboration or kernel-proof result is
claimed. The existing `.lake` dependency artifacts were only searched; they were not mutated.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0568` | exit 0; rank 616, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -i 'Euler class|欧拉类|eulerClass|euler_class|Thom class|ThomClass' .` with generated execution files, other instance dossiers, and `.lake` excluded | exit 0; found only target metadata plus an out-of-scope arithmetic `EulerClass` API |
| `rg -n -i 'Euler class|eulerClass|euler_class|Thom class|ThomClass' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; no matching topological Euler/Thom class text in the pinned mathlib source (`rg` exit 1 means no match) |
| `python3 -m json.tool Stage1_Instances/THM-M-0568/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0568/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0568` | exit 0; no output |

Known downstream failures are intentional and explicit: corrected theorem selection, exact
primary-source inspection and independent review, canonical Lean elaboration, anchor audit,
obligation registry, proof, hermetic replay, and release validation remain open. They prevent
theorem completion but do not invalidate this truthful planned intake.
