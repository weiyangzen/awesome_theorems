# Source-statement crosswalk

## Primary source candidate

Antonio Ambrosetti and Paul H. Rabinowitz, "Dual variational methods in critical point theory and
applications," *Journal of Functional Analysis* 14 (1973), 349-381,
DOI `10.1016/0022-1236(73)90051-7`, is the historical primary-source candidate. The commonly cited
mountain-pass result is Theorem 2.1, but its exact page, wording, hypotheses, and any publisher
errata have not yet been checked against a stable copy. This bibliographic identification is a
discovery anchor, not `H0` evidence.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "critical point existence" | a point where the derivative vanishes | Frechet derivative equals the zero continuous linear map | included; encoding open |
| mountain-pass geometry | base point, barrier sphere, and low endpoint beyond it | norm sphere and ordered real inequalities | included; normalization open |
| Palais-Smale condition | compactness for bounded-energy approximate critical sequences | sequence/subsequence convergence predicate | included; exact variant open |
| paths from `0` to `e` | admissible continuous curves | `ContinuousMap` or equivalent endpoint-constrained paths | included; API open |
| minimax critical level | infimum of pathwise maxima | conditionally complete lattice operations plus attained maxima | included; construction open |

## Fidelity boundary

Stage0 supplies only the Chinese name, the gloss `临界点存在性`, attribution to Ambrosetti and
Rabinowitz, and year 1973. It does not freeze a mathematical statement. The statement phase must
inspect the primary article, record theorem/page and all assumptions, check errata, and produce a
row-by-row source-to-Lean mapping. Independent review is required before `H0`.

No repo-local Lean declaration has been credited or audited during intake. A theorem with only the
geometric hypotheses but no Palais-Smale condition, or one concluding only an approximate critical
sequence, is not an exact anchor for this target.
