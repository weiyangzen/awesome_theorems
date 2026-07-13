# Source-statement crosswalk

## Repository authority and provenance

`Docs/researches/math_theorems.md:1557-1562` is the sole repository source record. It gives the
Chinese title "Gauss-Bonnet theorem", attributes it to Carl Gauss and Pierre Bonnet, gives 1848,
and supplies the complete gloss "the relationship between a surface's total curvature and
topology", high importance, and status `已验证` ("verified"). All six uncited lines originate at
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no publication,
edition, theorem, section, page, definitions, quantifiers, formula, hypotheses, conclusion, proof,
correction history, reviewer, or formal artifact. The attribution and date remain unverified
catalog metadata rather than primary-source provenance.

`Docs/Stage0_Blueprint.md:6000-6025` repeats the gloss and explicitly leaves the target formal
system, logical foundation, precise definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine status, and artifact links open. Its generic assertion
that a closed result is believed to exist is planning metadata, not evidence. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted` and resets this target to
`L0 / rework_required`.

The source classification is therefore provisional `H1`: the gloss recognizes the classical,
historically proved Gauss-Bonnet theorem family, but no exact source, variant, assumptions, proof,
errata mapping, or independent review is accepted. The next phase must select one exact reviewed
proposition before statement elaboration or ordinary theorem-proof execution.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "surface" | abstract Riemannian two-manifold or embedded regular surface | manifold/model-with-corners data, dimension condition, metric, orientation | representation and assumptions not selected |
| "total curvature" | signed `integral K dA`, absolute `integral abs(K) dA`, a scalar-curvature normalization, or an extrinsic quantity; possibly with boundary/corner corrections | selected curvature, area measure/form, manifold integral, boundary integral, finite sums | title suggests the signed Gaussian version, but no formula or normalization is source-selected; recorded queries found no end-to-end API |
| "topology" | Euler characteristic of the same surface | homology/cohomology/cell representation plus invariant bridge | invariant representation and scalar coercions open |
| "relationship" | equality to `2 * pi * chi`, or another source-defined statement | an exact typed equality with all side conditions | no truth-valued conclusion supplied |
| "Gauss-Bonnet" | closed, smooth-boundary, or corner-corrected theorem | distinct propositions and obligation trees | title alone cannot select among variants |
| `已验证` | untrusted inventory label | no proposition or proof object | explicitly rejected as H or M evidence |

## Candidate formulations not credited

A familiar modern closed-surface formulation says that for a compact oriented boundaryless
Riemannian two-manifold `M`, the integral of Gaussian curvature against area equals
`2 * pi * chi(M)`. A smooth-boundary formulation adds the integral of signed geodesic curvature,
and a piecewise-smooth formulation also adds exterior-angle terms. These are source-search leads,
not alternate encodings already shown equivalent. The repository does not select their domain,
normalization, or boundary policy, and no immutable passage has been independently reviewed.

The higher-dimensional Chern-Gauss-Bonnet theorem uses a normalized Pfaffian Euler form and is
separately cataloged under multiple IDs. It is neither the received two-dimensional claim nor a
credited generalization transport for this target.

The manifest's "non-Euclidean geometry" category is metadata, not a premise restricting the
surface to constant negative curvature. The separately cataloged hyperbolic-area formula is at most
a candidate consequence or special case after checked composition.

## Lean intake boundary

The pinned Riemannian API elaborates the generic manifold context. The pinned homological-complex
API elaborates `HomologicalComplex.eulerChar`, whose documentation explicitly defines an
alternating finrank sum for a supplied complex; it does not construct the topological Euler
characteristic of a surface. A bounded repository and pinned-mathlib search found no exact
Gauss-Bonnet declaration, no Gaussian/geodesic curvature vocabulary, and no end-to-end bridge.
This is intake discovery only, not an exhaustive anchor audit or proof of global absence.

The statement phase must pin immutable source bytes, transcribe every incorporated definition and
the exact proposition, map assumptions and conclusions, inspect corrections and errata, resolve
the closed/boundary/corner variants, and obtain independent review. Only then may it freeze minimal
imports, a canonical Lean expression and environment fingerprint, checked alternate-form
transports, and the required removed-hypothesis, changed-domain, binder-scope, and boundary-case
mutations. No H0, exact Lean statement, anchor audit, proof, or theorem completion is claimed here.
