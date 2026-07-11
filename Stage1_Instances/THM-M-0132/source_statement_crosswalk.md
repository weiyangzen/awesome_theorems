# Source-statement crosswalk

| Claim component | Primary source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Every elliptic curve over `Q` is modular | C. Breuil, B. Conrad, F. Diamond, R. Taylor, *On the modularity of elliptic curves over Q: wild 3-adic exercises*, JAMS 14 (2001), 843-939, Theorem A: "Every elliptic curve over Q is modular." DOI `10.1090/S0894-0347-01-00370-8` | `AwesomeTheorems.Stage1.S1_M_049.StatementShape` | Root wording located, but immutable source hash, assumptions/errata audit, and exact Lean correspondence are not accepted: `H1` |
| Semistable branch | A. Wiles, *Modular elliptic curves and Fermat's Last Theorem*, Annals of Mathematics 141 (1995), 443-551, Theorem 0.4: every semistable elliptic curve over the rationals is modular | `SemistableStatementShape` | Historical branch only; it must not be substituted for Theorem A |
| Completion of the semistable argument | R. Taylor, A. Wiles, *Ring-theoretic properties of certain Hecke algebras*, Annals of Mathematics 141 (1995), 553-572 | future semistable proof nodes | Companion proof source located; premise-to-node mapping remains open |
| Elliptic curve over `Q` | BCDT Theorem A domain | `WeierstrassCurve Rat` plus `IsElliptic` | Plausible mathlib model, but invariance and correspondence with the source's elliptic-curve object require checking |
| "is modular" | BCDT introductory conventions and referenced modularity framework | `IsModularEllipticCurve` / `ModularEllipticCurveWitness` | Legacy predicate is only a boundary: its freely supplied compatibility `Prop`s do not yet encode modularity |
| Weight, level, and compatibility | Standard weight-two newform formulation used in the cited modularity literature | `Gamma0WeightTwoCuspFormShape` and one candidate relation | Conductor equality, normalized eigenform structure, coefficients, and an actual compatibility proposition are missing |

The canonical human root is BCDT Theorem A, not merely the original conjecture and not Wiles's
semistable theorem. The statement phase must choose a precise modularity formulation, inspect the
actual Lean types, serialize the normalized expression, and mutation-test the universal quantifier,
base field, nonsingularity hypothesis, weight, level, and compatibility conditions.

Discovery links (not immutable evidence receipts):

- BCDT: <https://doi.org/10.1090/S0894-0347-01-00370-8>
- Wiles: <https://doi.org/10.2307/2118559>
- Taylor-Wiles: <https://doi.org/10.2307/2118560>

No `H0` or machine-closure claim is made. Required follow-up includes source-file hashing, errata
and correction search, detailed assumptions-to-node mapping, and independent review.
