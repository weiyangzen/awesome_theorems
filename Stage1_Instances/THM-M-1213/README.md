# THM-M-1213 rev-5.6 intake

This is a `planned` instance for the repository entry “Ginibre-Velo theorem.” The only supplied
mathematical wording is “local well-posedness of NLS.” That label names a family of results, not a
unique theorem, so this intake fails closed rather than selecting convenient parameters.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source identity | Ginibre and Velo, 1979, NLS local well-posedness | Exact paper/theorem and errata are not pinned |
| Equation | A nonlinear Schrodinger Cauchy problem | Sign, nonlinearity, dimension, and domain are unresolved |
| Data and solutions | Data-to-solution existence, uniqueness, and continuous dependence locally in time | Function spaces, topology, and solution notion are unresolved |
| Time | A data-dependent local interval | Lifespan and maximality conventions are unresolved |
| Formal surface | Lean 4 and pinned mathlib | No declaration or exact expression is nominated |
| Trust | Kernel-checked proof under a versioned foundation profile | Toolchain, imports, axioms, and TCB remain open |

The later statement phase must first disambiguate the primary theorem and freeze all analytic
parameters. A generic fixed-point theorem or an arbitrary modern NLS theorem is not an acceptable
substitute.

## Intake verdict

Lifecycle is `planned`; root vector is `[H3, M4, R4]`. The first failed gate is exact source
statement identification. No proof state is accepted and `theorem_complete` is false.

## Validation

The exact commands and results establishing manifest membership, structural consistency, JSON
syntax, and dossier-local integrity are recorded in `validation.md`.
