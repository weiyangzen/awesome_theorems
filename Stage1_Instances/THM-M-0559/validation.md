# Intake validation

Base revision: `418e6ea60487eaae4d9a1fa7aeb4bb7c575c33ee`.

Validation is intentionally limited to target/standard consistency, dossier structure, pinned API
availability, forbidden proof-token hygiene, and whitespace. `Formalizations/Lean/.lake` is the
automation clone's pre-existing symlink to the canonical pinned artifacts; no dependency update,
fetch, build, or mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0559` | exit 0; rank 607, planned, L0/rework_required, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0559/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0559/task-dag.json` | exit 0 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0559/IntakeSurface.lean` | exit 0; `Topology.CWComplex`, `HomotopyGroup.Pi`, `ContinuousMap.HomotopyEquiv`, and `ContinuousMap` elaborated under Lean 4.29.0 |
| forbidden proof-token scan over owned Lean sources | exit 0; no proof escape or assumed declaration |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0559` | exit 0; no output |

The first downstream gate remains the exact statement. In particular, API existence does not
establish the component map, functorial induced maps on `HomotopyGroup.Pi`, or Whitehead's theorem.
Primary theorem/page and errata inspection, source review, statement mutation tests, formal-anchor
audit, obligation registry, proof, hermetic replay, and independent validation all remain open.
