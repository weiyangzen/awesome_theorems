# Statement validation record

Item: `S56-M-0166-STATEMENT`  
Base revision: `ae68d10d70accbf26b8c8c53097b02a2ae2fa561`

## Frozen target

`Stage1Instances.THM_M_0166.HopfRinowStatement` is the intake-selected forward Hopf-Rinow claim.
The conclusion uses the intrinsic characterization of a minimizing geodesic: a smooth path on
`[0, 1]` whose every ordered subsegment has `pathELength` equal to `riemannianEDist`. This is not a
proxy predicate. It is used because the pinned mathlib revision exposes Riemannian path length and
distance but no native connection-based geodesic predicate.

The sole direct import is `Mathlib.Geometry.Manifold.Riemannian.Basic`. The explicit hypotheses
freeze finite dimension, infinite smoothness, absence of boundary, the Riemannian metric/distance
compatibility, connectedness, and metric completeness. No theorem proof is present.

## Commands and results

All Lean commands ran from `Formalizations/Lean` in this worker clone using existing pinned Lake
artifacts.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0166/Statement.lean` | 0 | canonical target and four mutation declarations elaborated; universe-explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0166/check_statement.py` | 0 | expression SHA-256 `8965e82e10defac0d0e33b119fb5a4e48e93cee58029fe3d55e9af3d2f97da55`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0166/Statement.lean lean-toolchain lake-manifest.json` | 0 | `aea289...f70b`, `651c8a...b1d2`, `321626...d81` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

## Mutation and boundary policy

The validator separately elaborates and distinguishes removal of completeness, removal of
connectedness, weakening to an arbitrary smooth path, and moving both endpoint binders under one
existential path. The target quantifies over all endpoint pairs, so `p = q` is included. Empty
manifolds are vacuous; singleton and zero-dimensional connected manifolds are not excluded.

This is statement-only evidence pending master acceptance. It does not advance anchor-audit,
obligation-tree, proof, validation, release, or theorem-completion state.
