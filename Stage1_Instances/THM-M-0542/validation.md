# Intake validation

Base revision: `ed4c9bd55f9fcfd10e711dd571aceaedd188fbcc`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, the
available pinned Lean executable, and whitespace. No canonical Lean proposition has been selected,
so no elaboration or kernel-proof result is claimed. The canonical `.lake` symlink was used
read-only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0542` | exit 0; rank 599, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| `python3 -m json.tool Stage1_Instances/THM-M-0542/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0542/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0542 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are selection and independent review of an exact source proposition,
canonical Lean elaboration and mutation tests, exhaustive anchor audit, obligation registry,
proof, hermetic replay, and release validation. These prevent theorem completion but do not
invalidate this fail-closed planned intake.
