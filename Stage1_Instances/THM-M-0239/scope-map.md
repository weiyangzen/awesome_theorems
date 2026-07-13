# Scope map

## Preserved theorem family

The intake preserves the classical inversion family named by the catalog:

- a compact Riemann surface or corresponding nonsingular algebraic curve of genus `g >= 1`;
- first-kind Abelian differentials and their path-dependent integrals modulo a period lattice;
- simultaneous inversion using `g` variable points, rather than inversion of one integral when
  `g > 1`; and
- a global existence or explicit inversion result associated with the surface's Jacobian.

These bullets delimit a recognizable family. They are not an accepted canonical statement,
definition chain, equivalence claim, Lean expression, or proof.

## Candidate formulations not credited

1. **Surjectivity form.** For a compact Riemann surface `X` of genus `g`, a degree-`g`
   Abel-Jacobi map `X^(g) -> J(X)` is surjective.
2. **Divisor-class form.** Every relevant degree-zero class is represented by `D - g P0` for an
   effective divisor `D` of degree `g`, after a base point and divisor/Jacobian conventions are
   fixed.
3. **Integral-congruence form.** Given a basis of holomorphic differentials and a point of the
   period quotient, find `g` points whose summed integrals realize it modulo periods.
4. **Explicit theta form.** Construct symmetric meromorphic functions of the solution points by
   genus-`g` theta functions and state the normal and exceptional cases.

The first three are often related presentations of the existence boundary; the fourth carries
additional explicit analytic content. No relationship is credited without a source-approved root
and checked transports.

## Decisions required at statement freeze

1. Select and lawfully preserve an immutable source edition with exact theorem, incorporated
   definitions, proof boundary, corrections, errata, and independent review.
2. Fix whether `X` is an analytic compact connected Riemann surface or a smooth projective
   algebraic curve, and specify nonemptiness, connectedness, genus, universes, and equivalence
   between analytic and algebraic models if both are used.
3. Define first-kind differentials, integration paths, homology basis, period matrix/lattice, the
   quotient defining `J(X)`, and equality modulo periods for an analytic formulation.
4. Define `X^(g)`: a finite multiset only, or the analytic/algebraic symmetric product with its
   quotient structure. Type-level `Sym X g` alone does not provide the required geometry.
5. Define divisors, degree, effectivity, linear equivalence, `Pic^0`, the Jacobian, and the exact
   checked relation among divisor, period-quotient, and Picard presentations.
6. Fix the Abel-Jacobi map, base point or independent base points, sign and translation
   normalization, ordered binders, and whether the theorem is merely surjectivity or includes a
   fiber, uniqueness, birationality, or explicit inversion claim.
7. For a theta formulation, fix normalization, characteristics, Riemann constants, normal versus
   exceptional input, multiplicities of zeros, and precisely which symmetric functions are
   represented.
8. Resolve genus `0`, genus `1`, repeated solution points, special divisors and positive-dimensional
   fibers, dependence on paths and bases, and every source-specific degeneracy.

## Explicit exclusions

- `THM-M-0238`, whose catalog gloss is inversion of elliptic integrals, as a genus-one substitute.
- `THM-M-0240`, whose catalog label is the Abel-Jacobi theorem, without a source-reviewed duplicate
  or dependency decision.
- Abel's theorem about when a divisor is principal, Abel-Jacobi injectivity on divisor classes, or
  a local inverse-function theorem.
- A genus-one Jacobi elliptic function or the pinned two-variable `jacobiTheta₂` functional
  equation in place of the arbitrary-genus theorem.
- The `Jacobian` namespace for weighted coordinates on a Weierstrass curve; it is not the general
  Jacobian variety of a compact curve.
- The Picard group `CommRing.Pic R` of a commutative ring as the Picard variety or `Pic^0(X)` of a
  curve.
- A bare type-level symmetric power, abstract structure storing the desired map/surjectivity as a
  field, numerical period computation, or source-free theorem chosen for API convenience.
- The catalog's untrusted `已验证` label, a citation, a theorem name, or adjacent API elaboration as
  human or machine proof evidence.

## Formal boundary

No canonical Lean expression is frozen. A bounded repo-local and pinned-mathlib search found no
exact Jacobi inversion declaration. Pinned mathlib's complex-manifold module explicitly lists
holomorphic line bundles and finite-dimensional section spaces as future work; its symmetric power
is combinatorial, its theta API is one-dimensional, and its Picard/Jacobian names refer to different
objects. These are intake observations, not an exhaustive external anchor audit or proof of global
absence.
