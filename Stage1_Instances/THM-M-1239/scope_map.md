# Scope map

| Surface | Intake scope | Boundary |
|---|---|---|
| Identity | `THM-M-1239`, Poincare inequality | A theorem family, not an exact statement |
| Subject | PDE/Sobolev analysis | Distinct from the probability target `THM-M-0998` |
| Left side | An `L^p` quantity associated with a Sobolev function | Function itself versus deviation from its mean is unresolved |
| Right side | Expected gradient/weak-derivative control and a constant | Derivative, norm, exponent, and constant convention are absent |
| Functions | Some Sobolev class | `W^{1,p}`, `W_0^{1,p}`, smooth closure, and mean-zero subspaces are not interchangeable |
| Domain | Unspecified | Boundedness, connectedness, boundary regularity, dimension, and measure are open |
| Lean surface | Lean 4 + pinned mathlib | No expression is credited before source selection and elaboration |

## Required statement decisions

1. Pin a theorem-level source with edition, statement locator, assumptions, and errata status.
2. Fix the ambient scalar field, dimension, domain class, measure, exponent range, and Sobolev model.
3. Fix zero-trace, compact-support, or mean-zero normalization and all boundary hypotheses.
4. Specify both norms, the weak gradient, the inequality direction, and constant dependencies.
5. Treat disconnected, unbounded, zero-measure, constant-function, and endpoint cases explicitly.
6. Only then elaborate and mutation-test the exact Lean target.

## Explicit exclusions

The probability/variance Poincare inequality, Wirtinger inequality, Friedrichs inequality, a
Gaussian or discrete spectral-gap result, and the tautological assertion that some constant exists
may not substitute for this PDE/Sobolev root. Alternate forms require checked transports after the
canonical statement is frozen.
