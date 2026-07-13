# Scope map

## Preserved theorem family

- Inversion of a genus-one elliptic integral in the historical Abel/elliptic-function setting.
- A resulting single-valued elliptic function after the appropriate period identifications.
- The 1827 Abel attribution and complex-analysis category supplied by the repository.

These bullets preserve the recognizable topic boundary. They are not an accepted proposition,
source crosswalk, Lean expression, or proof.

## Decisions required at statement freeze

1. Select an immutable primary or authoritative edition, an exact proposition and incorporated
   definitions, its proof boundary, translation relationship, corrections, errata, and independent
   review.
2. Fix the elliptic integral: Legendre normal form, a cubic or quartic algebraic differential, or
   another source-defined form; freeze every coefficient, parameter, modulus, and nonsingularity or
   distinct-root hypothesis.
3. Fix real versus complex scope, the algebraic curve or branched cover, basepoint, integration
   path, chosen square-root branch, analytic continuation, and the equivalence of paths.
4. Define "inverse": a local analytic inverse on a selected branch, a multivalued inverse, a
   meromorphic function on the complex plane, or a map from a quotient by a period lattice.
5. Freeze normalization, fundamental periods and their ordering, period-lattice construction,
   domain, codomain, and equality modulo periods.
6. Select the conclusion: existence, explicit construction, single-valued meromorphic extension,
   double periodicity, differential equation, addition law, or a source-specified conjunction.
7. Resolve branch points, poles, lattice points, zero or degenerate discriminant, limiting moduli,
   endpoints, empty domains, and every boundary convention.
8. Freeze the ordered binders, universes, typeclass context, all coercions, and any transport among
   Legendre, Jacobi, Weierstrass, curve, and quotient-torus encodings.

## Explicit exclusions

- `THM-M-0239`, the separately cataloged general Jacobi inversion theorem for Abelian integrals.
- `THM-M-0240`, the separately cataloged Abel-Jacobi theorem for algebraic curves and Jacobians.
- Abel's theorem on sums of algebraic integrals, Abel's power-series limit theorem, the Abel-Ruffini
  theorem, or any other result sharing Abel's name.
- Construction, periodicity, meromorphicity, pole order, or differential equation of the
  Weierstrass `P` function alone, without a checked inverse relation to the source-selected integral.
- A convenient special modulus, real interval, local inverse, or assumed inverse structure chosen
  without source approval.
- The catalog's untrusted `已验证` label, a theorem name, adjacent API elaboration, or another
  target's receipt as source or kernel evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib contains a `PeriodPair`, its period lattice,
the Weierstrass `P` function, periodicity, meromorphicity, pole order, and its cubic differential
equation. These are output-side ingredients adjacent to elliptic-integral inversion. The inspected
module does not define the source-selected integral, its primitive or branches, a quotient
torus-to-curve equivalence, or an inverse theorem. This bounded intake observation is neither a
complete anchor audit nor proof that no external formalization exists.
