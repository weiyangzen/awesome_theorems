# Source-statement crosswalk

## Repository authority and provenance

`Docs/researches/math_theorems.md:1543-1548` is the complete repository source record. It supplies
the title `球面几何余弦定理`, attribution `众多数学家`, date `古代`, gloss
`球面三角形边与角的关系`, high importance, and status `已验证`. All six uncited lines originate
at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no publication, edition,
section, page, theorem number, definitions, formula, quantifiers, hypotheses, conclusion, proof,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:5946-5971` repeats the gloss while explicitly leaving the target formal
system, exact definitions and premises, proof route, dependencies, equivalent formulations,
axioms, machine status, and artifact links open. Its generic planning language is not evidence.
The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

The source classification is therefore `H5`: the received gloss is not one stable truth-valued
proposition. This does not say that the classical spherical cosine rules are false or open. A later
statement/source review must redirect the family label to one exact reviewed proposition.

## Crosswalk

| Repository phrase | Candidate mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `球面三角形` / spherical triangle | three points joined by selected great-circle geodesic arcs on a round sphere | sphere subtype, vertex triple, arc/geodesic data, and validity predicate | subject identified; model and validity conditions open |
| `边` / sides | central angles, minor/oriented arcs, or intrinsic lengths `R * a` | vector angle or a new intrinsic spherical distance/arc-length encoding | convention and ranges open |
| `角` / angles | interior tangent angle, oriented angle, exterior angle, or plane-normal angle | tangent vectors and `InnerProductGeometry.angle`, or a checked equivalent | definition and orientation open |
| `关系` / relation | side cosine rule, dual angle rule, cyclic family, or equivalence | exact real trigonometric equality/equalities | no formula or root bundle selected |
| `球面几何余弦定理` / spherical law of cosines | conventional theorem-family name | source-normalized target and checked alternate transports | family identity only |
| `已验证` | inherited catalog status | no proposition or proof object | explicitly rejected as H or M evidence |

## Secondary discovery leads, not credited sources

The Encyclopedia of Mathematics article "Spherical trigonometry" displays both
`cos a = cos b cos c + sin b sin c cos A` and the dual angle identity, and states that `a`, `b`,
and `c` are central angles while the corresponding arc lengths are `aR`, `bR`, and `cR`. Eric W.
Weisstein's MathWorld page "Spherical Trigonometry" similarly presents the cyclic side and angle
cosine rules and cites textbook pages. These pages confirm why the catalog gloss is ambiguous and
provide leads for source discovery only. Neither is an admitted primary proof source, neither is
independently reviewed here, and neither upgrades `H5` or freezes the canonical statement.

## Lean intake boundary

Pinned mathlib contains nearby declarations such as `EuclideanGeometry.Sphere`,
`EuclideanGeometry.Sphere.oangle_center_eq_two_zsmul_oangle`,
`InnerProductGeometry.cos_angle`, and the Euclidean `EuclideanGeometry.law_cos`. The sphere type is
an ambient Euclidean center/radius bundle coercing to a point set; a subtype of that set inherits
ambient chord distance, not intrinsic arc distance. The Euclidean cosine theorem does not state the
spherical formula. No exact spherical-law candidate, terminal body, or checked transport is
credited.

The statement phase must first select and hash an immutable authoritative source, transcribe its
definitions and exact theorem, map every premise and conclusion, inspect corrections and errata,
and obtain independent review. Only then may it freeze the minimal imports, canonical Lean
expression and environment fingerprint, alternate-form transports, and the required removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations. No H0, exact Lean
statement, anchor audit, proof, or theorem completion is claimed here.
