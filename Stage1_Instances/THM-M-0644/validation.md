# Intake validation

Base revision: `1794fae27ddcf6d19b6984502e27a9233890d8d1`.

Validation is scoped to target membership, dossier structure/invariants, and a narrow elaboration
probe against existing pinned artifacts. The probe checks a formal candidate only. It is not the
rev-5.6 statement gate and establishes no accepted kernel proof or theorem completion.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0644` | exit 0; rank 690, planned, legacy artifacts unaccepted, theorem_complete false |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | exit 0; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...6d81` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0644/IntakeProbe.lean` | exit 0; `IsSatisfiable`, `IsFinitelySatisfiable`, and the compactness candidate elaborated with type `T.IsSatisfiable ↔ T.IsFinitelySatisfiable` |
| `python3 -m json.tool Stage1_Instances/THM-M-0644/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0644/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` (identity, lifecycle, rank, owned files, empty accepted states, and the exact open dependency chain) |
| `git diff --check -- Stage1_Instances/THM-M-0644` | exit 0; no output |

Known downstream failures: exact expression and environment fingerprints, checked alternate
encoding, statement mutations, pinpoint primary-source audit, formal-candidate provenance and trust
audit, obligation registry, proof credit, hermetic replay, and independent review remain open. These
prevent all later completion claims but do not invalidate a fail-closed `planned` intake.
