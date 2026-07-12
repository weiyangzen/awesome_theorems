# Intake validation

Base revision: `c72bad9e8827ffb1ba1a585dbe346c88393b4a3f`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. It does not validate a canonical statement or proof. The worktree began with the
shared `Formalizations/Lean/.lake` symlink shown as untracked; it points to the canonical pinned
artifacts and was used read-only. No Lake update, build, fetch, or dependency mutation was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0781` | exit 0; rank 786, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0781/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0781/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0781/IntakeProbe.lean)` | exit 0; seven pinned logic/set-theory API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0781` | exit 0; no output |

The initial probe used `Mathlib.SetTheory.ZFC.Basic` and failed because `ZFSet.choice` is exposed by
`Mathlib.SetTheory.ZFC.Class`; changing only that probe import produced the successful recorded run.
This was an intake API-discovery failure, not suppressed evidence.

Known downstream failures are intentionally open: independently reviewed primary sources and
attribution split; an encoded object theory and exact four-part statement; statement fingerprint
and mutation tests; discovery and obligation freezes; candidate/provenance audit; proof;
composition/trust checks; hermetic and independent reproduction; and release acceptance. They
prevent theorem completion but do not invalidate a truthful `planned` intake.
