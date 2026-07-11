# Source-statement crosswalk

The repository source record states the canonical-coordinate formula
`{f,g} = sum_i (partial_qi f partial_pi g - partial_pi f partial_qi g)` and says that it describes
the algebraic structure of physical quantities. The table separates that statement from nearby
claims that intake must not import into the target without evidence.

| Claim component | Repository or human-source anchor | Lean target at intake | Assessment |
|---|---|---|---|
| Coordinate formula | `Docs/researches/physics_theorems.md`, Hamiltonian mechanics item 4 | None selected | Exact repository wording located, but it is a definition rather than a closed proposition |
| Historical Poisson bracket | S.-D. Poisson, *Traite de mecanique*, first edition (1811), associated historically with the canonical bracket | None selected | Discovery-level bibliographic anchor only; exact volume/page, edition scan, notation, and errata are not audited |
| Algebraic structure | Candidate laws are bilinearity, antisymmetry, Leibniz, and Jacobi | Unselected conjunction or structure instance | The phrase does not determine whether one law, all laws, or an abstract Poisson-algebra structure is intended |
| Intrinsic formulation | A Poisson or symplectic manifold yields a bracket on smooth functions | Unselected model | Stronger/global formulation not licensed by the coordinate source wording |
| Constants-of-motion closure | Separate repository item: "the Poisson bracket of two constants of motion is again a constant of motion" | Excluded from this root | This is the separately listed Poisson theorem and would be a substituted theorem here |

The statement phase must use a primary edition to choose a proposition, then freeze the scalar
field, finite index type/dimension, phase-space domain, differentiability assumptions, ordered
binders, sign convention, summation convention, and whether the root is a single law or a bundled
Poisson-algebra result. Zero-dimensional phase space, constant functions, and swapped arguments
must be boundary or mutation probes.

No `H0` claim is made. `H2` records only a historical anchor and the exact repository wording;
edition hashing, pinpoint premise mapping, translation/notation review, errata search, and
independent review remain open. The repository label `已验证` is untrusted metadata and supplies no
human-source or machine-proof credit.
