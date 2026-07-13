# Scope map

## Preserved subject boundary

The intake preserves the recognizable family of cosine identities relating the sides and angles
of a spherical triangle. Familiar candidates include, in angular-side notation,

```text
cos a = cos b * cos c + sin b * sin c * cos A
cos A = -cos B * cos C + sin B * sin C * cos a
```

where `A` is opposite `a`. If `a`, `b`, and `c` instead denote arc lengths on a sphere of radius
`R`, the trigonometric arguments become `a / R`, `b / R`, and `c / R`. These formulas are search
and crosswalk candidates only. The repository does not select one of them as its exact claim.

## Decisions required at statement freeze

1. Select and independently review an immutable primary or authoritative source with exact
   edition, theorem/section/page or archival locator, incorporated definitions, premise mapping,
   proof boundary, corrections, and errata.
2. Decide whether the root is the cosine rule for sides, the dual rule for angles, all cyclic
   instances, an equivalence between them, or another explicitly sourced cosine formulation.
3. Fix the ambient object: the round two-sphere in real three-space, a round sphere of another
   dimension with a triangle in a great two-sphere, or an abstract constant-curvature surface.
4. Fix the radius `R > 0`, curvature, unit-sphere normalization, and whether side variables are
   central angles in radians or intrinsic geodesic arc lengths.
5. Define a spherical triangle: three vertices, selected great-circle arcs, and the required
   distinctness, non-antipodality, hemisphere, convexity, orientation, or side-range conditions.
6. Fix minor, major, or oriented arcs and the allowed side range. Points alone do not select a
   unique geodesic when antipodal, and major/minor choices can change angle conventions.
7. Define each vertex angle, for example by tangent directions of the incident great circles, and
   reconcile interior, exterior, oriented, and plane-normal conventions.
8. Freeze the vertex/side naming permutation, ordered binders, universes, coercions, all
   hypotheses, equality orientation, and exact conclusion.
9. Resolve coincident or antipodal vertices, zero radius, zero or `pi` side, collinear-on-one-great-
   circle triangles, repeated arcs, hemispherical boundary cases, and orientation reversal.
10. Select foundation, TCB, computation, and freshness profiles and compile checked transports for
    every alternate encoding that receives credit.

## Explicit exclusions

- The Euclidean planar law of cosines or a chord-length identity substituted for the spherical
  formula.
- The ambient metric on a subtype of `EuclideanGeometry.Sphere` or `Metric.sphere` treated as
  intrinsic spherical arc distance. Such a subtype inherits ambient chord distance.
- Only the central-angle identity for three unit vectors unless its relationship to the selected
  spherical sides and vertex angles is checked.
- A right-triangle specialization, small-angle approximation, navigation formula, hyperbolic
  cosine rule, sine rule, or spherical excess formula substituted for the requested root.
- A structure that stores the desired cosine identity, triangle validity, angle relationship, or
  geodesic facts as fields and then merely projects them.
- A theorem name, adjacent API elaboration, secondary web formula, or the catalog label `已验证`
  treated as exact statement identity or proof evidence.

## Neighbor boundary

`THM-M-0215` separately owns the hyperbolic law of cosines. `THM-M-0216` separately owns the
Gauss-Bonnet theorem, which can imply spherical excess in a suitable model but is not this cosine
identity. `THM-M-0193` owns the Euclidean Pythagorean theorem, and mathlib's Euclidean
`law_cos` is likewise not a substitute. No status or proof credit transfers across these targets.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.Geometry.Euclidean.Angle.Sphere` develops
angles in ambient Euclidean circles and spheres, and `Mathlib.Geometry.Euclidean.Triangle` provides
the Euclidean law of cosines. A bounded exact-topic search found no spherical-triangle cosine-law
declaration. This is an intake observation, not an exhaustive anchor audit or a global absence
claim. Minimal imports, exact target elaboration, expression/environment fingerprints, checked
transports, and semantic mutation tests belong to `S56-M-0214-STATEMENT`.
