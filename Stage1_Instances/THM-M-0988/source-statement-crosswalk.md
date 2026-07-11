# Source-statement crosswalk

## Candidate primary sources

- J. W. Lindeberg, "Eine neue Herleitung des Exponentialgesetzes in der
  Wahrscheinlichkeitsrechnung", *Mathematische Zeitschrift* 15 (1922), 211-225. This is a
  historical source candidate; the exact iid specialization, assumptions, and page must be
  inspected rather than inferred from the modern theorem name.
- P. Levy, *Calcul des probabilites* (1925), central-limit discussion. Exact edition, theorem/page,
  notation, and available errata remain to be established.

These are discovery anchors, not `H0` evidence. A stable modern source may be added for readable
assumption matching, but it cannot replace inspection of the selected primary statement.

## Crosswalk

| Human component | Intended mathematics | Candidate Lean component | Intake status |
|---|---|---|---|
| iid real variables | common real law and mutual independence | `IdentDistrib`, `iIndepFun` | included; exact binders open |
| finite variance | finite second moment of one summand | `MemLp (X 0) 2 P`, `variance` | included; equivalence audit open |
| centered sums | `sum X_k - n E[X_0]` | finite sum and integral | included |
| square-root scaling | multiplication by `(sqrt n)⁻¹` | `Real.sqrt`, inverse | included; zero-index convention open |
| Gaussian limit | mean zero, common variance | `gaussianReal 0 (variance ...).toNNReal` | included; degenerate case open |
| convergence in law | weak convergence of distributions | `TendstoInDistribution` | included; exact measure arguments open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_268.lean` imports
`Mathlib.Probability.CentralLimitTheorem` and records the candidate declaration
`ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub`. It is valuable discovery evidence,
not accepted rev-5.6 evidence: the statement phase must elaborate and fingerprint the exact target,
and anchor audit must independently verify the pinned revision, complete type, proof provenance,
axioms, dependency feasibility, and correspondence to the selected source.

Before `H0`, an independent reviewer must verify edition, theorem/page, assumptions, definitions,
normalization, zero-variance behavior, and errata, then approve every crosswalk row.
