# Source-statement crosswalk

## Candidate primary source

M. F. Atiyah and R. S. Ward, "Instantons and algebraic geometry", *Communications in
Mathematical Physics* 55 (1977), 117-124, DOI `10.1007/BF01626514`, is the primary candidate
matching the repository phrase "instantons and algebraic geometry". A stable copy must still be
inspected to identify the exact numbered result/page, referenced definitions, hypotheses, and any
errata. Bibliographic identification is not H0.

The label "Atiyah-Ward correspondence" is used for variants differing in base space, orientation,
framing, structure group, charge, and reality convention. The statement phase may not merge these
variants or silently replace the original result with the broader Ward correspondence.

## Crosswalk

| Repository phrase | Intended source component | Required Lean component | Intake status |
|---|---|---|---|
| "Atiyah-Ward correspondence" | one exact correspondence result | one canonical proposition with both moduli quotients | family identified; theorem/page open |
| instantons | (anti-)self-dual finite-action connections under source conventions | connection, curvature, Hodge star, ASD equation, analytic hypotheses | included; conventions open |
| algebraic geometry | holomorphic bundles on twistor/projective space | concrete complex space and holomorphic vector-bundle model | included; object API open |
| twistor lines | distinguished real projective lines | incidence family and restriction functor | included; exact real-line convention open |
| line triviality | trivial restriction on every required line | bundle trivialization/isomorphism predicate | included; rank and quantifiers open |
| reality condition | compatibility with the twistor involution | lifted conjugate-linear structure and coherence laws | included; source formulation open |
| correspondence | mutually inverse constructions modulo equivalence | well-defined maps and an equivalence of quotient/moduli types | included; quotient choices open |

## Evidence boundary

The legacy Lean module elaborates useful abstract interfaces and elementary consequences, but its
`WardTransformAPI` takes the transforms and inverse laws as data. It is neither source fidelity
evidence nor a terminal proof body for the classical theorem. Before H0, independent review must
verify the edition, exact page/result, assumptions, definitions, and errata row by row. Before any
M-credit, the canonical Lean target must elaborate and later audits must inspect terminal bodies,
axioms, and immutable dependency revisions.
