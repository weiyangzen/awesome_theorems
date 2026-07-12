# Scope map

## Included topic boundary

- A polynomial or algebraic surface in three variables over a source-specified field.
- Intersections of its zero set with a finite Cartesian product `A x B x C`.
- A source-specified incidence bound, structural alternative, or implication between the two.
- The algebraic or local analytic group-like form that constitutes the exceptional case.

## Decisions required at statement freeze

An immutable source passage must select the theorem/version and fix:

1. the base field (for example `C` or `R`) and whether the conclusion is algebraic or analytic;
2. polynomial degree, irreducibility, squarefreeness, and nontrivial dependence on each variable;
3. cardinalities of `A`, `B`, and `C`, whether they are equal, and the exact asymptotic quantifiers;
4. the exponent, dependence of constants, and any lower-order terms in a quantitative conclusion;
5. the exceptional subvariety or finite exceptional set and the locality of coordinate charts;
6. whether the exceptional alternative is an additive normal form, a one-dimensional algebraic
   group correspondence, or another explicitly stated group-related condition; and
7. empty sets, constant/coordinate-independent polynomials, reducible surfaces, singular points,
   repeated roots, and zero-dimensional components.

Binder order and all universes must be derived from that source rather than from a convenient Lean
encoding.

## Explicit exclusions

- The Schwartz-Zippel bound or a generic polynomial-evaluation fact as a substitute.
- The Elekes sum-product theorem, the Szemeredi-Trotter theorem, or an incidence corollary.
- A later quantitative refinement presented as the 2012 structural theorem without a checked
  implication crosswalk.
- A structure that assumes the incidence estimate or group-like representation as a field.
- Replacing a complex algebraic/analytic claim by a finite-field counting theorem.
- Treating the repository label `已验证` as human-proof or kernel evidence.

No canonical Lean target is frozen at intake because the source record does not distinguish these
materially different propositions.

