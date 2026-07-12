# Statement validation record

Item: `S56-M-0330-STATEMENT`  
Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`

## Frozen target

`Stage1Instances.THM_M_0330.HilleYosidaContractionTarget` selects the real Banach-space,
contraction-semigroup form of Hille-Yosida. The generator is a `LinearPMap`; its graph is defined
by the strong right derivative of a nonnegative-time family. The resolvent clause concretely gives
both inverse equations for `a I - A` and the pointwise bound `||R y|| <= a^-1 ||y||` for every
`a > 0`. No mathematical condition is stored in an opaque proposition field.

The two direct imports are the narrow pinned modules needed for `LinearPMap`, topology, nonnegative
reals, and continuous linear maps. `target_iff_expanded` checks an alternate parenthesization by
definitional equality. The selected formula is the standard contraction form associated with
Engel-Nagel, Chapter II, Theorem 3.5; exact primary-source and errata review remains downstream.

## Commands and results

Lean commands used the existing pinned `.lake` artifacts; no dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0330/Statement.lean` | 0 | target, concrete definitions, checked transport, and mutations elaborated; explicit expression printed |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 0 | expression SHA-256 `5696285042abd39e340c7e72b2c2855d17e2e335106b1aa6a724056fd68bd75e`; three mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0330/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | statement `48028e...d650`, toolchain `651c8a...1d2`, manifest `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target baseline valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all uniform L0 |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | rank 823, correct lane, planned, theorem_complete false |

This is statement-only evidence pending master acceptance. It does not prove Hille-Yosida or
advance the anchor-audit, obligation-tree, proof, validation, or release nodes.
