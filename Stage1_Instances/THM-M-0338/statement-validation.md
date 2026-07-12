# Statement validation record

Item: `S56-M-0338-STATEMENT`  
Base revision: `230f719da7724afb27c761dcb8c62a327557fe63`

## Frozen target

`Stage1.THM_M_0338.KadisonSingerStatement` formalizes the affirmative Kadison-Singer assertion.
The domain is a complex Hilbert space equipped with a `Nat`-indexed Hilbert basis. The diagonal
star subalgebra is characterized exactly by vanishing off-diagonal matrix coefficients. A state is
a positive complex-linear functional normalized at one; purity is the extreme-point condition.
The conclusion is existence and uniqueness among all state extensions to the bounded operators.

This resolves the intake encoding choices without substituting an equivalent paving or discrepancy
claim. The module defines no theorem asserting the target, and provides no proof credit.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned Lake environment. No
update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0338/Statement.lean` | 0 | state, purity, exact diagonal characterization, target, and four mutations elaborated; canonical expression printed |
| `python3 ../../Stage1_Instances/THM-M-0338/check_statement.py` | 0 | expression SHA-256 `c0c479c898a7b418bd4d82ad05d7514edfcc885cfd9a5487fb1a4ac5ffc37868`; all four mutations distinguished |
| `lake env lean --version` (from `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0338/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `6619fde2...ad12`, `651c8acc...b1d2`, `321626c8...b2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0338` | 0 | rank 831, planned, historical artifacts unaccepted, theorem incomplete |

## Mutation policy

The validator compares elaborated printed expressions. It distinguishes removal of purity,
replacement of the countably infinite basis by `Fin 2`, existential rather than universal scope
for the diagonal algebra, and uniqueness only among pure extensions. Thus the infinite domain,
binder scope, purity premise, and extension class are frozen rather than left implicit.

This is statement-only evidence pending master acceptance. Anchor audit, obligation tree, proof,
validation, release, audit completion, and theorem completion all remain open.
