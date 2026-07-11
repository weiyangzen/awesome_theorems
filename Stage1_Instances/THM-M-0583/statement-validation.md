# Statement validation record

Item: `S56-M-0583-STATEMENT`  
Base revision: `621e4c254d9e0dc9b50a60e66930c9f43601b890`

## Frozen target

`Stage1Instances.THM_M_0583.FourDimensionalTopologicalPoincareTarget` quantifies over every
Hausdorff compact boundaryless topological four-manifold encoded by a `ChartedSpace` over
`EuclideanSpace Real (Fin 4)`. Given an unpointed homotopy equivalence to the unit sphere in
`EuclideanSpace Real (Fin 5)`, it concludes that a homeomorphism to that sphere exists. It does not
state the unresolved smooth analogue.

The sole direct import is `Mathlib.Geometry.Manifold.PoincareConjecture`, the pinned defining module
for precisely this generalized statement object model. The local target adds the explicit
`CompactSpace` closedness condition and fixes `n = 4`. An `Iff.rfl` wrapper checks the fully expanded
encoding. No proof-wanted declaration is invoked or credited.

## Commands and results

All commands ran inside this worker clone. Lean used the existing canonical pinned `.lake` symlink;
no update, build, fetch, clone, or dependency mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0583/Statement.lean` | 0 | target, checked expansion, and four structural mutations elaborated; fully explicit target printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0583/check_statement.py` | 0 | expression SHA-256 `8ba8ef3cba0ad739c717ad8f42d40c221ff7a2cdcf79f7098709a60bd7a7ebce`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0583/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `ce7668...c6d8`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0583` | 0 | rank 116, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0583/instance.json` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0583/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0583` | 0 | no output |

## Mutation and status boundary

The validator compares fully explicit elaborated expressions. It distinguishes removal of the
homotopy-equivalence premise, changing dimension four to dimension three, changing the universal
manifold binder to an existential binder, and removing compactness. These are statement-identity
tests, not claims that every mutated proposition has been refuted in Lean.

This is statement-only evidence pending master acceptance. Primary-source wording and errata still
need the later human-source audit. Anchor audit, proof architecture, proof closure, H0, M0, hermetic
release replay, independent validation, audit completion, and theorem completion remain open.
