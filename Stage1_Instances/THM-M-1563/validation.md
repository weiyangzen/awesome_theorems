# Intake validation

Base revision: `2471626e15270bc76934bc81b54ed509898577f6`.

Validation date: 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake` artifacts were read only;
no update, build, clone, fetch, or dependency mutation was performed. The pre-existing untracked
`Formalizations/Lean/.lake` link makes this nonrelease evidence.

Validation is limited to manifest consistency, planned-dossier structure, scoped invariants, JSON,
and whitespace. No canonical Lean proposition exists yet, so `lake env lean --version` fingerprints
the available toolchain but is not an elaboration or proof result.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1563` | 0 | rank 574, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81` |
| repository search for `KPZ`, `Kardar`, and `随机表面生长` excluding pinned dependencies | 0 | found only underspecified catalogue metadata and neighboring-topic mentions; no exact proposition or local Lean target |

The post-write checks additionally parse both JSON files, assert the target/item/lifecycle/root
vector, verify that accepted states are empty and all six downstream tasks are open with the
expected dependency chain, reject forbidden proof-placeholder tokens in owned files, and run
`git diff --check` on the owned path.

Known downstream failures are exact source-statement identity, canonical Lean elaboration, anchor
audit, frozen obligation graphs, proof, hermetic validation, and independent review. These prevent
statement or theorem completion but do not invalidate this deliberately open `planned` intake.
