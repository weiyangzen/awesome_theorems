# Intake validation

Base revision: `44b9849ef3fd618f97e63d42e60134771f7302b9`.

Validation is deliberately limited to target membership, dossier structure, intake invariants,
pinned toolchain availability, JSON syntax, and whitespace. No canonical Lean expression has been
selected, so the Lean invocation below is an environment check only and grants no statement or
proof credit. The reused `Formalizations/Lean/.lake` path is untracked in this worker clone; it was
not created or modified by this intake and makes this nonrelease evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0161` | exit 0; rank 660, L0/rework_required, planned, theorem_complete false |
| `git status --short` | exit 0; pre-existing `?? Formalizations/Lean/.lake` recorded before edits |
| `git rev-parse HEAD` | exit 0; `44b9849ef3fd618f97e63d42e60134771f7302b9` |
| `cd Formalizations/Lean && lake env lean --version` | exit 0; Lean version 4.29.0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0161/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0161/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0161` | exit 0; no output |

Known downstream failures are intentionally open: primary-source pinpoint inspection and independent
review; exact regularity and orientation conventions; canonical Lean statement and mutation tests;
formal-anchor audit; obligation registry and typed graphs; proof; hermetic/offline validation; and
independent release verification. They prevent audit and theorem completion but do not invalidate
this fail-closed `planned` intake.
