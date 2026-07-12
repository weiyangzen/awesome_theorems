# Intake validation

Base revision: `18efc1c7be6d7f37ac4e26f3ee773eae861c42f0`.

The preflight worktree contained the automation-provided untracked symlink
`Formalizations/Lean/.lake` to the canonical pinned artifacts; it was not modified. Validation is
limited to manifest consistency, dossier structure, scoped intake invariants, the pinned API probe,
and whitespace. The probe checks declarations only and supplies no canonical theorem proof.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0540` | exit 0; rank 597, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0540/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0540/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0540/IntakeProbe.lean)` | exit 0; all three pinned mathlib declarations elaborated with their full types |
| `rg -n '\b(sorry\|admit\|axiom)\b' Stage1_Instances/THM-M-0540 --glob '*.lean'` with failure on a match | exit 0; no forbidden Lean token found |
| `git diff --check -- Stage1_Instances/THM-M-0540` | exit 0; no output |

## Status boundary

Known downstream failures are the ambiguous theorem-shaped source proposition, pinpoint source and
errata review, exact coefficient and universe conventions, canonical Lean elaboration and mutation
tests, obligation registry, terminal-body audit, proof, hermetic replay, and independent review.
They prevent audit and theorem completion but do not invalidate a fail-closed planned intake.
