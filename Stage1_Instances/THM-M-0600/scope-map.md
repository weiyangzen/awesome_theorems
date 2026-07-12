# Scope map

## Included claim

- A finite-dimensional smooth real manifold `M` without boundary, a smooth map `f : M -> R`, and a
  point `p : M`.
- `p` is critical: the derivative of `f` at `p` vanishes.
- The Hessian at `p` is nondegenerate; its negative index is a natural number `lambda` no larger
  than the manifold dimension `n`.
- There is a local smooth coordinate chart centered at `p` in which, on an open neighborhood of
  zero,
  `f = f(p) - x_1^2 - ... - x_lambda^2 + x_(lambda+1)^2 + ... + x_n^2`.

## Decisions reserved for the statement phase

The selected source must settle its differentiability convention and whether it states the result
first on an open subset of `R^n` or intrinsically on a manifold. The Lean statement must then freeze
the model space, finite-dimensional hypotheses, chart/local-equivalence encoding, derivative and
Hessian definitions, bilinear-form nondegeneracy, index representation, neighborhood quantifiers,
and the zero-dimensional, local-minimum (`lambda = 0`), and local-maximum (`lambda = n`) cases.

The displayed sign ordering is a convention, not permission to change the Hessian index. A checked
transport will be needed if the chosen Lean API orders positive coordinates first or uses a linear
change of variables rather than an indexed coordinate sum.

## Explicit exclusions

- The Morse-Bott lemma, splitting lemma with a degenerate residual term, or a parametrized Morse
  lemma as a substitute for the ordinary nondegenerate theorem.
- A second-order Taylor approximation, equality only up to higher-order error, or a statement only
  about diagonalizing the Hessian.
- Morse inequalities, Morse theory, handle attachment, or a global classification of the manifold.
- A theorem restricted to one dimension, polynomial functions, minima only, maxima only, or a fixed
  index, unless used later as a clearly labeled child obligation.
- A structure or hypothesis that contains the desired coordinate normal form as data.

No claim about manifolds with boundary or infinite-dimensional manifolds is included in this root.
