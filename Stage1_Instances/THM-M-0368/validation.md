# Intake validation

Base revision: `ded29702119d0d4880db9fcf1d0a6560a89058fd`.

This validation covers manifest membership, dossier structure, JSON integrity, a bounded pinned
mathlib name search, and a narrow Lean API probe. Because the repository record does not supply an
exact formula, no canonical target, expression hash, mutation result, or proof is claimed. The
shared canonical `.lake` symlink was used read-only and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0368` | exit 0; rank 860, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0368/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0368/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `rg -l -i 'Hardy.Littlewood|maximal function|MaximalFunction' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 1 with no matches (expected negative bounded name search) |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0368/IntakeProbe.lean)` | exit 0; all six pinned analysis API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0368` | exit 0; no output |

Known downstream failures are intentionally open: exact primary/authoritative source selection and
independent review; operator, domain, threshold, and constant freeze; canonical statement
elaboration and mutation tests; obligation and discovery freezes; complete anchor audit; proof;
hermetic replay; and release acceptance. They prevent theorem completion but do not invalidate a
truthful `planned` intake.
