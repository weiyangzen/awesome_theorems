# Intake validation

Base revision: `5467f527e0c402d2d52235957d4f316892fcfb75`.

Validation is scoped to target membership, dossier structure/invariants, and a narrow elaboration
probe against existing pinned artifacts. The probe checks formal ingredients only. It is not the
rev-5.6 statement gate and establishes no canonical target or kernel-proof result.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0649` | exit 0; rank 695, planned, legacy artifacts unaccepted, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | exit 0; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...6d81` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0649/IntakeProbe.lean` | exit 0; elementary maps/substructures, Tarski-Vaught, directed `iSup` membership, direct-limit injection, and `Equiv_iSup` elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0649/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0649/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0649 .stage1-worker-selftest.json` | exit 0; no output |

The first probe attempt failed because `Mathlib.ModelTheory.DirectLimit` does not re-export
`ElementarySubstructures`; adding that minimal explicit import made the same probe pass. This is
recorded as resolved setup feedback, not omitted evidence.

Known downstream failures: exact primary-source theorem/page and independent review, the choice and
elaboration of a canonical chain encoding, checked alternate transport and mutation suite, full
formal-candidate audit, obligation registry, proof, hermetic replay, and release validation remain
open. They prevent every completion claim but do not invalidate this truthful planned intake.
