# Intake validation

Base revision: `b5a452fcaf03fdb99da11e1749d1f393684d8fe3`.

Validation is limited to repository/manifest consistency, dossier structure, scoped intake
invariants, toolchain availability, the narrow local formal-candidate search, and whitespace. No
canonical Lean expression has been selected in this intake phase, so no elaboration or kernel
result is claimed. The `Formalizations/Lean/.lake` symlink was already untracked at preflight; it
points to the canonical pinned artifacts, was not modified, and is classified as nonrelease input.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0162` | exit 0; rank 661, L0/rework_required, planned, theorem_complete false |
| `rg -n 'Frenet\\|Serret\\|frenet' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 1; no exact name hit (narrow discovery evidence only) |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux release |
| `python3 -m json.tool Stage1_Instances/THM-M-0162/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0162/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; checks identity, planned lifecycle, L0 baseline, rank, empty acceptance, open root vector, artifact inventory, and ordered open DAG |
| direct trailing-whitespace scan over the six dossier files | exit 0; no trailing whitespace |
| `git diff --check -- Stage1_Instances/THM-M-0162` | exit 0; no output |

Known downstream failures: pinpoint source inspection and independent review, exact smoothness and
sign selection, canonical Lean elaboration and mutation tests, full formal-candidate audit,
obligation expansion, proof, hermetic replay, and independent verification remain open. They
prevent theorem completion but do not invalidate this fail-closed planned intake.
