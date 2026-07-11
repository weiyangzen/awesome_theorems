# Statement validation record

Item: `S56-M-0586-STATEMENT`  
Base revision: `621e4c254d9e0dc9b50a60e66930c9f43601b890`

## Frozen target

`Stage1Instances.THMM0586.HighDimensionalPoincareTarget` is the exact target selected by the
accepted intake boundary: for each natural `n >= 5`, a compact Hausdorff smooth manifold charted
by boundaryless Euclidean `n`-space and homotopy equivalent to the unit `n`-sphere is homeomorphic
to that sphere. Its sole direct import is `Mathlib.Geometry.Manifold.PoincareConjecture`.

The checked implication
`generalizedTopologicalTarget_implies_highDimensionalTarget` relates mathlib's broader generalized
topological statement shape to this root. It does not reverse the implication, turn mathlib's
`proof_wanted` source marker into a constant, or prove either theorem. Exact primary-source
theorem/page/errata review remains open, so human-source status remains `H2`.

## Commands and results

Lean commands ran from `Formalizations/Lean` using the existing pinned `.lake` artifacts. No
dependency update, fetch, build, or cache mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0586/Statement.lean` | 0 | target, implication transport, four mutations, and dimension-five boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0586/check_statement.py` | 0 | expression SHA-256 `48062820803a28b54a2bcf9b1122a10ce4d4b53b1d9e37e5f0c8b119955346e7`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0586/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `326186...b49`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | rank 117, planned, L0/rework-required, theorem incomplete |

## Mutation and boundary policy

The validator compares serialized explicit elaborated expressions. It distinguishes removal of
smoothness, replacement of the unbounded natural dimension by `Fin 100`, existential instead of
universal dimension scope, and replacement of `5 <= n` by `6 <= n`. The kernel-checked sphere
self-homeomorphism exercises the included `n = 5` boundary without assuming the target.

This is statement-only evidence pending master acceptance. It advances neither proof nor theorem
completion and supplies no evidence for anchor-audit, obligation-tree, proof, validation, or
release nodes.
