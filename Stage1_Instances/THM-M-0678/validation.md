# Intake validation

Base revision: `6fb5d7698be077f0e9c0e01fac425d492ec114c8`.

Validation is intentionally limited to target-set consistency, dossier syntax, scoped intake
invariants, pinned environment identification, and whitespace. The metadata does not identify one
proposition, so elaborating a Lean theorem would test an invented or substituted target. No kernel
statement/proof, source review, audit completion, or theorem completion is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0678` | exit 0; rank 720, planned, no accepted legacy artifacts, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |
| `python3 -m json.tool Stage1_Instances/THM-M-0678/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0678/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `for f in Stage1_Instances/THM-M-0678/*; do git diff --no-index --check /dev/null "$f" >/dev/null \|\| test $? -eq 1; done` | exit 0; no whitespace errors in the untracked intake files |

The existing canonical `.lake` artifacts were used read-only. No update, build, dependency clone,
fetch, or other dependency mutation was performed.

Known downstream failures are exact primary-source selection and independent review, separation
from `THM-M-0679`, canonical Lean statement and elaboration, mutation tests, anchor audit,
obligation registry, proof, hermetic replay, and release review. These remain open without
invalidating this truthful planned intake.
