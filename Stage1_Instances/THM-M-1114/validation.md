# Intake validation

Base revision: `b5a74dd6c3311423a4b689e17b549e32b41eb936`.

The preflight worktree contained the untracked reused `Formalizations/Lean/.lake` link/artifact;
this intake did not modify it. Validation is limited to repository/manifest consistency, dossier
structure, scoped intake invariants, JSON syntax, and whitespace. The source metadata does not
determine a canonical Lean proposition, so a fabricated elaboration probe would be invalid and no
kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1114` | exit 0; rank 554, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1114/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1114/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `! rg -n '[ \t]+$' Stage1_Instances/THM-M-1114` | exit 0; no trailing whitespace found |

Known downstream failures: exact primary-source inspection, canonical theorem selection, Lean
elaboration and mutation tests, anchor/provenance audit, obligation freeze, proof, hermetic replay,
and independent review remain open. They prevent statement and theorem completion but do not
invalidate this fail-closed planned intake.
