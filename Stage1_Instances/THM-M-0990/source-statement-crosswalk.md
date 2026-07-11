# Source-statement crosswalk

## Candidate primary sources

- A. M. Lyapunov, the original 1901 central-limit theorem work. A stable edition or translation,
  exact theorem location, and its original hypotheses have not yet been inspected.
- William Feller, *An Introduction to Probability Theory and Its Applications*, Volume II, second
  edition, Wiley (1971), Chapter XVI's central-limit-theorem treatment. Exact section theorem/page,
  wording, and errata remain to be checked against the edition.
- Patrick Billingsley, *Probability and Measure*, third edition, Wiley (1995), the central limit
  theorem chapter. The exact Lyapunov result/corollary location and conventions remain to be
  inspected.

These are discovery anchors, not `H0` evidence. A later phase must select a source, capture its
pinpoint statement and proof, check errata, and obtain independent review.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| triangular array | finite row of real random variables | row-indexed functions and row length | included; encoding open |
| independent | joint independence within each row | `iIndepFun` or exact finite-family equivalent | included; strength to verify |
| centered row sum | subtract expectations then sum | integral/expectation and finite sum | included |
| row variance scale | square root of summed variances | variance, nonnegativity, square root, nonzero conditions | included; edge cases open |
| Lyapunov condition | normalized sum of absolute `2 + delta` moments tends to zero | `Integrable`, `Real.rpow`, and `Tendsto` | included; exact formulation open |
| central limit conclusion | convergence to standard normal | `TendstoInDistribution` or weak convergence of pushforward laws | included; transport open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_270.lean` supplies useful API-discovery shapes for
triangular arrays, variance sums, moments, Gaussian laws, and convergence in distribution. Its
public statement requires `LyapunovHypotheses D`, which unfolds to the unconstrained proposition
field `D.characteristicFunctionTaylorBridge`. Thus it is not an exact formalization of the source
implication and supplies no proof credit. Its comments about missing upstream closure must be
re-audited at the pinned dependency revision.

Before `H0`, every source assumption and conclusion must be mapped to the final Lean binders and
definitions, including row length, centering, variance edge cases, moment existence, and the chosen
equivalence between distribution-function and weak-convergence formulations.
