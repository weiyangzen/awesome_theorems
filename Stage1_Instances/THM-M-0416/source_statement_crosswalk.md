# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Unit-group structure | J. Neukirch, *Algebraic Number Theory*, Springer (1999), Chapter I, section on the unit theorem | `AwesomeTheorems.Stage1.S1_M_071.StatementShape` | Standard primary textbook anchor located; exact theorem/page, edition identity, and errata still require audit: `H1` |
| Torsion factor | Classical roots-of-unity subgroup `mu(K)` | `NumberField.Units.torsion K` | Intended correspondence; equality with roots of unity and finiteness need declaration-level audit |
| Free rank | Classical rank `r1 + r2 - 1` | `NumberField.Units.rank K` and `rank_modTorsion` | The legacy wrapper states mathlib rank; the formula and place-count conventions must be cross-checked |
| Direct-product expression | A basis of fundamental units gives unique torsion-times-powers expression | `fundSystem` and `exist_unique_eq_mul_prod` | Strong candidate discovered, but exact type, imports, axioms, and terminal provenance belong to later phases |
| Finite free quotient | Equivalent quotient formulation of the structure theorem | `Module.Free`, `Module.Finite`, and `Module.finrank` on the additive quotient | Equivalence to the classical direct-product statement is not accepted at intake |

The repo-local discovery module is
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_071.lean`; it imports
`Mathlib.NumberTheory.NumberField.Units.DirichletTheorem` and names relevant declarations. Under
rev-5.6 it is legacy discovery input only. Its compiled status, pinned revision string, wrappers,
and proof claims must be independently re-audited before receiving any machine credit.

Additional comparison source: S. Lang, *Algebraic Number Theory*, 2nd ed., Springer GTM 110
(1994), chapter on the unit theorem. No `H0` claim is made. Source audit must obtain an immutable
edition, verify exact theorem/page and conventions, check errata, and map proof nodes to passages.
Statement work must elaborate and fingerprint the target, validate equivalent encodings, and
mutation-test hypotheses, binder scope, rank-zero behavior, and empty products.
