# Statement validation record

Item: `S56-M-0995-STATEMENT`  
Base revision: `8d7cfb9e267efd34427f29cb4d7103282a0d0942`

## Frozen target

`Stage1Instances.THM_M_0995.StatementShape` is the exact bounded-summand, one-sided upper-tail
claim selected by intake. The probability measure, finite range, real summands, nonnegative common
bound and variance budget, measurability, square integrability, mutual independence, centering,
almost-sure absolute bound, variance-sum bound, and nonnegative threshold are explicit.

The sole direct import is `Mathlib.Probability.Moments.Variance`.
`statementShape_iff_expandedSourceShape` kernel-checks the direct quantified expansion. The
historical Stage1 module is not imported and contributes no proof credit.

## Commands and results

Lean commands ran from `Formalizations/Lean` using the existing pinned Lake environment. No Lake
dependency was fetched or modified.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0995/Statement.lean` | 0 | target, checked expansion, four mutations, and three boundary lemmas elaborated; explicit target printed |
| `python3 Stage1_Instances/THM-M-0995/check_statement.py` | 0 | expression SHA-256 `0201bd579e5b8f490d8079891aec8d7e8b4d69c1534a18a9e6bc77e464faafa2`; all four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0995/Statement.lean Stage1_Instances/THM-M-0995/check_statement.py Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match `statement.json`; pinned mathlib revision is `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and distinguishes removal of almost-sure
boundedness, replacement of real variables by integer variables, movement of the threshold outside
the problem binders, and exclusion of `t = 0`. Kernel-checked lemmas exercise `t = 0`, simultaneous
`v = b = 0`, and `n = 0`. The zero-denominator behavior is intentionally the behavior of Lean's
totalized real division; it is not silently excluded.

This is self-tested statement evidence pending master acceptance. It does not prove Bernstein's
inequality or advance the anchor-audit, obligation-tree, proof, validation, or release nodes.
