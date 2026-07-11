# THM-M-1152 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for Perron's method. The
repository source says only "the upper-solution/lower-solution method for the
Dirichlet problem." That wording identifies a method, not one exact theorem.
In particular, it leaves open the operator, domain and boundary hypotheses,
data class, generalized solution convention, and whether boundary attainment
is part of the root. Intake preserves those choices instead of silently
substituting a convenient envelope theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A source-backed Perron theorem for a specified Dirichlet problem | No unique proposition is selected until operator, domain, data, and conclusion are fixed |
| Perron classes | Upper/lower generalized solutions, boundary inequalities, and comparison order | Semicontinuity and boundary-limit conventions remain open |
| Envelope | Pointwise infimum of the upper class and/or supremum of the lower class | Nonemptiness, finiteness, and equality are not assumed |
| Interior argument | Harmonic replacement, directed approximation, and harmonicity of the envelope | The analytic infrastructure and dimension assumptions remain open |
| Boundary argument | Barriers, regular boundary points, and attainment of boundary data | Full-domain regularity must not be inferred from the method alone |
| Uniqueness | Maximum/comparison principle and coincidence of upper/lower solutions | Depends on the selected operator and solution class |
| Formal system | Lean 4 plus pinned mathlib | Exact imports, declaration, expression hash, and environment fingerprint belong to the statement phase |

The provisional architecture is recorded as `PER-CLASS`, `PER-ENV`,
`PER-LIFT`, `PER-HARM`, `PER-BDY`, and `PER-UNIQ`. These labels are a scope map,
not a frozen obligation registry and provide no proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first
failed theorem gate is exact-statement identity. The dependent statement phase
must choose a primary-source-backed version and freeze every binder,
hypothesis, boundary convention, and conclusion before inspecting Lean proof
closure. No theorem completion is claimed.

## Validation

Exact intake validation commands and results are in `validation.md`. They cover
manifest membership, repository structural checks, JSON syntax, and dossier
hygiene only. Master acceptance remains outstanding.
