# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Index equals the sum of conjugate-point multiplicities | J. Milnor, *Morse Theory*, Annals of Mathematics Studies 51, Princeton University Press (1963), Section 15, Theorem 15.1 (the index theorem) | no exact repo-local declaration identified | Primary-source discovery anchor located; edition/scan hash, premise-by-premise audit, and errata review are not accepted: `H1` |
| Index form is the fixed-endpoint second variation | Milnor, *Morse Theory*, Sections 14-15 | future Hessian/index-form bridge | The functional-analytic domain and normalization must be frozen before correspondence can be credited |
| Conjugate multiplicity | dimension of the space of Jacobi fields vanishing at the initial point and at the conjugate point | future Jacobi evaluation-kernel definition | Candidate mathematical encoding only |
| Interior sum and endpoint condition | conjugate instants strictly before the terminal instant; terminal nonconjugacy makes the critical point nondegenerate | future finite conjugate-instant sum | Interval boundary convention is frozen in prose but not checked in Lean |

The source theorem has several nearby formulations, including versions that state index and nullity
together when the terminal endpoint is conjugate. This dossier does not silently identify those
variants. Its planned root excludes terminal conjugacy, counts multiplicity in the open segment,
and requires a checked bridge between the source's variation space and whichever Lean completion is
chosen.

No mathlib theorem name is asserted at intake. Later anchor audit must search the pinned dependency
tree and external Lean 4 projects, recording exact modules, declaration types, revisions, axioms,
and terminal proof provenance. Later source audit must pin the cited edition, map every assumption,
check corrections/errata, and obtain independent review before any `H0` claim.

Discovery link (not an immutable evidence receipt):

- Milnor book record: <https://press.princeton.edu/books/paperback/9780691080086/morse-theory>
