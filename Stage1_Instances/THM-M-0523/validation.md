# Intake validation

Base revision: `e3d0fd205c9c81486cb86f68cdc66d4d4e5bb264`.

This validation covers manifest membership, dossier structure, JSON integrity, source-conflict
discovery, and a narrow pinned Lean API probe. Because the repository wording conflicts with the
named theorem, no canonical target, expression hash, mutation result, or proof is claimed. The
pre-existing canonical `.lake` symlink was used read-only; no update, build, clone, or fetch ran.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0523` | exit 0; rank 895, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0523/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0523/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0523/IntakeProbe.lean)` | exit 0; six pinned cusp API checks elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0523 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0523` | exit 0; no output |

Known downstream failures are intentionally open: primary-source pinpointing and independent
review, adjudication of the Heegner/cusp conflict, canonical statement elaboration and mutations,
obligation/discovery freezes, anchor audit, proof, hermetic replay, and release acceptance. They
prevent theorem completion but do not invalidate this truthful `planned` intake.
