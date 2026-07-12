# Scope map

## Included theorem family

- The M. Riesz strong-type boundedness theorem for the Hilbert/conjugate-function operator.
- An exponent strictly between `1` and `infinity`.
- A source-selected real-line `L^p(R)` or periodic `L^p(T)` domain.
- A precise transform construction, initially on an appropriate dense class and extended to `L^p`.
- A bound of the form `norm (H f) <= C_p * norm f`, including the quantification and permitted
  dependence of `C_p`.

## Decisions required by the statement phase

1. Select the real-line Hilbert transform or the periodic conjugate-function operator from an exact
   source statement. A later transport between them needs its own checked witness.
2. Fix scalar values, measure normalization, kernel sign and factor, and the representation of the
   exponent in Lean.
3. State whether the transform is defined by truncated singular integrals, almost-everywhere
   principal values, Fourier multipliers, or a continuous extension from a dense subspace.
4. Specify whether the conclusion is existence of a bounded operator, an explicit norm estimate,
   or both, and whether the constant is sharp.
5. Separate construction/well-definedness from boundedness and identify any density or
   almost-everywhere equivalence bridge.

## Explicit exclusions

- Weak type `(1,1)`, `L^infinity` to BMO boundedness, weighted `L^p`, vector-valued extensions, and
  higher-dimensional Riesz transforms.
- A theorem only for `p = 2`, a Schwartz-space Fourier multiplier identity, or boundedness of an
  arbitrary supplied operator as a substitute for the full `1 < p < infinity` result.
- Pointwise existence of the principal value without the `L^p` norm estimate, or the norm estimate
  for a postulated Hilbert transform without constructing/crosswalking that operator.
- The repository label `已验证` as human-source or machine-proof evidence.

The canonical Lean target is intentionally not frozen during intake because these choices are not
determined by the repository source record.
