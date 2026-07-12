# Scope map

## Included claim

- A closed, connected, orientable topological 3-manifold `M`.
- Prime decomposition of `M`, including the spherical and `S^2 x S^1` factors governed by the
  source formulation.
- For each irreducible factor, cutting along a finite family of disjoint incompressible embedded
  tori (the JSJ decomposition).
- A geometric structure on every resulting component, modeled on one of Thurston's eight
  three-dimensional homogeneous geometries.
- The completeness and finite-volume/boundary behavior required by the selected exact formulation.

This freezes the standard closed-orientable geometrization claim as the intended human target. The
statement phase must derive all binders and hypotheses from an inspected source and must decide
whether the canonical proposition is expressed using prime and JSJ pieces, a thick-thin
decomposition, or an equivalent formulation connected by checked transports.

## Boundary decisions

- Connectedness is included for a single-root statement. A disconnected extension is a
  componentwise corollary unless the selected source states it directly.
- Orientability is included. A nonorientable version may follow through the orientable double
  cover, but it cannot silently replace or enlarge the canonical target.
- "Closed" means compact without boundary. Any compact-with-boundary formulation must specify
  boundary incompressibility and the geometry/completeness convention and then provide a checked
  transport to the closed claim.
- Exceptional and reducible cases must be represented explicitly; they may not be hidden by
  assuming the manifold is already irreducible, atoroidal, or hyperbolic.
- The eight candidate geometries are spherical, Euclidean, hyperbolic, `S^2 x R`, `H^2 x R`,
  universal-cover `SL(2,R)`, Nil, and Sol. Their Lean definitions and equivalence conventions remain
  statement-phase work.

## Explicit exclusions

- The Poincare conjecture alone or only the simply connected case.
- Hyperbolization only for atoroidal Haken 3-manifolds.
- Merely asserting that a manifold has a supplied decomposition or geometric structure as a field
  of an abstract package.
- A classification of the eight model geometries without existence of the required decomposition.
- A prose claim that Ricci flow with surgery succeeds, absent concrete manifold, flow, surgery,
  decomposition, and classification interfaces.
- The historical `GeometrizationPackage` in `S1_M_128.lean`; its proposition-valued fields assume
  the missing mathematical content and provide no statement or proof closure for this target.

## Expected formal surface

An exact target will require concrete APIs for topological/smooth 3-manifolds, embedded spheres and
tori, connected sums, irreducibility, incompressibility, cutting and reconstruction, JSJ pieces,
locally homogeneous Riemannian structures, and the eight model geometries. A proof via Perelman's
route additionally requires Ricci flow with surgery and the analytic-to-topological classification
bridge. Missing APIs must be recorded as blockers rather than replaced by abstract assumed fields.
