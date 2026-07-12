# Scope map

## Included topic boundary

- An arithmetic-geometric formula genuinely identified in a primary source by Shou-Wu Zhang.
- A height or height pairing of a source-specified Heegner cycle on a higher-dimensional
  Kuga-Sato, Shimura, or related arithmetic variety.
- A derivative of a source-specified Rankin or automorphic L-function.
- The exact equality, including every period, volume, discriminant, factorial, sign, Euler factor,
  and normalization appearing in the selected source.
- The classical Gross-Zagier formula only as source-justified context or a checked specialization,
  not as a replacement for the higher-dimensional claim.

## Decisions required at statement freeze

The statement phase must inspect an immutable primary-source edition and freeze:

1. The theorem/equation number, page, and whether the relevant result is unconditional or refers
   to definitions and assumptions elsewhere in the paper.
2. The modular eigenform or automorphic representation, its weight and level, coefficient field,
   and any newform, ordinarity, or local hypotheses.
3. The imaginary quadratic field, discriminant, embedding data, Heegner hypothesis, conductors,
   characters, and excluded primes.
4. The ambient variety, codimension and construction of the Heegner cycle, homological
   triviality, projector, and coefficient conventions.
5. The height pairing, measures, Petersson norms, completed versus incomplete L-function, Euler
   factors, analytic continuation, functional-equation sign, derivative order, and all constants.
6. Boundary behavior when the cycle, height, derivative, or normalization factor vanishes and the
   exact scalar field in which the equality is asserted.

The Lean statement must expose these data and hypotheses. It must not assume the desired equality
as a structure field or hide undefined analytic and intersection-theoretic content behind an
uninterpreted predicate.

## Explicit exclusions

- The elliptic-curve Gross-Zagier theorem alone.
- The Birch-Swinnerton-Dyer conjecture, a nonvanishing corollary, or a rank formula alone.
- An arbitrary theorem relating an abstract `height` function to an abstract `LDerivative` when
  those names have no construction matching the source.
- A formula from a later generalization, p-adic analogue, or different Shimura variety unless the
  source audit proves it is the repository's intended 1997 target.
- The repository labels `已验证` and "1997" as proof, bibliographic, or kernel evidence.

No canonical Lean expression is frozen at intake.
