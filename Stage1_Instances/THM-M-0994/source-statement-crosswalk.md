# Source-statement crosswalk

## Primary source candidate

Wassily Hoeffding, "Probability Inequalities for Sums of Bounded Random Variables," *Journal of
the American Statistical Association* 58(301), 1963, pp. 13-30, DOI
`10.1080/01621459.1963.10500830`. Theorem 2 is the intended original anchor for independent
variables with possibly unequal bounds. Exact theorem wording, equation numbering, assumptions,
and applicable errata still require inspection from a stable copy; this citation is therefore H2,
not H0.

## Crosswalk

| Source component | Frozen repository meaning | Candidate Lean component | Intake status |
|---|---|---|---|
| independent `X_i` | finite independent real random variables | `iIndepFun` restricted to a finite index set | included; encoding open |
| `a_i <= X_i <= b_i` | interval bound almost surely | `forall i, almost everywhere x, X i x in Set.Icc (a i) (b i)` | included; source transport open |
| `S - E S` | sum of coordinate-wise centered variables | finite sum of `X i x - integral (X i)` | included |
| upper-tail threshold | event `epsilon <= S - E S`, `epsilon >= 0` | real measure of a measurable event | included; measurability obligations open |
| exponential bound | `exp (-2 epsilon^2 / sum (b_i-a_i)^2)` | real exponential and finite real sum | included; proxy equivalence open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_274.lean` imports
`Mathlib.Probability.Moments.SubGaussian` and records a candidate reduction through
`ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun`. It uses the proxy
`sum ((norm (b_i-a_i))/2)^2`; the later statement and anchor nodes must check its exact type,
algebraic equivalence, assumptions, degenerate behavior, imports, axioms, and proof provenance at
the pinned revision. The file receives no accepted rev-5.6 credit from this intake.

Before H0, an independent reviewer must verify the source scan, Theorem 2 and surrounding
definitions, all hypotheses, normalization from Hoeffding's `n t` notation to `epsilon`, and errata,
then approve the row-by-row source-to-Lean mapping.
