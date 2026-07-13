# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-0240`, the title `阿贝尔-雅可比定理`, the gloss
`代数曲线的雅可比簇`, the attribution to Niels Abel/Carl Jacobi, and the year 1834. Importance
`high` and status `已验证` are catalog metadata, not human-source or kernel evidence.

The title and noun-phrase gloss locate a classical curve/Jacobian family but do not identify one
truth-valued root. A later statement phase may select a proposition only from an immutable,
independently reviewed source passage and must preserve the neighboring target boundaries.

## Candidate interpretations not credited

1. Existence of an abelian variety representing a degree-zero Picard functor of a complete smooth
   algebraic curve, with a precise qualification when the curve has no rational point.
2. An isomorphism between a source-defined `Pic^0(C)` and the rational points of the Jacobian.
3. Abel's theorem: a degree-zero divisor has zero Abel-Jacobi image exactly when it is principal.
4. Jacobi inversion: a symmetric power, commonly of degree equal to the genus, surjects onto the
   Jacobian.
5. A based Abel-Jacobi map from the curve to its Jacobian and an injectivity, embedding, generation,
   or genus-dependent exceptional-case result.
6. A universal property identifying the Jacobian as an Albanese or Picard variety.
7. Over the complex numbers, an identification of the algebraic Jacobian with the analytic complex
   torus formed from holomorphic differentials and integral homology.

These interpretations have different binders, hypotheses, conclusions, constructions, and proof
dependencies. None is selected, asserted, or credited at intake.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- the exact numbered proposition or source-defined conjunction and its proof boundary;
- algebraic, analytic, or comparison formulation and whether the result is existence,
  representability, identification, inversion, kernel characterization, map property, or universal
  property;
- the base field and whether it is arbitrary, perfect, separably or algebraically closed, or
  specifically `Complex`;
- the curve convention: complete/projective, nonsingular/smooth, geometrically connected or
  integral, and its genus;
- whether a rational base point is assumed, how absence of one changes the Picard functor or point
  identification, and whether a divisor of degree one suffices;
- the precise divisor, linear-equivalence, invertible-sheaf, Picard-functor, `Pic^0`, symmetric
  power, abelian-variety, analytic-torus, and Abel-Jacobi map definitions;
- covariance and sign conventions, degree component, chosen base point, normalization of the map,
  and whether equality, equivalence, isomorphism, surjectivity, injectivity, or representability is
  concluded;
- all ordered binders, universes, typeclass assumptions, incorporated definitions, transports, and
  uniqueness clauses; and
- historical edition, correction or errata state, source-node mapping, and every boundary case
  below.

## Degenerate and boundary cases

The selected source must resolve genus zero and one; the empty or nonempty rational-point locus;
non-algebraically-closed and inseparable fields; base change and descent; singular, reducible, or
nonproper curves; degree zero versus degree `g` Picard components; divisors versus line bundles;
effective divisors and symmetric powers of degree below, equal to, or above the genus; dependence on
the base point and translation; trivial Jacobians; injectivity failures in genus zero; and whether
the result concerns scheme points, geometric points, complex analytic spaces, or functors of
points.

## Neighbor and substitution exclusions

- `THM-M-0238` separately owns the catalog's Abel-theorem target. A divisor-kernel statement cannot
  silently replace this target.
- `THM-M-0239` separately owns Jacobi inversion. Surjectivity of a symmetric-power map cannot
  silently replace this target.
- A generic existence theorem for an abelian variety, a ring-level Picard group, or a theorem about
  one elliptic curve is substrate rather than a general Abel-Jacobi theorem.
- Mathlib declarations under `WeierstrassCurve.Jacobian` concern weighted Jacobian coordinates on a
  Weierstrass curve; the shared word `Jacobian` provides no target or proof credit.
- A structure or hypothesis storing the desired Jacobian, Picard equivalence, Abel-Jacobi map, or
  universal property provides no proof of its existence or properties.
- A complex-torus special case cannot replace a source-selected algebraic theorem, nor conversely,
  without checked transports.
- The untrusted `已验证` label, inspected source leads, and API probe provide no source-fidelity or
  proof credit.

## Formal boundary

Pinned mathlib exposes schemes, smooth and proper morphisms, Weierstrass curves, elliptic-curve
points in Jacobian coordinates, and a Picard group of invertible modules over a commutative ring.
The latter explicitly leaves connection to invertible sheaves on `Spec R` as future work. The probe
authenticates adjacent interfaces only. It neither defines the Jacobian variety or Picard functor of
a general smooth projective curve nor states or proves an Abel-Jacobi result.
