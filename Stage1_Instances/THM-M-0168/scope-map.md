# Scope map

## Included claim

Let `u : R^2 -> R` be sufficiently regular. Its entire graph is

```text
Graph(u) = { (x, y, u(x,y)) | (x,y) in R^2 } subset R^3.
```

Assume this graph is minimal. The included conclusion is that `u` is affine: there exist
`a b c : R` such that `u(x,y) = a*x + b*y + c` for every `(x,y)`. Consequently the graph is an
affine plane. A planned analytic encoding replaces geometric minimality by the minimal-surface
equation

```text
div (grad u / sqrt (1 + |grad u|^2)) = 0
```

everywhere on `R^2`. The geometric and PDE formulations are alternate encodings until a checked
bridge freezes their exact regularity assumptions and conventions.

## Domains and binders to freeze at statement phase

- Domain exactly all of Euclidean `R^2`, not a bounded domain or proper open subset.
- Codomain `R`, with the graph embedded in Euclidean `R^3` using a fixed coordinate convention.
- The weakest source-faithful regularity class, provisionally at least `C^2` for a pointwise PDE;
  any smooth, weak, or variational formulation must be mapped explicitly.
- Minimality as zero mean curvature, stationary area, area minimizing, or the displayed PDE; the
  selected predicate and implications among these notions must be kernel checked.
- Ordered binders for the affine coefficients and the exact equality between functions.
- The norm, gradient, derivative, divergence, square-root positivity, universes, and typeclass
  assumptions used by the Lean expression.

## Boundary and mutation cases

Constant and nonconstant affine functions are included and give horizontal or tilted planes.
Functions defined only locally, on a disk, or on a proper open subset are excluded: non-affine
minimal graphs exist there. The dimension is essential: this target concerns graphs over `R^2`
in `R^3`, and must not be broadened to all higher-dimensional entire minimal graphs. An empty-domain
or abstract predicate wrapper must not make the result vacuous. Later mutation tests must change
the domain, remove minimality, alter binder scope, and exercise affine boundary cases.

## Explicit exclusions

- Bernstein approximation results, Bernstein polynomials, or Bernstein inequalities.
- The higher-dimensional Bernstein problem or a claim for arbitrary `R^n`.
- A theorem only for bounded gradient, bounded height, radial functions, or another strengthened
  hypothesis unless it is used as a named intermediate obligation.
- An abstract `IsMinimalGraph` predicate whose definition stores affineness or the conclusion.
- A statement that assumes vanishing Hessian and merely derives affineness; that is only a final
  bridge, not the Bernstein theorem.
- A set-theoretic assertion that the graph is some plane without a checked transport to the
  coefficient form of `u`.
