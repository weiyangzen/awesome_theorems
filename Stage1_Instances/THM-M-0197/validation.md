# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`.
Base tree: `829a47c47ae831cada4f8acc6c2c00ba5883215e`.

Validation covers target membership, the planned dossier and open DAG, exact repository wording,
source-boundary consistency, JSON integrity, file hygiene, and a narrow pinned Lean API probe. The
automation-provided canonical `.lake` symlink was present before this work and was used read-only.
No dependency update, build, clone, fetch, or `.lake` mutation was performed. This dirty worker run
is explicitly nonrelease evidence.

The modern source lead was downloaded only to inspect and hash its versioned statement surface. It
is not admitted as an accepted primary source, proof, or dependency. The subsequent structured
validation recipes denied network access and used only the already pinned Lean artifacts.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `check_stage1_standard: ok` with 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0197` | exit 0; rank 1015, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` before editing | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree recorded above |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0197/IntakeProbe.lean)` | exit 0; eight generic distance, convex-hull, Euclidean-angle, and minimum interfaces elaborated; no canonical target declared |
| bounded exact-name search for Fermat point, Fermat-Torricelli, Torricelli point, or geometric median | exit 1 (expected no-match); no target-specific declaration found in pinned mathlib or repository-local Lean sources |
| `python3 -B Stage1_Instances/THM-M-0197/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; planned H5/M4/R4 intake invariants, fingerprints, receipt, file hygiene, and six open tasks agree |
| prohibited-construct scan over owned Lean files | exit 1 (expected no-match); no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parsing for `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 for each |
| scoped Git and per-new-file no-index whitespace checks | exit 0 for whitespace validation; no trailing-space diagnostics |

## Status boundary

The intake deliverable is self-tested, but every dependent phase remains open. The first downstream
failure is exact source statement identity: strict versus closed interior, ambient and comparison
domains, triangle nondegeneracy, existence and uniqueness, and both sides of the 120-degree split
are unresolved. Canonical elaboration and mutation tests, source acceptance, anchor audit,
obligation registry, proof, trust closure, hermetic replay, independent verification, and master
acceptance have not occurred. Consequently `audit_complete` and `theorem_complete` remain false,
and no accepted receipt or proof body is reported.
