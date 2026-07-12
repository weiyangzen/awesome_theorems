# THM-M-1036 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for existence and uniqueness of
solutions to stochastic differential equations. The historical `S1_M_229.lean`
file is a discovery input only and receives no statement or proof credit here.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human claim | strong existence and pathwise uniqueness for an Ito SDE under regularity assumptions | The manifest does not identify a source edition or theorem number |
| Model | finite-dimensional Brownian SDE `dX_t = b(t,X_t) dt + sigma(t,X_t) dW_t` with an initial condition | Dimensions, time horizon, and deterministic versus random coefficients remain to be frozen |
| Regularity | a standard global-Lipschitz plus linear-growth sufficient condition | Local-Lipschitz/non-explosion variants are not silently identified with this claim |
| Conclusion | an adapted strong solution satisfying the integral equation, unique up to the source-selected indistinguishability convention | Weak existence, uniqueness in law, maximal solutions, and numerical approximation are excluded |
| Lean boundary | probability measures, filtrations, adapted processes, Bochner integration, and a Brownian stochastic integral | No repo-local general Ito-integral/SDE API has been accepted at intake |

The canonical human claim and unresolved choices are recorded in `intake.json`.
The mapping from the repository label to candidate primary-source formulations is
in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first
failed theorem-completion gate is proof/integration closure. The statement phase
has now frozen and elaborated the conservative finite-dimensional global-
Lipschitz target in `Statement.lean`; see `statement.json` and
`statement-validation.md`. Primary-source page-level review is still open, so
no H0 claim is made. The theorem is not complete.

## Validation

The commands and exact results for this dossier are recorded in `validation.md`.
They establish target membership, standard consistency, JSON syntax, and local
artifact integrity only; no Lean kernel closure is claimed.

The immutable-revision formal-candidate inventory is recorded in
`anchor-audit.json` and `anchor-audit-validation.md`. It found useful pinned
mathlib and external Brownian-process substrate, but no exact terminal Lean 4
SDE existence-and-uniqueness theorem. Those anchors receive no machine proof
credit, and the root remains `[H2, M4, R3]`.
