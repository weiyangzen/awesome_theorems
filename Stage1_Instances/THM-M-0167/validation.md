# Intake validation record

Base revision: `0091960f0657f8228ab5c8e3ca414cefd6c90931`.

All commands ran from the worker automation clone on 2026-07-12. The existing
canonical `.lake` artifacts were used without update, build, fetch, or other
mutation.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0167` | 0 | rank 664, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | 0 | hashes `651c8acc...b1d2` and `321626c8...b2d81` respectively |
| `rg -n -i 'Singer\|minimal surface\|minimal hypersurface\|locally homogeneous\|curvature homogeneous' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | only unrelated Ivan Singer bibliography matches; no candidate declaration identified |
| `python3 -m json.tool Stage1_Instances/THM-M-0167/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n -g '!validation.md' 'sorry\|admit\|sorryAx\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0167` | 1 | no forbidden proof-escape matches in the substantive dossier artifacts; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0167 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test manifest creation; rerun after creation |

This is an intake-only node and introduces no Lean declaration. Consequently,
there is no honest theorem elaboration or kernel proof check to claim in this
phase. The exact-statement gate, formal-candidate audit, all proof gates, and
master acceptance remain open. Dossier-local JSON, forbidden-token, and diff
checks are rerun after artifact creation and recorded in this table before the
worker self-test manifest is emitted.
