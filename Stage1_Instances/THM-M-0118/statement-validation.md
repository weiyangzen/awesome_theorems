# Statement validation record

Item: `S56-M-0118-STATEMENT`  
Base revision: `25f9c9fc7ebc5af027982533c083f67f86ddfb1f`

## Frozen target

`Stage1Instances.THMM0118.NakanoVanishingTarget` freezes the vector-bundle
claim selected by intake: for a compact Kahler manifold of complex dimension
`n`, a Nakano-positive holomorphic vector bundle has
`H^q(X, Omega^p_X tensor E) = 0` for natural degrees satisfying `p + q > n`.
Vanishing is encoded as `Subsingleton` of the cohomology type, which carries an
`AddCommGroup` instance.

The sole direct import is `Mathlib.Algebra.Group.Defs`. The pinned snapshot has
no bundled analytic Kahler manifold, Nakano-positive holomorphic bundle, or
Dolbeault coefficient-cohomology API. `NakanoVanishingData` therefore types
those missing interfaces without including any vanishing conclusion. These
interfaces require checked transports when native APIs exist and receive no
proof credit here.

## Commands and results

All commands ran inside this worker clone. Lean ran from `Formalizations/Lean`
with the existing pinned Lake artifacts. No update, fetch, clone, dependency
build, or mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0118` | 0 | rank 329, planned, L0/rework-required, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0118/Statement.lean` | 0 | target, `Iff.rfl` expansion, four mutation fixtures, and explicit expression elaborated |
| `python3 ../../Stage1_Instances/THM-M-0118/check_statement.py` | 0 | expression SHA-256 `f3d6dd9891dd0197f4227d4a9091952cdb148663a2bc17a624c4bc07310bc2a5`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0118/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `f6068e...2eba`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |

## Mutations and boundary

The validator independently elaborates and serializes mutations removing
Nakano positivity, changing degree indices from naturals to integers, changing
binder scope and its dimension condition, and extending the result to the
boundary `p + q = n`. None serializes to the canonical expression. These are
structural statement-kill checks, not proofs that every altered mathematical
claim is false.

This is statement-only evidence pending master acceptance. The theorem remains
unproved and incomplete; source acceptance, anchor audit, obligation tree,
proof, full validation, and release remain open.
