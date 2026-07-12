# Intake validation

Base revision: `ed278d07d4b1fbd48887625b78d32141bebc9441`.

Validation covers target-set membership, dossier structure, JSON integrity, scoped invariants, and a
narrow pinned Lean API probe. The canonical 21-component proposition is still open, so this record
does not claim statement elaboration, a target hash, mutation testing, proof closure, or release
evidence. The worker reused the canonical `.lake` artifacts read-only and ran no update, build,
clone, or fetch.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0722` | exit 0; rank 759, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0722/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0722/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0722/IntakeProbe.lean)` | exit 0; six API types elaborated under pinned Lean/mathlib |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0722 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0722` | exit 0; no output |

Known downstream failures are intentionally open: independent source review and errata audit, exact
problem inventory and encodings, canonical statement elaboration and mutation tests, obligation and
discovery freezes, formal-anchor audit, all 21 proof branches, hermetic replay, and release review.
They prevent theorem completion but do not invalidate a truthful planned intake.
