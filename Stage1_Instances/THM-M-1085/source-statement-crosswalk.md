# Source-statement crosswalk

## Candidate sources

- D. Slepian, "The one-sided barrier problem for Gaussian noise," *Bell System Technical Journal*
  41 (1962), 463-501. This is the historical primary-paper candidate. The exact result number,
  hypotheses, covariance orientation, treatment of singular covariance, and errata require direct
  inspection before it can support `H0`.
- R. J. Adler and J. E. Taylor, *Random Fields and Geometry*, Springer, 2007, Section 2.2. This is a
  modern formulation candidate. The exact theorem/page, conventions, and relationship to the 1962
  result must be checked against a fixed edition.

These references are discovery anchors only. Bibliographic identification and the familiar theorem
name do not constitute an audited primary-source proof or exact-statement match.

## Crosswalk

| Repository phrase | Frozen intended component | Required Lean component | Intake status |
|---|---|---|---|
| Slepian's lemma | finite Gaussian comparison theorem | one exact declaration, not a theorem-family label | included; source pin open |
| Gaussian vectors | centered, jointly Gaussian real coordinates | finite indexed family/law plus joint-Gaussian predicate | included; encoding open |
| equal variances | `Var(X_i) = Var(Y_i)` coordinatewise | integrability, expectation, variance | included; convention open |
| covariance order | `Cov(X_i,X_j) <= Cov(Y_i,Y_j)` off diagonal | covariance definition and pairwise quantification | included; orientation sanity-checked |
| comparison | lower-tail order of finite maxima for every `u` | measurable finite maximum and event probability | included; strictness open |
| degeneracy | singular covariance allowed if source permits | approximation/continuity bridge if APIs require positivity | intended; source audit open |

## Assumption and conclusion boundary

Centering, joint Gaussianity, a shared nonempty finite index set, equal coordinate variances, and
pairwise covariance order are root-relevant assumptions. The conclusion is a distributional
comparison for every threshold, not merely an expectation inequality. The statement phase must
mutation-test removal of equal variances, reversal of covariance order, an empty index type, and a
changed event direction before any proof closure is credited.

## Evidence boundary

No repo-local Lean declaration has been accepted or inspected for this intake. Repository text
search found no Slepian-named mathlib declaration, but that is not a complete anchor audit. The
statement and anchor-audit phases must inspect the pinned mathlib revision and credible external
Lean projects, recording exact modules, declaration types, revisions, axioms, and terminal body
provenance. Before `H0`, an independent reviewer must verify the chosen primary edition, exact
result/page, assumptions, proof boundary, errata, and every source-to-Lean crosswalk row.
