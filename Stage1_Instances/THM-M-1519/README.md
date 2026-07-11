# THM-M-1519 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Poisson bracket target. The repository
source gives the coordinate formula and says that it describes the algebraic structure of
observables. That is a definition plus an informal role, not a uniquely quantified theorem. Intake
therefore preserves the source wording and records the missing theorem choice rather than silently
substituting the distinct Poisson theorem about constants of motion.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source root | The canonical-coordinate operation `{f,g} = sum_i (partial_qi f partial_pi g - partial_pi f partial_qi g)` | A definition alone has no proposition to prove; the exact root law or characterization remains open |
| Phase space | A finite-dimensional canonical phase space with coordinate pairs `(q_i,p_i)` | Base field, dimension/index type, smoothness class, and global versus chart-local semantics are unspecified |
| Observable space | Scalar-valued differentiable functions closed under the bracket | Function domain, differentiability order, and closure hypotheses must be frozen later |
| Algebra laws | Bilinearity, antisymmetry, Leibniz rule, and Jacobi identity are candidate meanings of "algebraic structure" | No individual law or conjunction is credited as the source theorem |
| Coordinate independence | Intrinsic symplectic/Poisson-manifold bracket and agreement with the displayed coordinate formula | Not inserted into the root without a source-backed choice |
| Dynamics | Relation to Hamiltonian evolution and the theorem that brackets of constants of motion remain constant | Explicitly a separate repository entry ("Poisson theorem"), not this target |
| Formal system | Lean 4 plus pinned mathlib | Exact imports, declaration, toolchain, and environment fingerprint belong to the statement phase |

Provisional scope nodes are `PB-ROOT` (exact proposition), `PB-DATA` (phase space and observables),
`PB-DEF` (coordinate or intrinsic bracket), `PB-LAWS` (selected algebra laws), `PB-CHART`
(coordinate/intrinsic agreement), and `PB-EDGE` (zero-dimensional and constant-observable cases).
They are discovery scope, not a frozen obligation registry or proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
exact-statement identity: the source record does not say which proposition about the displayed
operation is the theorem. No Lean declaration, source closure, or theorem completion is claimed.

## Validation

The exact commands and results are recorded in `validation.md`. They establish manifest membership,
repository-standard consistency, JSON syntax, and dossier hygiene only. Master acceptance remains
outstanding.
