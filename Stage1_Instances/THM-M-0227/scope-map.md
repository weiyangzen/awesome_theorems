# Scope map

## Preserved theorem family

- A domain in the complex plane, with its exact source definition and inherited topology fixed
  before formalization.
- Simple connectedness of that domain in the source's sense.
- The open unit disk as the codomain.
- Existence of a conformal equivalence, ordinarily represented by a bijective holomorphic map with
  holomorphic inverse after the exact source statement and encoding are accepted.

These bullets delimit the recognizable Riemann-mapping theorem family. They are not an accepted
canonical statement or a proof.

## Decisions required at statement freeze

1. Select an immutable primary or authoritative source edition and exact theorem/definition
   locators, including incorporated definitions, assumptions, corrections, errata, and an
   independent source review.
2. Decide whether "domain" is a defined term that already supplies nonemptiness, openness, and
   connectedness, or whether those hypotheses must be explicit Lean binders.
3. Fix the ambient space. The classical planar theorem concerns a proper subset of `Complex`; a
   simply connected Riemann surface or a complement in the Riemann sphere is a different target.
4. Make properness explicit. The whole complex plane is simply connected but is not
   biholomorphic to the unit disk, so omitting this boundary changes the truth value.
5. Freeze the simple-connectedness encoding. Mathlib's `IsSimplyConnected` for a set includes
   path-connected nonemptiness through the subtype topology; it must be crosswalked to the
   source's convention rather than matched by name alone.
6. Freeze "conformal equivalence": ambient functions restricted to sets, a homeomorphism between
   subtypes with analytic forward and inverse maps, or another representation. Pointwise
   nonzero-derivative conformality alone is not a bijective equivalence.
7. Decide whether the conclusion is existence only or also the normalized uniqueness statement
   obtained after fixing a base point and a positive derivative. Automorphism uniqueness is not
   part of the catalog gloss.
8. Resolve boundary and degenerate cases: the empty set, singleton or non-open sets, the whole
   plane, the unit disk itself, unbounded proper domains, boundary points, and the orientation-
   reversing antiholomorphic reading of "conformal."

## Explicit exclusions

- The uniformization theorem for arbitrary simply connected Riemann surfaces.
- A theorem only for bounded, Jordan, convex, polygonal, or smoothly bounded domains unless a
  checked reduction covers every domain in the accepted source target.
- The Schwarz lemma, open mapping theorem, inverse function theorem, or existence of local
  conformal charts as a substitute for the global equivalence.
- A homeomorphism without holomorphic forward and inverse maps, or a holomorphic map lacking
  injectivity or surjectivity.
- A structure or hypothesis that assumes the desired equivalence and then merely projects it.
- Caratheodory boundary extension, prime-end correspondence, normalized uniqueness, boundary
  regularity, or an explicit formula unless the selected source root includes it.
- The repository label `已验证`, a theorem name, or adjacent API elaboration as H0 or M0 evidence.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides `Complex.UnitDisc`,
`IsSimplyConnected`, open-set predicates, analytic predicates, homeomorphisms, and local conformal
predicates. A bounded local name search found no exact Riemann-mapping or biholomorphic-unit-disk
declaration in pinned mathlib or the repo-local Lean sources. This is intake discovery only, not an
exhaustive anchor audit or a global absence claim.
