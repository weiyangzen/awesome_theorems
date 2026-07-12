# Statement validation record

Item: `S56-M-1065-STATEMENT`  
Base revision: `205d13cfc35c45883410c569709a91cb34edce16`

## Frozen target

`Stage1Instances.THM_M_1065.KMTStrongApproximationTarget` freezes the normalized partial-sum KMT
claim selected by intake. The input is a probability law on `Real` with integrable first and second
moments, mean zero, second moment one, and a two-sided exponential moment. The output is one
probability space carrying iid increments with that law and iid `N(0,1)` increments.

Positive constants `C`, `K`, and `lambda` may depend on the input law but precede `n` and `x`. For
every `n >= 1` and `x >= 0`, the probability that some partial-sum discrepancy through time `n`
exceeds `C * log n + x` is bounded by `K * exp (-lambda * x)`. The sole direct import is
`Mathlib.Probability.Distributions.Gaussian.Real`.

The full direct expansion is kernel-equivalent by `target_iff_expandedSourceShape`. Four mutations
are distinguished from the printed canonical expression: removed exponential-moment assumptions,
changed value domain, terminal-time-only error, and a changed positive-time binder. The boundary
theorem `discrepancyEvent_one` checks the `n = 1` convention.

## Commands and results

Commands used only the existing pinned Lake environment; dependency state was not changed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1065/Statement.lean` | 0 | target, expansion, checked iff, mutations, boundary theorem, and explicit print elaborated |
| `python3 Stage1_Instances/THM-M-1065/check_statement.py` | 0 | four mutations killed; expression SHA-256 `b257ceb1...cebd0`; pinned mathlib revision reported |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-1065/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | statement `7f3b249e...edaf1`; toolchain `651c8acc...b1d2`; manifest `321626c8...2d81` |

## Status boundary

This is self-tested statement evidence pending master acceptance. Primary-source theorem/page and
errata review remains open for the anchor-audit node. No proof of KMT, source acceptance, M0, audit
completion, or theorem completion is claimed.
