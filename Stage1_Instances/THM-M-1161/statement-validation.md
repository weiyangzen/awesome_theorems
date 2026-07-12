# Statement validation record

Item: `S56-M-1161-STATEMENT`. Base revision:
`767bcb5c33375def04fc8f536c5a5e3f27c31aa0`.

The canonical proposition is a `def ... : Prop`, not a theorem carrying a proof. This is deliberate:
the statement phase checks elaboration without introducing any unproved declaration or proof term.
The integral equation is present pointwise in `Solves`; `operator_eq_integral` fixes its relation to
the compact operator, and the adjoint compatibility branch is retained.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1161/FredholmIntegralEquationStatement.lean` | 0 | Lean elaborated the file and printed the fully qualified canonical declaration with result `Prop` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, matching `lakefile.lean` |
| `sha256sum Stage1_Instances/THM-M-1161/FredholmIntegralEquationStatement.lean` | 0 | `221cf8a4ecd3534978bf7ce0c7330921bd7a492d6dd6daba1db2d55be8482985` |

No proof or downstream completion is claimed. Minimality here means each direct import supplies a
distinct statement surface: adjoints, the pinned compact/Fredholm operator vocabulary, and Bochner
integration. Master acceptance remains required.
