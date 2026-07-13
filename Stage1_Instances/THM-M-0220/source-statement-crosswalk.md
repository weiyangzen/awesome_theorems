# Source-statement crosswalk

## Repository authority and provenance

`Docs/researches/math_theorems.md:1585-1590` is the sole repository source record. It supplies the
Chinese title "hyperbolic area formula", attribution to "many mathematicians", a nineteenth-
century date, the complete gloss "the relationship between the area of a hyperbolic triangle and
angle defect", high importance, and status `已验证` ("verified"). All six uncited lines originate
at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no
publication, edition, theorem, page, formula, definitions, normalization, quantifiers, hypotheses,
proof, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:6108-6133` repeats that gloss and calls the target a formula or identity,
while explicitly leaving the formal system, logical foundation, precise definitions and premises,
proof route, dependencies, alternate forms, axioms, machine status, and artifact links open. Its
generic planning claim that a closed result is believed to exist is not evidence. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

The source classification is therefore `H1`: a standard proved theorem family is recognizable,
but exact statement, assumptions, source edition, proof boundary, errata, and source-to-node
mapping have not been audited. This is not H0 and does not freeze either familiar formula.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "hyperbolic" | curvature `-1`, curvature `-k^2`, a selected model, or an abstract constant-curvature surface | `UpperHalfPlane`, a disk model, or future Riemannian objects | geometry and scale not selected |
| "triangle" | finite geodesic triangle, ideal or partially ideal triangle, ordered boundary, or enclosed region | a new triangle/region structure and geodesic predicate | no hyperbolic triangle API matched |
| "area" | nonnegative Riemannian volume, upper-half-plane invariant measure, or signed area | `MeasureTheory.volume`, `UpperHalfPlane.volume_def`, or a transported measure | adjacent invariant measure probed; target encoding open |
| "angle" | interior angle between geodesic tangent directions in radians | a hyperbolic tangent-angle definition or checked conformal transport | Euclidean angle API exists; no hyperbolic bridge credited |
| "angle defect" | `pi - (alpha + beta + gamma)` for a finite triangle, with extensions for ideal vertices | a real expression after angles are source-defined | catalog supplies no formula or case policy |
| common curvature `-1` form | `Area(T) = pi - (alpha + beta + gamma)` | equality for a source-frozen triangle and area | familiar candidate only; normalization not selected |
| common curvature `-k^2` form | `Area(T) = (pi - angleSum(T)) / k^2`, with `k > 0` | equality with explicit scale binder and hypotheses | familiar candidate only; not definitionally identical to the normalized form |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as H or M evidence |

## Neighbor and dependency boundary

`THM-M-0215` owns the hyperbolic cosine law; `THM-M-0216` owns a Gauss-Bonnet theorem;
`THM-M-0217`, `THM-M-0218`, and `THM-M-0219` own the Klein, Poincare disk, and Poincare
half-plane model topics. Those targets can supply future dependency or transport candidates only.
They do not confer statement identity or proof credit on `THM-M-0220`.

## Lean intake boundary

At the pinned revision, `Mathlib.Analysis.Complex.UpperHalfPlane.Metric` supplies
`UpperHalfPlane.dist_eq` and a metric-space instance.
`Mathlib.Analysis.Complex.UpperHalfPlane.Measure` defines the invariant measure by
`UpperHalfPlane.volume_def`. `Mathlib.Geometry.Euclidean.Angle.Unoriented.Affine` supplies generic
Euclidean angle vocabulary. The probe elaborates these interfaces, but none is a hyperbolic
triangle-area theorem. A bounded exact-topic search found no hyperbolic-triangle, angle-defect, or
Gauss-Bonnet declaration in pinned mathlib or the repo-local Lean tree; this is not an exhaustive
anchor audit or a global absence proof.

The statement phase must first select and hash an immutable source, transcribe all incorporated
definitions and the exact proposition, map every premise and conclusion, inspect corrections and
errata, reconcile the normalization and neighboring-target boundaries, and obtain independent
review. Only then may it freeze minimal imports, a canonical Lean expression and environment
fingerprint, checked alternate-form transports, and the required semantic mutation tests. No H0,
exact Lean statement, proof, or theorem completion is claimed here.
