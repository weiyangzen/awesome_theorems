# Source-statement crosswalk

| Claim component | Human source anchor | Lean target candidate | Intake assessment |
|---|---|---|---|
| Hamiltonian evolution preserves phase-space volume | V. I. Arnold, *Mathematical Methods of Classical Mechanics*, 2nd ed., Springer, 1989, Chapter 3, section 16, "Liouville's theorem" (discovery bibliographic anchor) | `Stage1.THM_M_1520.LiouvilleStatement`: `MeasurePreserving (Phi t) volume volume` for a global canonical Hamiltonian flow | Exact Lean target elaborated; primary-source pinpoint, assumptions, proof-node mapping, and errata review are not accepted: `H2` |
| Hamiltonian flow preserves the symplectic form | Same classical symplectic formulation; exact proposition/page requires source audit | a flow/pullback theorem for the Hamiltonian vector field | Candidate structural parent; no exact mathlib declaration or checked instantiation yet |
| Preservation of volume follows from preservation of `omega` | exterior-algebra identity for the top exterior power `omega^n/n!` | pullback commutes with wedge powers and scalar multiplication | Necessary bridge candidate; normalization and orientation/measure conventions remain open |
| Canonical-coordinate formulation | standard Hamilton equations plus vanishing divergence | Euclidean divergence/Jacobian statement | Useful local route, but only a special encoding until a checked manifold equivalence is supplied |
| Measure invariance | volume-form invariance implies invariance of the associated measure | equality of mapped/restricted measures on the domain of the local flow | Corollary candidate; measurability and local-domain boundaries must be explicit |

The repository discovery source says only "phase-space volume conservation" and marks it
"verified". That metadata fixes the intended theorem family but does not specify compactness,
completeness, regularity, sign conventions, local-flow domains, orientation, or a formal encoding.
The statement phase chooses the standard canonical-coordinate formulation for every finite number
of degrees of freedom. The stronger manifold/local-flow formulation remains an alternate route and
is not claimed equivalent without a checked transport.

No `H0` or machine-closure claim is made. Required source work includes an immutable scan/hash,
exact page and theorem wording, convention and assumption mapping, correction/errata search, and an
independent review. Required formal work includes repository-local mathlib search, exact declaration
types and revisions, checked transports between geometric, coordinate, and measure formulations,
and mutation tests preventing a Euclidean-only or assumed-invariance substitute.

Discovery references (not accepted immutable receipts):

- Arnold, DOI: <https://doi.org/10.1007/978-1-4757-2063-1>
- Repository source record: `Docs/researches/math_theorems.md` (the THM-M-1520 provenance selected
  into `Docs/Stage0_Blueprint.md`)
