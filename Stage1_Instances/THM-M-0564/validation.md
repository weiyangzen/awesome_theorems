# Intake validation

Base revision: `07cadbebc45abaef80eaced8be5323f71613c97a`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, the
bounded repository/source search recorded in the crosswalk, and whitespace. The source wording is
not a proposition, so no fabricated Lean elaboration or kernel-proof result is claimed. The
pre-existing `Formalizations/Lean/.lake` symlink is unrelated worker-clone infrastructure and was
not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0564` | exit 0; rank 612, L0/rework_required, planned, theorem_complete false |
| `rg -n 'characteristic class\|CharacteristicClass\|Stiefel\|ChernClass\|Pontryagin\|示性类' Formalizations Stage1_Instances Docs --glob '*.lean' --glob '*.md' --glob '*.json'` | exit 0; source metadata and generic dependency/blocker mentions found; no `THM-M-0564` Lean artifact found |
| `find Formalizations/Lean/.lake/packages/mathlib/Mathlib -type f \( -iname '*Characteristic*' -o -iname '*Chern*' -o -iname '*Stiefel*' -o -iname '*VectorBundle*' \)` | exit 0; only characteristic-function and Euler-characteristic filenames found |
| `python3 -m json.tool Stage1_Instances/THM-M-0564/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0564/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0564` | exit 0; no output |

Known downstream failures: the source phrase must be corrected to a single source-located
proposition; primary-source and independent review, canonical Lean elaboration, anchor audit,
obligation registry, proof, hermetic replay, and release validation remain open. These failures
prevent theorem completion but do not invalidate this fail-closed planned intake.
