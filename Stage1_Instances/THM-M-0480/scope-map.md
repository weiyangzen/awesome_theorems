# Scope map

## Preserved theorem family

The intake preserves the ordinary prime number theorem family described by the catalog formula
`pi(x) ~ x/log(x)`: the prime-counting function is asymptotically equivalent to `x/log(x)` at
positive infinity. This sentence is a scope locator, not the frozen canonical proposition.

A conventional real-variable candidate would count primes at most `floor(x)` and assert
asymptotic equivalence along the real `atTop` filter. A conventional natural-variable candidate
would compare the real cast of `Nat.primeCounting n` with `(n : Real) / log n` along the natural
`atTop` filter. Intake does not choose between them or credit their equivalence.

## Decisions required at statement freeze

1. Define `pi`: natural prime counting, a real extension by floor or nonnegative floor, and whether
   primes at the endpoint are included.
2. Fix the input domain and filter: naturals tending to infinity, nonnegative reals tending to
   positive infinity, or another source-selected encoding.
3. Fix the codomain and coercions, including casts of `Nat.primeCounting`, floor behavior, and the
   treatment of negative real inputs if a total real function is used.
4. Define `~` as source-approved asymptotic equivalence, a ratio tending to one, or an explicit
   epsilon formulation, and supply checked transports for every credited alternate form.
5. Fix the logarithm base and expression grouping. In Lean this normally means natural `Real.log`
   and `x / log x`, but the catalog alone is not an accepted source decision.
6. Freeze ordered binders, all side conditions, universe and typeclass context, options, minimal
   imports, the exact conclusion, and the scope of every variable.
7. Decide whether an equivalent `pi(x) * log(x) / x -> 1`, a `theta(x) ~ x` or `psi(x) ~ x` form,
   or an nth-prime asymptotic is merely a proof route or an advertised alternate with a checked
   two-way transport.

These choices can change the literal proposition even when standard mathematics later proves
some choices equivalent.

## Boundary and mutation cases

- At `x = 0` and `x = 1`, `log x` or division makes a pointwise ratio unsuitable; an asymptotic
  formulation may ignore an eventual finite prefix, but the total functions still need definitions.
- A real extension must specify negative inputs and values between consecutive integers, including
  prime jump points and whether `floor`, `ceil`, or `Nat.floor` is used.
- A natural sequence avoids negative inputs but changes the filter domain and formal target.
- Changing `atTop` to a finite neighborhood, deleting a cast, changing `<= x` to `< x`, using
  base-10 logarithm without a compensating constant, or replacing equivalence by one-sided Big-O is
  a statement mutation, not presentation.
- The statement phase must mutation-test removed side conditions, changed domain, changed binder
  scope, and representative boundary cases before any proof evidence is inspected.

No degenerate case is canonically excluded at intake.

## Explicit non-substitutions and neighbors

- Chebyshev upper or lower bounds, `theta`/`psi` definitions, and the Abel-summation relation are
  ingredients or weaker results, not the prime number theorem root.
- Bertrand's postulate (`THM-M-0481`) and Chebyshev estimates (`THM-M-0482`) are separate targets.
- The Riemann-von Mangoldt formula (`THM-M-0498`) and de la Vallee Poussin error term
  (`THM-M-0499`) are distinct stronger or quantitatively different targets.
- The prime number theorem for arithmetic progressions, Dirichlet's infinitude theorem, nth-prime
  asymptotics, Mertens-type results, and zeta nonvanishing are not silently interchangeable roots.
- Finite prime counts, numerical ratios, a structure field or hypothesis containing the result,
  an untrusted verified label, or an API probe cannot serve as proof.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks the
prime-counting definition and divergence, the generic `Asymptotics.IsEquivalent` interface,
`Real.log`, `Filter.atTop`, `Chebyshev.theta` and `psi`, the prime-counting/theta integral identity,
the small integral estimate, and an eventual prime-counting upper bound. Pinned
`Mathlib.NumberTheory.Chebyshev` explicitly leaves Chebyshev's lower bound as a TODO. None of these
interfaces proves `theta(x) ~ x` or the catalog PNT root.

No canonical Lean expression or fingerprint is frozen. The bounded observations are feasibility
and discriminator evidence only; exhaustive formal-candidate provenance belongs to the dependent
anchor-audit phase.
