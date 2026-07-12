# Intake validation

Base revision: `b5768b55f94197ed20d70d350ea6d4def3c3a667`.

Validation is limited to target membership, repository consistency, the planned dossier's
structure and invariants, pinned-toolchain identity, scoped discovery, JSON syntax, and whitespace.
The canonical human proposition is not uniquely identified, so there is no exact Lean expression
to elaborate and no kernel theorem result is claimed. Existing `.lake` artifacts were read only;
no update, build, clone, fetch, or dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0676` | exit 0; rank 577, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | exit 0; Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes `651c8acc...b1d2` and `321626c8...2d81` |
| scoped `rg` searches for prime/atomic models in repository Lean and pinned `Mathlib/ModelTheory` | exit 0 for atomic-formula hits; no prime-model theorem/module found; not a full anchor audit |
| `python3 -m json.tool Stage1_Instances/THM-M-0676/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0676/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0676 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary-source selection and independent review, canonical
Lean statement and structural mutations, formal-anchor audit, obligation registry, proof,
hermetic replay, and independent release validation. These prevent theorem completion but do not
invalidate the self-tested, fail-closed planned intake. No accepted proof state or downstream-node
credit is recorded.
