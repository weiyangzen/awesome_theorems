# Statement validation record

Item: `S56-M-0318-STATEMENT`  
Base revision: `7c8a8597055a5d4012e43f6e2f6727d1a8632aa5`

## Frozen target

`Stage1Instances.THM_M_0318.SchauderFixedPointTarget` is the compact-convex claim selected by the
accepted intake dependency: an arbitrary real normed vector space, a nonempty compact convex set,
and a map continuous on and preserving that set. The conclusion is a fixed point belonging to the
set. Completeness of the ambient space, global continuity, finite dimensionality, contraction, and
uniqueness are deliberately absent.

The minimal direct imports are `Mathlib.Analysis.Normed.Module.Basic` and
`Mathlib.Analysis.Convex.Basic`. Removing either loses a required identifier. A separately tested
`Mathlib.Topology.Basic` import was redundant and removed. `target_iff_expanded` kernel-checks the
API spelling against a direct binder-level expansion. This is statement identity, not proof credit.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. Lean ran from `Formalizations/Lean` against the
existing pinned `.lake` artifacts. No update, fetch, clone, or dependency build was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0318/Statement.lean` | 0 | canonical target, checked expansion, four mutations, and two boundary lemmas elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0318/check_statement.py` | 0 | expression SHA-256 `2605ac76...56b5f`; all four structural mutations distinguished; file SHA-256 `e428904e...2912d` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0318/Statement.lean lean-toolchain lake-manifest.json` | 0 | `e428904e...2912d`, `651c8acc...b1d2`, `321626c8...5cb2d81` |
| import-removal trials using temporary files under `/tmp` | 0 as a test harness | removing either retained import made elaboration fail; removing `Mathlib.Topology.Basic` still passed, so it was removed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0318` | 0 | rank 684, planned, theorem completion false |
| `git diff --check -- Stage1_Instances/THM-M-0318 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and status boundary

The validator rejects removal of compactness, specialization of the arbitrary ambient space to
`Real`, relocation of the fixed-point witness outside the map binder, and removal of the self-map
hypothesis. Kernel-checked lemmas exercise exclusion of the empty set and inclusion of the
singleton case.

This is self-tested statement elaboration pending master acceptance. The primary-source
theorem/page/terminology crosswalk remains `H2` and belongs to anchor/source audit. No Schauder
proof, `H0`, audit completion, or theorem completion is claimed.
