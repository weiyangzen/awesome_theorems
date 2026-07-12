# Intake validation

Base revision: `7c8a8597055a5d4012e43f6e2f6727d1a8632aa5`.

Validation is limited to manifest consistency, dossier structure and fail-closed invariants, and a
narrow Lean vocabulary probe. `Formalizations/Lean/.lake` was already untracked in the worker clone
before this intake; the pinned artifacts were reused without update, build, fetch, or other
mutation. This is nonrelease evidence. No canonical Lean expression or proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0321` | exit 0; rank 687, L0/rework_required, planned, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0321/IntakeProbe.lean)` | exit 0; pinned Lean 4 elaborated `IsCompact`, `Convex`, `LocallyConvexSpace`, `ContinuousAffineMap`, and the two type-level probes |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0321/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0321` | exit 0; no output |

The first attempt to encode maps directly on the subtype `K` failed because an arbitrary convex
subset subtype does not inherit an `AddTorsor`, which `ContinuousAffineMap` requires. The probe was
corrected to the honest ambient-map-plus-`MapsTo` candidate encoding and then passed. This is useful
statement-phase evidence, not a hidden proof or broadened target.

Known downstream failures are the uninspected exact primary statement and errata, canonical Lean
expression and fingerprint, immutable candidate audit, obligation registry, proof, trust closure,
hermetic replay, and independent review. They prevent audit and theorem completion but do not
invalidate this self-tested `planned` intake.
