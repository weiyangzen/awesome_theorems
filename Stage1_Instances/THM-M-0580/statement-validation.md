# Statement validation record

Item: `S56-M-0580-STATEMENT`  
Base revision: `9c8fbcb508ef94b14b4cc94df3d576550867591d`

## Frozen target

`Stage1Instances.THM_M_0580.PerelmanPoincareTarget` reproduces the topological
three-dimensional Poincare statement in the pinned mathlib source: for
`M : Type u`, the ordered instances are `TopologicalSpace M`, `T2Space M`,
`ChartedSpace (EuclideanSpace Real (Fin 3)) M`, `SimplyConnectedSpace M`, and
`CompactSpace M`; the conclusion is a nonempty homeomorphism from `M` to the
unit sphere in `EuclideanSpace Real (Fin 4)`.

This convention models a boundaryless topological three-manifold through
Euclidean charts. `T2Space` and `CompactSpace` express the closed convention.
`SimplyConnectedSpace` already includes the relevant nonempty/path-connected
content, so no redundant connectedness hypothesis is added. Orientability is
not inserted. `ExpandedTarget` removes only local aliases, and the checked
`perelmanPoincareTarget_iff_expandedTarget` is definitional.

The single direct import is `Mathlib.Geometry.Manifold.PoincareConjecture`, the
pinned source module whose `proof_wanted` entry supplies this exact statement
surface. The marker creates no retained proof declaration, so this node claims
statement elaboration only.

## Commands and results

Commands ran in this worker clone on 2026-07-12. Lean commands ran from
`Formalizations/Lean` using the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0580/Statement.lean` | 0 | canonical target, direct-expansion iff, and four mutations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0580/check_statement.py` | 0 | expression SHA-256 `938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`; all mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0580/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `612007...9b3`, `651c8a...1d2`, and `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115, planned, L0/rework-required, theorem incomplete |

The mutation validator distinguishes removal of `T2Space`, removal of
`CompactSpace`, changing dimension three to four, and weakening the
homeomorphism conclusion to mere nonemptiness. The smooth diffeomorphism and
generalized homotopy-sphere forms remain explicitly noncanonical alternates.

Status boundary: this is self-tested statement evidence pending master
acceptance. It does not complete the anchor audit, obligation tree, proof,
validation, release, audit-completion, or theorem-completion gates.
