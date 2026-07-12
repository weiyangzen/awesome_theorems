# Scope map

## Included theorem family

- The ordinary prime-counting function `pi(x)`, counting primes at most `x`.
- A logarithmic integral `Li(x)` with an exact source-selected normalization.
- An existential absolute constant `c > 0`.
- The unconditional asymptotic estimate at positive infinity
  `pi(x) - Li(x) = O(x * exp(-c * sqrt(log x)))`.
- A checked transport between real-variable and natural-variable versions if
  both are advertised.

The exponential factor and square-root logarithm are part of the root claim.
The bare prime number theorem `pi(x) ~ x / log x` is weaker and cannot replace
it.

## Statement decisions still open

The statement phase must select one pinpoint source and freeze:

1. whether `x` ranges over reals or naturals and which `atTop` filter is used;
2. whether real `pi(x)` means `Nat.primeCounting floor(x)` and how negative
   inputs are excluded or extended;
3. whether `Li(x)` is a Cauchy principal value, an offset integral such as
   `integral 2..x (1 / log t)`, or another explicitly normalized function;
4. whether the theorem is presented with asymptotic `IsBigO` or explicit
   constants `C`, `x0`, and how those formulations are transported;
5. exact quantifier order and whether `c` is merely positive and absolute;
6. strictness and handling of integer/prime discontinuities.

Changing `Li` by an additive constant is often harmless to this asymptotic
class, but that fact must be checked rather than used to erase statement
identity.

## Formal object boundary

Pinned mathlib defines `Nat.primeCounting` and has real `log`, `sqrt`, `exp`,
`Filter.atTop`, and `Asymptotics.IsBigO`. It does not expose a named
logarithmic-integral function in the searched pinned tree. Thus an exact target
will need a reviewed local definition or a located equivalent API, together
with a floor/natural-variable decision. The intake probe establishes only API
availability, not the error estimate.

## Explicit exclusions

- The ordinary prime number theorem without this quantitative error term.
- A Riemann-hypothesis conditional square-root error bound.
- Modern stronger zero-free-region error terms substituted for the historical
  square-root-log form.
- An estimate only for `Chebyshev.theta` or `Chebyshev.psi` without a checked
  transfer to `pi - Li`.
- A claim about `pi(x) - x / log x`, or an equality without asymptotic meaning.
- Finite computation of primes or zeta zeros as proof of the asymptotic claim.
