# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1506-1511` supplies exactly the title `笛卡尔圆定理`, attribution
to Rene Descartes, the year 1643, the gloss `四圆相切的曲率关系` ("the curvature relation of four
tangent circles"), importance `中`, and status `已验证`. Git blame places all six uncited lines at
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
definitions, ordered binders, hypotheses, proof boundary, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:5806-5831` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 target manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected modern source lead

Jeffrey C. Lagarias, Colin L. Mallows, and Allan R. Wilks, *Beyond the Descartes Circle Theorem*,
American Mathematical Monthly 109 (2002), 338-361, DOI
`10.1080/00029890.2002.11920896`, was inspected through arXiv `math/0101066v1` on 2026-07-13.
The observed 25-page PDF has SHA-256
`b5a2da8a0c2aa594084afd2180ac427be3ea9dc862ac922c7ae43f9774372858`.

The abstract gives the positive-radius, disjoint-interior formulation. Section 1, printed page 1,
defines a Descartes configuration as four mutually tangent circles with no three having a common
tangent, permits straight lines as degenerate circles with bend zero, and states Theorem 1.1:

```text
(sum j = 1..4, bj)^2 = 2 * (sum j = 1..4, bj^2).
```

Printed page 2 explains the larger signed formulation: an oriented radius is positive for an
inward normal and negative for an outward normal; oriented curvature is its reciprocal; and the
four orientations are compatible when their oriented interiors are disjoint either directly or
after reversing all four. The identity remains valid for those oriented configurations.

This source is authoritative evidence that the catalog points to a stable theorem family, but it is
not accepted `H0`. The repository does not cite it; its full definitions, assumptions, proof, and
relationship between abstract and oriented formulations have not been independently crosswalked;
no errata or correction record was independently audited; and its historical note says Descartes'
1643 proof sketch was incomplete while Steiner (1826) and Beecroft (1842) supplied complete proofs.
No primary historical proof edition or translation was inspected or credited.

## Clause crosswalk

| Catalog component | Inspected source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "four circles" | a Descartes configuration of four plane circles, with straight-line degenerations allowed | `Fin 4 -> EuclideanGeometry.Sphere P` plus a future configuration/oriented-circle type | plane, finiteness, orientation, and line representation open |
| "tangent" | mutually tangent; no three share a common tangent; compatible oriented interiors for all configurations | `Sphere.IsExtTangent`, `Sphere.IsIntTangent`, pairwise predicates, and future signed-orientation data | source condition is not one existing predicate |
| "curvature" | `1 / r` in the ordinary case; signed reciprocal oriented radius generally; bend zero for a line | real-valued bend function with positivity, nonzero-radius, or signed/line cases | exact domain and totalization open |
| "relation" | Theorem 1.1 quadratic identity above | `((sum b)^2 = 2 * sum (b^2))` over `Fin 4` | candidate conclusion known; canonical packaging and expression not frozen |
| Descartes / 1643 | source reports the original equivalent relation and an incomplete proof sketch | provenance only | no complete Descartes proof or primary passage credited |
| `已验证` | untrusted inventory label | source review plus kernel receipts would be required | no H or M credit |

## Pinned Lean boundary

Pinned mathlib contains `EuclideanGeometry.Sphere.IsExtTangent` and `IsIntTangent` together with
`isExtTangent_iff_dist_center` and `isIntTangent_iff_dist_center`. These authenticate real
Euclidean sphere tangency and ordinary radius relations. A bounded search of pinned mathlib and
repo-local Lean found no Descartes/Soddy four-circle curvature theorem, compatible oriented-circle
model, or signed-bend construction; the only Descartes-named mathlib theorem was the unrelated rule
of signs. This is scoped discovery evidence rather than an exhaustive immutable anchor audit.

Before leaving `H1`, accountable reviewers must admit an immutable source proposition, transcribe
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary, correction,
and boundary case, audit a complete proof source and historical attribution separately, and approve
the mapping independently. Only then may the statement phase select minimal imports, fingerprint an
elaborated expression, compile checked transports, and execute the required statement mutations.
