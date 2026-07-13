# Scope map

## Preserved source boundary

The repository fixes only the title `切比雪夫估计`, the gloss `素数分布的上下界估计`, Pafnuty
Chebyshev, and 1850. This locates the classical Chebyshev-estimate family concerning prime
distribution. It does not choose a single mathematical function, pair of inequalities, constants,
threshold, domain, or quantifier structure.

The historical source lead is P. L. Tchebichef, *Memoire sur les nombres premiers*, presented to
the Imperial Academy of Saint Petersburg in 1850 and published in 1852. Its introduction describes
bounds for the sum of logarithms of primes and consequences for prime counting. That relationship
does not by itself determine which displayed theorem the short catalog gloss intends.

This boundary is a theorem-family map, not a canonical mathematical statement.

## Decisions required at statement freeze

1. Preserve and independently review one immutable primary or approved authoritative passage,
   including its incorporated definitions, assumptions, conclusion, proof boundary, translation,
   correction, and errata disposition.
2. Decide whether the root bounds the ordinary prime-counting function `pi(x)`, the logarithmic
   prime sum `theta(x)`, the prime-power sum `psi(x)`, or a source-linked package with checked
   transports among them.
3. Fix exact versus asymptotic or eventual form: explicit inequalities, two-sided linear bounds,
   Big-O/Theta notation, or bounds for a normalized ratio are not interchangeable statements.
4. Fix every constant and its quantification, every strict or weak inequality, the starting
   threshold, and whether the source asserts both directions in one root.
5. Fix natural versus real arguments, coercions or floor conventions, the meaning of "at most
   x", logarithm normalization, and all ordered binders and hypotheses.
6. Resolve inputs below two, zero and negative real inputs, integer and prime discontinuities,
   equality at endpoints, empty sums, and every finite exceptional range.
7. Compile checked transports for every credited alternative encoding and perform the required
   removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

## Candidate readings not credited

- Explicit positive constants `a,b` and a threshold `x0` such that
  `a*x/log(x) <= pi(x) <= b*x/log(x)` for all `x >= x0`.
- A two-sided linear bound for Chebyshev `theta(x)` or `psi(x)`.
- A bound only on `theta(x)` such as `theta(x) <= log(4)*x`.
- An eventual upper bound for `pi(x)` with a parameter `epsilon`.
- The asymptotic prime number theorem `pi(x) ~ x/log(x)`.

These examples discriminate scope; none is selected as the target.

## Explicit exclusions

- The prime number theorem, which is stronger and separately owned by `THM-M-0480`.
- Bertrand's postulate, a consequence developed in Chebyshev's memoir and separately owned by
  `THM-M-0481`.
- The Riemann-von Mangoldt explicit formula (`THM-M-0498`) or a de la Vallee Poussin error term
  (`THM-M-0499`).
- Only an upper bound, or positivity/nonnegativity of a counting function, presented as the
  catalog's promised upper-and-lower result.
- A structure, hypothesis, axiom, or oracle that stores the desired bounds.
- Numerical prime tables, sampled ratios, the untrusted label `已验证`, an API name, or a successful
  probe used as source or proof evidence.

No canonical human proposition, Lean expression, alternate transport, obligation registry,
discovery protocol, proof body, or completion claim is frozen at intake.
