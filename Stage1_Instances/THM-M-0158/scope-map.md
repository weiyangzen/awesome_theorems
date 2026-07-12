# Scope map

## Included claim

Let `U` be an open subset of `R^2`, let `x : U -> R^3` be a sufficiently differentiable regular
parametrized surface, and let `N : U -> R^3` be a sufficiently differentiable chosen unit normal.
At a point, write

```text
I  = [[E, F], [F, G]]
II = [[e, f], [f, g]],
```

where `E = <x_u,x_u>`, `F = <x_u,x_v>`, and `G = <x_v,x_v>`. Provisionally use the convention
`e = <x_uu,N>`, `f = <x_uv,N>`, and `g = <x_vv,N>`. Regularity makes `I` invertible. The included
claim says that `N_u` and `N_v` lie in the span of `x_u,x_v`, and their coordinate columns satisfy

```text
coefficients(N_u, N_v) = - I^-1 * II.
```

Equivalently, for the shape operator convention `S = -dN`, its matrix in the coordinate tangent
basis is `I^-1 * II`. This invariant form is an alternate encoding, not permission to define `S`
so that the desired result becomes a field or definitional tautology.

## Domains and binders to freeze at statement phase

- Exact smoothness needed for `x` and `N`, and whether normal differentiability is derived from a
  cross-product construction or assumed explicitly.
- A point in an open parameter domain, with the local-coordinate derivatives evaluated there.
- Regularity as linear independence of `x_u,x_v`, equivalently positivity of `EG - F^2` in this
  Euclidean setting, with the exact checked bridge made explicit.
- Orientation dependence: replacing `N` by `-N` reverses `II` and the normal derivative but
  preserves the equation.
- Matrix row/column order, signs, derivative conventions, universes, and all typeclass assumptions.

## Boundary cases

The canonical local formula excludes a singular parametrization and points outside the open
parameter domain. It does not require a globally orientable surface; a local chosen unit normal is
enough. Empty domains make a globally quantified wrapper vacuous and must be mutation-tested rather
than used as evidence for the pointwise theorem. A later source audit must decide whether a primary
formulation instead uses an abstract oriented surface and tangent-space differential.

## Explicit exclusions

- The Gauss map theorem, Gauss curvature formula, Gauss equations, or Codazzi-Mainardi equations.
- A formula only for a graph, sphere, principal coordinates, or another special surface.
- The tautology `S = -dN` without deriving the coordinate relationship to `I` and `II`.
- An abstract package that stores tangency or the matrix equality as assumed data.
- A statement over arbitrary matrices detached from derivatives of a regular surface.
