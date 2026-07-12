# Statement validation record

Item: `S56-M-0319-STATEMENT`  
Base revision: `1794fae27ddcf6d19b6984502e27a9233890d8d1`

## Frozen target

`Stage1Instances.THM_M_0319.BrouwerFixedPointTarget` is the exact intake-selected ambient-map
formulation. It quantifies over every `n : Nat`, a nonempty compact convex
`K : Set (EuclideanSpace Real (Fin n))`, and an ambient `f` that is continuous on `K` and maps `K`
to itself. Its conclusion is an actual `x in K` satisfying `f x = x`. The zero-dimensional case is
included; `zeroDimensionalBoundary` checks it without adding compactness, convexity, or continuity.

The subtype self-map, closed-ball, and simplex encodings are deliberately uncredited because no
checked transport to this root has yet been supplied. This avoids silently substituting a special
case for the repository's compact-convex Euclidean wording.

## Commands and results

All Lean commands ran from `Formalizations/Lean` using the existing pinned Lake environment. The
untracked shared `.lake` link/path was present at preflight and was not modified. Evidence is scoped
and nonrelease.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0319/Statement.lean` | 0 | exact target, five mutations, and the zero-dimensional boundary proof elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0319/check_statement.py` | 0 | expression SHA-256 `2e4dc02230de7a1c08fdf4a19ef0ec1da107297972dee0e85d893bdb33d6a514`; all five mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0319/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `1b2804...440a`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0319` | 0 | rank 685, planned, L0/rework-required, theorem incomplete |

The mutations remove nonemptiness, remove the self-map condition, strengthen relative continuity
to global continuity, relocate continuity outside the map binder, and specialize arbitrary finite
dimension to three. Their explicit elaborated expressions differ from the canonical expression.

This is statement-only evidence pending master acceptance. It does not prove Brouwer's theorem or
advance anchor-audit, obligation-tree, proof, validation, or release nodes.
