# Scope map

## Included claim

- Euclidean space of natural dimension `n` and first weak/classical derivative order one.
- Exponents `1 <= p < n` and Sobolev conjugate `q` satisfying `1/q = 1/p - 1/n`.
- An inequality of the form `norm(f, L^q) <= C(n,p) * norm(gradient f, L^p)`.
- A sufficiently regular compactly supported scalar-valued function, with the exact regularity and
  completion formulation deferred to the inspected source and available Lean API.

## Statement-phase decisions

The exact source must decide whether the domain is `R^n`, whether functions are `C_c^1`, smooth
and compactly supported, or members of a completed Sobolev space; whether `p = 1` is included;
whether values are real or complex; and whether the result asserts a uniform constant or supplies a
specific constant. Binder order, exponent encoding (`Real`, `ENNReal`, or conjugate parameters),
gradient norm, measure normalization, zero-dimensional and empty-support cases must then be frozen.

## Explicit exclusions

- The endpoint embeddings at `p = n`, Morrey embedding for `p > n`, or a logarithmic inequality.
- A bounded-domain, manifold, fractional, higher-order, weighted, discrete, or trace inequality as
  a substitute for the Euclidean first-order claim.
- Merely assuming the norm inequality as a hypothesis or field of a structure.
- Treating an import or repository metadata label `已验证` as proof of the target.

The later statement may use a checked equivalent Gagliardo-Nirenberg-Sobolev formulation only when
an exact transport establishes that its domains, exponents, derivative, and norms match this scope.
