# THM-M-1280 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the solution of the Yamabe problem. The
Stage0 phrase "Yamabe conjecture proof" is expanded here into a proposition rather than treated as
evidence that the proposition is formalized.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Every smooth closed Riemannian manifold of dimension at least three has a conformal metric of constant scalar curvature | Connectedness and the representation of dimension must be settled by the statement phase |
| Conformal form | A positive smooth `u` and metric `u^(4/(n-2)) g` | Fractional powers, metric positivity, and scalar curvature lack a frozen Lean encoding |
| PDE form | The conformal Laplacian Yamabe equation with a constant multiplier | Constants and sign conventions require a checked transport |
| Variational form | Attainment of the conformal-class Yamabe constant | Sobolev space, normalization, regularity, and equivalence are later obligations |
| Boundary cases | Dimension below three, boundary, noncompactness, and disconnectedness | Excluded or explicitly unresolved; no generalization is implied |
| Historical branches | Yamabe's variational setup, Trudinger's repair, Aubin's strict-inequality cases, Schoen's remaining locally conformally flat case | Source-to-obligation audit is not performed in intake |
| Foundations | Lean 4 kernel, pinned mathlib, differential geometry and nonlinear analysis | No usable formal root declaration was identified or credited |

The structured claim, ordered hypotheses, candidate equivalent formulations, and exclusions are in
`intake.json`. Source genealogy and statement mismatches are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate: there is no canonical declaration, elaborated expression hash,
environment fingerprint, checked transport, or mutation test. The theorem is not complete.

## Validation

The exact commands and results in `validation.md` establish manifest membership, repository
standard consistency, JSON syntax, local reference integrity, and clean patch formatting only.
They are intake evidence, not kernel evidence for the theorem.
