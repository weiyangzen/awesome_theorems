# Source-statement crosswalk

## Available record and source candidates

The repository inventory supplies the Chinese title "Wigner semicircle law", Eugene Wigner, 1955,
and the gloss "eigenvalue distribution of Wigner matrices". Its `已验证` value is untrusted
metadata under rev-5.6 and contains no assumptions or convergence claim.

The historical primary-source candidate is Eugene P. Wigner, *Characteristic Vectors of Bordered
Matrices With Infinite Dimensions*, **Annals of Mathematics** 62(3) (1955), 548-564,
DOI `10.2307/1970079`. This intake records bibliographic discovery only. The paper's exact theorem
or displayed result, probability model, normalization, mode of convergence, relevant pages,
corrections, and relationship to the modern named formulation have not yet received a pinned
edition audit and independent review. It therefore does not establish `H0`.

A modern source must be chosen if the canonical root is stronger than Wigner's exact 1955 result.
That choice must preserve honest genealogy: a modern almost-sure or weak-convergence theorem may
not be cited as though it were verbatim the original statement.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "Wigner matrices" | symmetric/Hermitian ensemble and entry laws | probability space, random matrix, symmetry and independence predicates | family identified; exact domain open |
| "eigenvalue distribution" | empirical measure with multiplicities | real spectrum and finite empirical probability measure | intended object identified; encoding open |
| semicircle law | limiting compactly supported probability measure | Borel probability measure and scaled semicircle density | included; scale open |
| large dimension | sequence indexed by matrix size and limit `n -> infinity` | dimension-indexed measurable family and convergence filter | included; binder order open |
| convergence | expectation/probability/almost-sure weak convergence | exact measure-convergence predicate and null-set quantifiers | unresolved |
| 1955 / Wigner | historical locator | no machine-proof credit | candidate paper identified only |

## Human and machine boundary

The repo-local text search found no theorem-specific Lean artifact for `THM-M-1105`, and a narrow
name search of the pinned mathlib source found no declaration or module named for Wigner or the
semicircle law. These negative searches are discovery observations, not a complete anchor audit.
The later anchor phase must search by underlying probability, matrix-spectrum, empirical-measure,
and convergence APIs, then inspect credible external Lean projects at immutable revisions.

Before `H0`, an independent reviewer must verify the selected edition, theorem/page or exact
statement location, definitions, every hypothesis, proof boundary, and errata. Before statement
credit, every row must map to an elaborated Lean target, including normalization and convergence
mode. No public machine-checked proof and no repo-local proof closure is claimed here; the current
machine debt remains unclassified between missing infrastructure and theorem formalization until
the statement and anchor audits are performed.
