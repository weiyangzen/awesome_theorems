# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1550-1555` supplies exactly the title `双曲余弦定理`, attribution
to multiple mathematicians, the nineteenth century, the gloss `双曲三角形边与角的关系` ("a
relation between the sides and angles of a hyperbolic triangle"), high importance, and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record supplies no bibliography, model,
curvature, formula, definitions, binders, hypotheses, proof boundary, corrections, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:5973-5999` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected modern source lead

Immanuel Asmus, *Duality between Hyperbolic and de Sitter Geometry*, arXiv:0810.5303v2
(`[math.DG]`, submitted 2008-10-29, version dated 2008-10-30), was inspected from the immutable
arXiv PDF. Its notation section defines the normalized hyperboloid `H^2`, Minkowski product,
hyperbolic distance `d_H(x,y) = arcosh(-<<x,y>>)` and generalized segments. Section 3 defines
non-degenerate hyperbolic triangles, side lengths, tangent vectors, and angles. Theorem 5.1,
printed pages 22-23, states for a hyperbolic or antipodal-hyperbolic triangle with the usual
opposite-side labels:

```text
cosh(a) = cosh(b) cosh(c) - cos(alpha) sinh(b) sinh(c)
cosh(b) = cosh(a) cosh(c) - cos(beta)  sinh(a) sinh(c)
cosh(c) = cosh(a) cosh(b) - cos(gamma) sinh(a) sinh(b).
```

The proof computes the Minkowski inner product of the unit tangent vectors at a vertex, substitutes
the point inner products determined by the three side lengths, and obtains the first equation;
renaming vertices supplies the other two. The observed PDF SHA-256 is
`177baa15f7605896660eab44526c46f09c546606014f970a43de4e5545e422b6`.

This is a credible complete modern proof lead, but it is not cited by the catalog. A primary
historical source, source-identity decision, correction/errata review, approved treatment of
degenerate cases, and independent review remain open. The PDF was inspected but not added to the
repository. The source classification is therefore provisional `H1`, not `H0`.

## Clause crosswalk

| Catalog component | Inspected source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "hyperbolic triangle" | non-degenerate triangle in normalized `H^2` (or `-H^2`) | a new triangle predicate over an approved hyperbolic-plane model | model and definition transport open |
| "sides" | positive hyperbolic distances `a`, `b`, `c` between the labeled vertices | `dist` after a selected metric/model plus opposite-side equations | labeling and nondegeneracy open |
| "angles" | angles from Minkowski products of unit tangent vectors | an approved angle predicate or tangent-space angle | exact encoding and range open |
| "relation" | three cyclic side-law equations in Theorem 5.1 | one equation or a conjunction of cyclic equations | root conclusion not selected by catalog |
| curvature scale | normalized hyperboloid, hence curvature `-1` convention | explicit scale/profile or normalized model | absent from catalog |
| degenerate triangles | excluded from the main theorem; discussed separately after Theorem 5.9 | explicit exclusion or a separate boundary theorem | catalog policy absent |
| `已验证` | untrusted inventory label | source review and kernel receipt would be required | no H0 or M credit |

## Pinned Lean boundary

Pinned mathlib contains real hyperbolic trigonometric identities such as `Real.cosh_sub` and
`Real.cosh_sq_sub_sinh_sq`, and an actual Poincare distance on `UpperHalfPlane` with
`UpperHalfPlane.cosh_dist`. It also contains the Euclidean theorem
`InnerProductGeometry.norm_sub_sq_eq_norm_sq_add_norm_sq_sub_two_mul_norm_mul_norm_mul_cos_angle`.
These declarations authenticate useful substrate and an explicit non-substitute. They do not
define a hyperbolic triangle or angle and do not state the three-point hyperbolic cosine law.

A bounded search of repo-local Lean and pinned mathlib found no exact hyperbolic-triangle cosine-law
declaration. This is intake discovery only, not the later immutable anchor audit and not a global
absence theorem.

## Source gate

Before leaving `H1`, reviewers must select an accepted source edition and exact root proposition,
map all definitions, binders, hypotheses, conclusions, model and curvature conventions, cyclic
forms, and boundary cases, audit corrections and historical attribution, and independently approve
fidelity to `THM-M-0215`. The statement phase must then freeze minimal imports, an elaborated Lean
expression and environment fingerprint, checked model/label transports, and the required removed-
hypothesis, changed-domain, binder-scope, and boundary-case mutations.
