# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Every finite abelian extension of `Q` lies in a cyclotomic field | L. C. Washington, *Introduction to Cyclotomic Fields*, 2nd ed., Springer GTM 83 (1997), Chapter 14 (Kronecker-Weber theorem) | `AwesomeTheorems.Stage1.S1_M_074.StatementShape K` | Standard source located, but exact theorem/page, assumptions, edition hash, and errata require source audit: `H1` |
| Extension is finite | Encoded by “finite extension” in the classical formulation | `[NumberField K]` together with `[Algebra Q K]` | Candidate typeclass encoding; exact redundancy and universe behavior require elaboration |
| Extension is abelian over `Q` | Encoded by “abelian extension” in the classical formulation | `[IsAbelianGalois Q K]` | Candidate packages Galois and commutativity; declaration type must be inspected |
| Containment in `Q(zeta_n)` | Classical subfield/containment formulation | `Nonempty (K ->ₐ[Q] CyclotomicField n Q)` | An algebra embedding is the intended presentation-level containment; equivalence to an intermediate-field formulation is not yet accepted |
| Positive cyclotomic index | Classical sources generally take a positive integer modulus | `exists n : Nat, n != 0` | Boundary convention is explicit; mutation and API checks are deferred |

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_074.lean` supplies a useful
candidate statement and adjacent mathlib wrappers. Under rev-5.6 it is unaccepted discovery input:
it explicitly says that it contains no terminal Kronecker-Weber proof. No machine closure is inferred
from the source label `已验证` or from those wrappers.

Discovery sources, not immutable evidence receipts:

- Washington, DOI: <https://doi.org/10.1007/978-1-4612-1934-7>
- D. A. Marcus, *Number Fields*, 2nd ed., Springer Universitext (2018), chapter on cyclotomic fields and the Kronecker-Weber theorem, as a secondary comparison source.

No `H0` claim is made. The source audit must verify a physical or immutable digital edition,
pinpoint theorem/page and premises, check errata, map proof nodes to source passages, and obtain
independent review. The statement phase must elaborate the actual Lean expression, fingerprint the
environment, validate transports, and mutation-test binders, assumptions, and boundary indices.
