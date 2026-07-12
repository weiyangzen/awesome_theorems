# Source-statement crosswalk

## Repository authority and provenance

`Docs/researches/math_theorems.md:1571-1576` is the sole repository source record. It supplies the
Chinese title "Poincare disk model", attribution to Henri Poincare, the year 1882, the complete
gloss "a conformal model of hyperbolic geometry", high importance, and status `已验证`
("verified"). All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no publication, edition, section,
page, theorem, definitions, formula, quantifiers, hypotheses, conclusion, proof, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:6054-6079` repeats the gloss while explicitly leaving the target formal
system, logical foundation, precise definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine status, and artifact links open. Its generic assertion
that a closed result is believed to exist is planning metadata, not evidence. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

The source classification is therefore `H5`: the received record is not a stable proposition.
This classification neither refutes nor calls open a source-selected theorem about the Poincare
disk. A later statement phase must redirect the topic label to an exact, reviewed proposition
before ordinary theorem-proof execution.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "disk" | open unit disk in `Complex`, a real disk, or an abstract charted surface | `Complex.UnitDisc`, `Metric.ball (0 : Complex) 1`, or a manifold type | pinned unit-disk API probed; representation not selected |
| "Poincare" | a normalized hyperbolic metric, distance, line element, or full model package | a new metric/Riemannian structure and definitions, or a checked imported package | absent from the catalog and from the pinned unit-disk API |
| "hyperbolic geometry" | a synthetic plane, constant-curvature surface, or another analytic model | axiom structure, curvature theorem, or explicit comparison type | comparison object and model relation open |
| "model" | satisfaction of axioms, an isometry, or a structure with proved laws | a proposition relating the disk construction to the selected geometry | no conclusion supplied |
| "conformal" | angle preservation or a positive pointwise scalar relation between metrics | generic `ConformalAt`, a Riemannian conformality predicate, or a checked custom definition | orientation and encoding open; generic mathlib conformality includes antiholomorphic maps |
| common distance formula | a formula such as an `arsinh`, `artanh`, logarithmic, or cross-ratio expression | equality for a source-frozen disk distance | not present in the source; formulas and scale are not interchangeable by default |
| common geodesic description | diameters and boundary-orthogonal circular arcs | a geodesic predicate plus Euclidean circle/line geometry | not present in the source; root membership open |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as H or M evidence |

## Candidate normalization not credited

A familiar modern bundle places a metric proportional to
`4 * |dz|^2 / (1 - |z|^2)^2` on the open unit disk, then proves constant Gaussian curvature `-1`,
completeness, Euclidean conformality, and a geodesic description by diameters and circles
orthogonal to the boundary. This is a useful source-search lead only. The repository does not say
which normalization or which subset of that bundle constitutes its theorem, and no source passage
has been reviewed. It is therefore not the canonical statement.

## Lean intake boundary

At the pinned mathlib revision, `Mathlib.Analysis.Complex.UnitDisc.Basic` is titled "Poincare disc"
and defines `Complex.UnitDisc := Metric.ball (0 : Complex) 1`; it does not install a hyperbolic
metric or state a disk-model theorem. Generic conformality APIs elaborate, while
`Mathlib.Analysis.Complex.UpperHalfPlane.Metric` defines a hyperbolic distance on the separately
cataloged upper-half-plane model. No transport from that metric to the disk is credited.

The next phase must first select and hash an immutable primary or authoritative source, transcribe
all incorporated definitions and the exact proposition, map every premise and conclusion, inspect
corrections and errata, reconcile neighboring model targets, and obtain independent review. Only
then may it freeze minimal imports, a canonical Lean expression and environment fingerprint,
checked alternate-form transports, and the required semantic mutation tests. No H0, exact Lean
statement, anchor audit, proof, or theorem completion is claimed here.
