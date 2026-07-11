# Source-statement crosswalk

| Claim component | Human source discovery anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Minimal deformation ring equals the corresponding Hecke algebra | R. Taylor and A. Wiles, *Ring-theoretic properties of certain Hecke algebras*, Annals of Mathematics 141 (1995), 553-572, DOI `10.2307/2118560` | `TaylorWilesPatchingData.isREqualsT` inside `SelectedStatementShape` | Primary source identified, but exact theorem number, assumptions, edition hash, and errata mapping remain open |
| Modularity lifting for an odd two-dimensional representation | A. Wiles, *Modular elliptic curves and Fermat's Last Theorem*, Annals of Mathematics 141 (1995), 443-551, DOI `10.2307/2118559` | conclusion `IsModularLift rho M` | The local predicate is only an abstract compatibility witness, not yet an exact encoding of Wiles's theorem |
| Residual modularity and irreducibility | Wiles 1995 and Taylor-Wiles 1995 hypotheses | `SelectedResidualHypotheses rho M` | Rank/oddness/irreducibility are named, but determinant and restriction hypotheses may be missing |
| Minimal local deformation problem | Wiles 1995 minimal case and Taylor-Wiles patching setup | `SelectedLocalHypotheses patch lift` | Abstract predicates do not yet encode primes, inertia, conductor, finite-flatness, or ordinarity concretely |
| Auxiliary primes and patching | Taylor-Wiles 1995 | fields of `TaylorWilesPatchingData` | Data boundary only; no construction, infinitude result, or patching theorem is supplied |
| `R = T` implies modularity | Consequence in the classical argument | implication to `IsModularLift rho M` in `StatementShape` | Candidate logical placement; must be separated and checked as a bridge if the source root is `R = T` |

The repository's historical `S1_M_065.lean` is a useful vocabulary sketch, but it bundles crucial
mathematics into `Prop` fields and even assumes `isREqualsT` before concluding modularity. It cannot
serve as an exact formalization or terminal proof. The statement phase must select a pinpointed
primary theorem, transcribe every premise, choose concrete or explicitly axiomatized object models,
serialize the elaborated target, and mutation-test omitted hypotheses and boundary cases.

No `H0` or machine closure is claimed. Source audit still requires immutable source hashes, exact
page/theorem locations, correction/errata search, premise-to-binder mapping, and independent review.
