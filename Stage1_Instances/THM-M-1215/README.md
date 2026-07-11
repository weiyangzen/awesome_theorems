# THM-M-1215 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the catalogue entry "Bourgain
well-posedness theorem." The catalogue supplies only "well-posedness of periodic NLS" and a
1993 attribution. That wording does not determine a unique equation, spatial dimension,
nonlinearity, regularity range, or well-posedness conclusion. The likely primary source is
Bourgain's 1993 GAFA paper on periodic nonlinear Schrodinger equations, but selecting one of its
results as the canonical theorem requires source-level statement work.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Equation family | nonlinear Schrodinger evolution on a torus | sign, power, coefficients, and dimension are unresolved |
| Initial data | a periodic Sobolev space `H^s(T^d)` | `d`, `s`, real/complex model, and norm convention are unresolved |
| Conclusion | a Hadamard well-posedness package | local/global, lifespan, uniqueness class, persistence, and dependence strength are unresolved |
| Analytic route | Fourier restriction/Bourgain spaces, multilinear estimates, fixed point, and conservation where applicable | architecture only; no proof credit |
| Lean surface | no exact repo-local declaration identified | statement phase must construct and elaborate a concrete PDE proposition |
| Foundations | Lean 4 kernel plus pinned mathlib | toolchain, imports, analytic primitives, axioms, and dependency closure remain open |

The initial proof-package scope includes the exact PDE and solution notion, periodic Fourier and
Sobolev models, the relevant restriction-space estimates, the local construction and uniqueness
argument, continuous dependence, and any conservation/iteration argument needed by the selected
source theorem. No variant receives proof credit at intake.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. `H1` means that a plausible
primary paper has been identified but no theorem/page/assumption/errata audit is accepted. `M4`
records that the catalogue phrase is underdetermined and no exact Lean target exists. The first
failed gate is the exact statement gate. This intake neither validates the historical "verified"
label nor claims theorem completion.

Exact intake checks are recorded in `validation.md`.
