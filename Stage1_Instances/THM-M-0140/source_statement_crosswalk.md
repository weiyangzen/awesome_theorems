# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Canonical basis for a Coxeter Hecke algebra | D. Kazhdan and G. Lusztig, *Representations of Coxeter groups and Hecke algebras*, Inventiones Mathematicae 53 (1979), 165-184, especially Section 1 | future concrete replacement for `AwesomeTheorems.Stage1.S1_M_056.StatementShape` | Primary paper and relevant section located; theorem/proposition pinpoint, immutable copy, assumptions, and errata review are not yet accepted: `H1` |
| Coxeter system and length | Same paper, opening definitions in Section 1 | `CoxeterMatrix`, `CoxeterSystem`, and `CoxeterSystem.length` candidates in mathlib | Candidate object correspondence only; no exact encoding crosswalk is credited |
| Hecke algebra and standard basis | Same paper's Hecke algebra construction and standard basis conventions | no accepted concrete repo-local declaration | Required root object is absent from the accepted intake target |
| Bar involution | Same paper's involution used to characterize the basis | no accepted concrete repo-local declaration | Coefficient and algebra involutions must be formalized and convention-checked |
| Triangular normalization and uniqueness | Same paper's canonical-basis characterization in Section 1 | legacy `KazhdanLusztigBasisPackage` is only an abstract discovery model | The legacy predicates do not encode coefficients, Bruhat support, or normalization and cannot receive exact-statement credit |
| Transition coefficients/Kazhdan-Lusztig polynomials | Coefficients arising from the canonical basis in the original construction | future downstream declarations | Downstream output; neither a replacement for nor proof of the basis root |

The title-level repository description, "the canonical basis of a Hecke algebra," is intentionally
narrowed here to the generic one-parameter Hecke algebra attached to a Coxeter system. It is not the
Kazhdan-Lusztig conjecture and not the unrelated later canonical-basis theory for quantum groups.
The statement phase must select a coefficient parameter convention, serialize the normalized Lean
expression, check transports between common conventions, and mutation-test Coxeter hypotheses,
Bruhat triangularity, bar invariance, and rank-zero/rank-one boundaries.

Discovery locator (not an immutable evidence receipt):

- Original paper DOI: <https://doi.org/10.1007/BF01390031>

No `H0` or machine-closure claim is made. Required source follow-up includes an immutable edition
hash, exact result/page pinpoint, notation and premise mapping, correction/errata search, and
independent review.
