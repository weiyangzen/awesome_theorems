# THM-M-1130 rev-5.6 intake

This is the `planned` dossier for the heat equation (`热方程`). The repository describes it as
the mathematical model of heat conduction, not as a proposition with a truth-valued conclusion.
An equation becomes a Lean theorem target only after a source fixes a domain, solution notion,
coefficients, data, regularity, and a mathematical claim about its solutions. This intake does not
silently substitute a fundamental-solution, existence, uniqueness, maximum-principle, or physical
derivation theorem. Historical `已验证` metadata supplies no source or proof credit.

## Scope map

| Surface | Intended scope | Boundary at intake |
|---|---|---|
| Equation family | A heat/diffusion PDE, schematically `partial_t u = alpha * laplacian u`, with possible source and variable coefficients | Dimension, coefficient regime, sign convention, and homogeneous versus inhomogeneous form remain open |
| Space-time domain | A time interval and spatial domain, possibly all Euclidean space or a bounded domain | Boundary regularity and initial/boundary conditions are not specified by repository metadata |
| Solution concept | Classical, weak, mild, or semigroup solution | Regularity and equality notion must be source-selected rather than conflated |
| Candidate theorem claim | A sourced result about the selected equation, such as derivation, well-posedness, characterization, or representation | No one candidate is canonical until the source-statement gate identifies the repository claim exactly |
| Exclusions | The PDE merely restated as both hypothesis and conclusion; a one-dimensional specialization; the fundamental solution (`THM-M-1132`); the maximum principle (`THM-M-1133`) | Neighboring target identities must remain distinct; a conditional Lean theorem does not empirically validate heat conduction |
| Formal system | Lean 4 plus pinned mathlib analysis APIs | No module, declaration, expression hash, or environment fingerprint is credited at intake |

## Intake verdict

Lifecycle is `planned`; provisional vector is `[H1, M3, R3]`. The first failed theorem gate is
exact source-statement identification: the available record names an equation/model but no theorem
about it. The statement phase must locate a primary-source claim and freeze one exact mathematical
proposition without broadening or substitution. No Lean theorem or theorem-completion claim is
made. The open phase DAG is in `task-dag.json`; validation evidence is in `validation.md`.
