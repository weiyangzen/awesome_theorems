# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| No nonzero solutions to `a^n + b^n = c^n` for integral `n > 2` | A. Wiles, *Modular elliptic curves and Fermat's Last Theorem*, Annals of Mathematics 141 (1995), pp. 443-551; introduction states FLT and explains the semistable-modularity implication | `Mathlib.NumberTheory.FLT.Basic.FermatLastTheorem` | Named primary proof source, but a versioned page/theorem-to-node premise audit and errata review are not yet accepted: `H1` |
| Completion of the modularity argument used for FLT | R. Taylor and A. Wiles, *Ring-theoretic properties of certain Hecke algebras*, Annals of Mathematics 141 (1995), pp. 553-572 | future `M0387-WTW` nodes | Primary companion source located; detailed assumptions-to-node crosswalk remains open |
| Fixed exponent over naturals | Same root claim specialized to one `n` | `FermatLastTheoremFor n` | Candidate statement API; exact elaboration deferred |
| Integer and rational formulations | Classical scaling/sign transports; source genealogy not yet pinpointed | `FermatLastTheoremWith Int n`, `FermatLastTheoremWith Rat n` | Existing Lean equivalence names located, but no rev-5.6 credit before checked statement work |
| Primitive/coprime formulation | Standard primitive-solution reduction; primary pinpoint still required | `FermatLastTheoremForCoprime n` in the legacy local module | Candidate local bridge only |

The historical wording and modern natural-number encoding agree on the intended mathematical
content after sign/permutation and denominator-clearing transports, but this sentence is not a
checked bridge. The statement phase must inspect the actual declaration type, serialize its
normalized expression, check every credited transport, and mutation-test domain, binders,
hypotheses, and boundary exponents before any proof evidence is considered.

Source links for discovery (not immutable evidence receipts):

- Wiles: <https://doi.org/10.2307/2118559>
- Taylor-Wiles: <https://doi.org/10.2307/2118560>

No `H0` claim is made. Required follow-up includes edition/file hashes, pinpoint premise mapping,
errata/correction search, and independent review.
