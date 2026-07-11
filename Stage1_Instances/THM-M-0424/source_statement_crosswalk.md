# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Stable classes of central simple algebras over a field | R. Brauer, *Untersuchungen ueber die arithmetischen Eigenschaften von Gruppen linearer Substitutionen I*, Math. Z. 28 (1928), 677-696 | `CSA K`, `IsBrauerEquivalent`, `BrauerGroup K` in `Mathlib.Algebra.BrauerGroup.Defs` | Historical primary anchor located, but exact section/page premise and errata audit remain open |
| Abelian operation induced by tensor product | E. Artin, C. J. Nesbitt, R. M. Thrall, *Rings with Minimum Condition* (1944), Brauer-group treatment; exact edition/page must be pinned | `CSATensorProductData` and `BrauerGroupAbelianLawData` in the legacy local module | These are uninhabited target interfaces, not proof evidence |
| Identity and inverse | Standard field class and opposite-algebra construction in the same classical theory | proposed `oneRep` and `invRep` fields of `BrauerGroupAbelianLawData` | Statement candidates only; constructions and laws are not credited |
| Equality of classes iff Brauer equivalence | Definition of the quotient by stable matrix equivalence | `brauerClass_eq_iff_isBrauerEquivalent` | Legacy repo-local wrapper is a discovery candidate and is weaker than the root |
| Division-algebra normal form | J. H. M. Wedderburn, structure theory for finite-dimensional simple algebras; exact primary theorem genealogy pending | `IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite` | Supporting classification theorem, not a substitute for the group law |

The repository source phrase `中心单代数的分类` (classification of central simple algebras) does not
specify whether it means Artin-Wedderburn classification, Brauer stable classification, the abelian
group construction, or an arithmetic computation. The theorem name `布饶尔群`, historical Brauer
attribution, and legacy formal boundary support the conservative group-construction reading frozen
in `intake.json`. This inference still requires primary-source review and independent acceptance.

No `H0` or machine-closure claim is made. The statement phase must choose and elaborate one exact
Lean expression, freeze binders/universes and imports, check transports, and mutation-test the field
hypothesis, centrality/simplicity/finite-dimensionality, equivalence relation, and operation laws.
The later source audit must pin editions or immutable scans, map every premise to pages/sections,
search corrections, and distinguish the original historical construction from modern reformulations.
