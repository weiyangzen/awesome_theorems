# Scope map

## Included claim boundary

- Complex-valued square-integrable functions on a finite-dimensional real Euclidean space.
- The Fourier transform extended from a suitable dense test-function class to `L^2`.
- Isometry in the literal sense `||Fourier f||_2 = ||f||_2` for every `f` in `L^2`.
- Inner-product preservation as the corresponding polarization formulation, subject to the same
  normalization and a checked equivalence or common isometric operator.

## Decisions required at statement freeze

The exact source must fix the spatial domain (`R`, `R^n`, or a more general group), scalar field,
Fourier kernel/sign, constants such as `(2 * pi)`, Haar or Lebesgue measure normalization, and
whether the theorem is stated first on an integrable dense subspace or directly as the unitary
extension on `L^2`. It must also decide the dimension binder, the zero-dimensional case, equality
of equivalence classes almost everywhere, and whether surjectivity/inversion is part of the theorem
or only a consequence.

Mathlib's pinned declaration is more polymorphic than the repository wording: it permits a
finite-dimensional real inner-product domain and values in a complex Hilbert space. A canonical
target must specialize this to the source-approved scalar Euclidean claim unless a primary source
crosswalk independently justifies the extra generality.

## Explicit exclusions

- Parseval identities only for Fourier series, finite groups, or an orthonormal basis.
- The Hausdorff-Young inequality, Fourier inversion, or an `L^1` norm bound as a substitute.
- A Schwartz-function-only identity as a substitute for the extension to all `L^2` classes.
- An arbitrary Hilbert-valued or locally compact abelian group generalization without source scope.
- A transform with an unexplained normalization constant.
- A structure or hypothesis that assumes norm preservation and then projects it.
- The repository label `已验证` or an uninspected mathlib theorem name as completion evidence.
