# Statement validation record

Item: `S56-M-1235-STATEMENT`  
Base revision: `4fbe3ce993b660eb9a4da0d9139eb8b6f66878d0`

## Frozen target

`Stage1Instances.THMM1235.WolibnerGlobalExistenceAndUniqueness` freezes the result stated in
Wolibner's 1933 paper, pages 698-700, together with its uniqueness section on pages 725-726. The
source considers a closed planar region, bounded or exterior, whose frontier is a finite union of
closed analytic curves. Given integrable vorticity with the source decay and Holder hypotheses,
zero circulation on interior boundary components, potential force, positive density, and pressure
normalization, it constructs for every finite `T > 0` the five functions satisfying conditions
`(I)`-`(VIII)` on `0 <= t <= T`; section 5 gives uniqueness.

The sole direct import is `Mathlib.Data.Real.Basic`. The pinned library has no source-matching
classical Euler or analytic-boundary API. Conditions `(I)`-`(VIII)` are consequently named `Prop`
fields in a typed `Motion` structure. They assume neither existence nor uniqueness. This retains
the historical theorem rather than substituting the legacy whole-plane, bounded-vorticity model.
Later expansion of those fields needs checked transports and receives no proof credit here.

## Commands and results

All commands ran inside this worker clone. Lean used the existing pinned Lake environment; no
dependency was fetched, updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1235` | 0 | rank 159, planned, L0/rework-required, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-1235/Statement.lean` from `Formalizations/Lean` | 0 | exact target, `Iff.rfl` expansion, four mutation fixtures, and explicit expression elaborated |
| `python3 ../../Stage1_Instances/THM-M-1235/check_statement.py` from `Formalizations/Lean` | 0 | expression SHA-256 `77aec2...3c23`; all four mutations distinguished |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-1235/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `e59d7e...1697`, `651c8a...b1d2`, and `321626...2d81` |

## Mutation and boundary record

The validator separately elaborates mutations that remove Holder continuity, substitute the whole
plane for the source domain, move the finite terminal-time binder outside the data quantifier, and
admit `T = 0`. None serializes to the canonical expression. These are structural statement-kill
checks, not proofs that the mutated propositions are mathematically false.

The stable primary scan inspected for statement identification is GDZ volume
`PPN266833020_0037`, article `LOG_0069`; DOI `10.1007/BF01474610`. No scan was copied into the
repository. Full source-proof and errata acceptance belongs to the later audit node.

This is statement-only evidence pending master acceptance. The theorem remains unproved and
incomplete; anchor audit, obligation tree, proof, full validation, and release remain open.
