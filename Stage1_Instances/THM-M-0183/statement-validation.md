# Statement validation record

Item: `S56-M-0183-STATEMENT`  
Base revision: `2386f0c7fd499f33644e2df01ca29eecfd54c055`

## Frozen target

`Stage1Instances.THMM0183.YauCalabiConjectureTarget` freezes the intake-selected Ricci-flat
corollary: on a compact smooth complex Kahler manifold with vanishing real first Chern class, every
prescribed Kahler class contains a compatible Kahler metric with zero Ricci tensor. The only direct
import is `Mathlib.Geometry.Manifold.Complex`.

The pinned snapshot lacks native analytic Kahler metric, real first Chern class, Kahler-class, and
Ricci-tensor APIs. `CalabiYauDomain` and `KahlerMetricInterface` expose those notions as typed
interfaces, but no field assumes existence of the desired metric. The exact existential remains the
target. Future native definitions require checked transports and receive no credit here.

## Commands and results

All commands ran in this worker clone on 2026-07-12. Lean ran from `Formalizations/Lean` using the
existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0183/Statement.lean` | 0 | target, checked source-shape identity, and four mutations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0183/check_statement.py` | 0 | expression SHA-256 `f6f6506ce1ecc2a33f7c56a3a3ea97ac0271eeeb619d421e1e8f97f61cd08478`; all mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0183/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `38816c...6c25`, `651c8a...1d2`, and `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0183` | 0 | rank 130, planned, L0/rework-required, theorem incomplete |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and distinguishes removal of compactness,
removal of real-first-Chern-class vanishing, replacement of every prescribed class by some class,
and weakening to an unspecified Ricci-flat metric. No positive-dimension, connectedness,
nonemptiness, or boundarylessness restriction is silently inserted.

This is statement-only evidence pending master acceptance. It does not prove Yau's theorem or
advance anchor-audit, obligation-tree, proof, validation, or release nodes.
