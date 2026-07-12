# Intake validation

Base revision: `91055abb3f5bee7f79323bc9cbefa7f2a8145f1f`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean discovery probe. It does not claim canonical statement acceptance, source acceptance, theorem
proof, or any downstream gate. The worker's `Formalizations/Lean/.lake` is an existing symlink to
the canonical pinned artifacts and was used read-only; no dependency update or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0768` | exit 0; rank 778, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0768/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0768/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0768/IntakeProbe.lean)` | exit 0; all three pinned declarations and the proposition-only crosswalk spelling elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0768` | exit 0; no output |

Known downstream failures are intentionally open: primary-source acceptance and independent
review, canonical declaration and mutation tests, obligation/discovery freezes, formal anchor and
proof-body audit, proof credit, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate a truthful `planned` intake.
