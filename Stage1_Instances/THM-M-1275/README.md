# THM-M-1275 rev-5.6 intake

This directory is the `planned` intake instance for the Yamabe existence theorem. The manifest's
untrusted `已验证` label is discovery metadata and grants no human-source or machine-proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Every smooth conformal class on a compact connected boundaryless manifold of dimension at least three contains a constant-scalar-curvature metric | The statement phase must choose and elaborate the exact Lean representation |
| Geometric data | Smooth manifold, Riemannian metric, conformal rescaling by a positive smooth function | Regularity, dimension, boundary, connectedness, and exponent conventions are explicit |
| Analytic form | Positive solution of the conformal-Laplacian Yamabe equation | Coefficient and Laplacian-sign conventions are not yet frozen |
| Variational form | Attainment of the Yamabe constant by a positive minimizer | Equivalence to the metric statement is not yet checked |
| Historical cases | Yamabe's program, Trudinger's repair, Aubin's strict-inequality cases, Schoen's remaining cases | These are source/proof-architecture candidates, not closed nodes |
| Exclusions | Dimension two, noncompact manifolds, manifolds with boundary, componentwise disconnected variants | Separate theorems; none may be substituted for the root |
| Machine surface | Lean 4 and pinned mathlib | No declaration, expression hash, environment fingerprint, or candidate proof has been accepted |

The source-to-claim relationship and historical correction boundary are recorded in
`source_statement_crosswalk.md`. Structured binders, hypotheses, exclusions, profiles, and the
provisional target boundary are recorded in `intake.json`.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Only intake is self-tested here. Every later node remains open and retains its blueprint dependency.

## Intake verdict

Lifecycle remains `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem
gate is exact Lean statement elaboration. In particular, mathlib API availability for the required
differential geometry and nonlinear elliptic PDE is not assumed. The theorem is not complete.

## Validation

The exact commands and results in `validation.md` establish target membership, rev-5.6 structural
consistency, JSON syntax, dossier-local references, and clean patch formatting only.
