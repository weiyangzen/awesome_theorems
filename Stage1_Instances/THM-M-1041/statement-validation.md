# Statement validation record

Item: `S56-M-1041-STATEMENT`  
Base revision: `26d86e8061117f2975b8278f35ca3b2aac5e0efb`

## Frozen target

`Stage1Instances.THM_M_1041.HilleYosidaContractionTarget` selects the real Banach-space,
contraction-semigroup form of Hille-Yosida. The generator is a `LinearPMap`; its graph is defined
by the strong right derivative of a nonnegative-time family. The resolvent clause concretely gives
both inverse equations for `a I - A` and the pointwise bound `||R y|| <= a^-1 ||y||` for every
`a > 0`. No mathematical condition is stored in an opaque proposition field.

The two direct imports are the narrow pinned modules needed for `LinearPMap`, topology, nonnegative
reals, and continuous linear maps. `target_iff_expanded` checks an alternate parenthesization by
definitional equality. The source relationship is intentionally bounded: the selected formula is
the standard contraction form identified with Engel-Nagel, Chapter II, Theorem 3.5, while exact
primary-source pagination and errata review remain downstream H-status work.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` using the
existing pinned `.lake` artifacts; no dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1041/Statement.lean` | 0 | target, concrete component definitions, checked transport, and three mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1041/check_statement.py` | 0 | expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1041/Statement.lean lean-toolchain lake-manifest.json` | 0 | `4e211b...14699`, `651c8a...1d2`, `321626...2d81` |

This is statement-only evidence pending master acceptance. It does not prove Hille-Yosida or
advance the anchor-audit, obligation-tree, proof, validation, or release nodes.
