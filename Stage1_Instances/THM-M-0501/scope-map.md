# Scope map

## Included theorem-family boundary

- Uniform distribution of primes in reduced residue classes.
- A modulus `q`, a residue class `a` coprime to `q`, and a cutoff `x`.
- A source-selected prime-counting or weighted counting function.
- A main term involving `phi(q)` and a quantitative, uniform error bound.
- The logarithmic range imposed on `q`, and the quantified parameters controlling that range.
- The effective or ineffective dependence of constants, including the role of exceptional real
  zeros of Dirichlet L-functions in the proof.

## Decisions required at statement freeze

An immutable mathematical source must decide all of the following before a Lean proposition can be
frozen:

1. Whether the conclusion concerns `pi(x; q, a)`, Chebyshev's `theta`, or von Mangoldt's `psi`.
2. Whether `x` is natural or real and precisely how endpoint inequalities and floors are handled.
3. The order and dependence of the quantifiers over the logarithmic-range exponent, error exponent,
   constants, `x`, `q`, and `a`.
4. Whether the error is stated as a power saving in `log x` or in exponential square-root form,
   and whether the assertion is uniform over all reduced residue classes.
5. The exact range for `q`, positivity and coprimality hypotheses, and every small-`x` convention.
6. Which constants are ineffective and whether ineffectivity is mathematical data in the formal
   claim or only a metatheoretic fact about a proof.

## Explicit exclusions

- A zero-free region, zero-density theorem, or exceptional-zero statement by itself. Such results
  may be proof dependencies but are not substitutes for the named distribution theorem.
- Dirichlet's qualitative theorem that each reduced residue class contains infinitely many primes.
- The prime number theorem for a fixed modulus without the Siegel-Walfisz uniform modulus range.
- A statement assumed through an opaque hypothesis and then projected tautologically.
- The repository labels `已验证` and "L-function zero estimate" as proof or statement evidence.
- Any convenient asymptotic variant without a checked, source-backed transport to the selected
  canonical claim.

No canonical Lean target is frozen at intake because the supplied source record does not resolve
these choices.
