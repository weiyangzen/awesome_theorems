# Intake validation

Base revision: `7ef318624419c655b58febd5f373b9327c4f1268`.

Validation is limited to target/manifest consistency, dossier structure, scoped intake invariants,
the pinned Lean executable's availability, narrow repository and pinned-mathlib discovery searches,
and whitespace. No canonical Lean expression has been selected, so no elaboration or kernel-proof
result is claimed. The canonical `.lake` artifacts were used read-only; no update, build, clone, or
fetch command was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0585` | exit 0; rank 626, planned, L0/rework_required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository and pinned-mathlib `rg` search for Seiberg-Witten and monopole theorem terms | search completed; only the explicitly non-evidentiary `S1_M_252.lean` package fields were found, with no pinned-mathlib theorem-specific match |
| `python3 -m json.tool Stage1_Instances/THM-M-0585/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0585/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0585 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary-source result selection and independent review,
canonical Lean elaboration and mutation tests, exhaustive formal-anchor audit, obligation registry,
proof, hermetic replay, and release validation. They prevent theorem completion but do not
invalidate this truthful `planned` intake.
