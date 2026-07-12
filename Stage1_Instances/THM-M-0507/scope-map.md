# Scope map

## Included topic boundary

- An additive-number-theory theorem whose proof is explicitly identified by a source as an
  application of the Hardy-Littlewood circle method.
- A source-specified representation/counting function, its domains and weights, and the exact
  asymptotic or existence conclusion.
- The circle integral or Fourier coefficient identity, major/minor arc decomposition, singular
  series/integral, local-solubility hypotheses, and error bounds required by that proposition.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different outputs of the method:

1. a Waring-type theorem about representations as sums of powers;
2. a Goldbach-type theorem about sums of primes;
3. an asymptotic formula for partitions or another generating-function coefficient;
4. a reusable abstract circle-method theorem deriving an asymptotic from separately stated major
   and minor arc estimates;
5. merely the Fourier coefficient identity underlying a particular application.

The statement phase must inspect an immutable source and freeze one proposition: ordered binders,
domains, the representation function, number of summands, limiting regime, uniformity, local
conditions, constants, main term, and error term. It must distinguish an exact theorem from a
description of a proof technique.

## Explicit exclusions

- Katona's combinatorial circle method, which is unrelated despite the shared English name.
- Vinogradov's three-primes theorem, Waring's theorem, Goldbach statements, and partition formulas
  as substitutes unless an exact source selects that proposition.
- A tautology assuming the major/minor arc estimates and restating one of them as the conclusion.
- A finite numerical check or experimental asymptotic fit.
- A theorem about generic Fourier analysis that does not crosswalk to the selected additive
  representation problem.
- The manifest label `已验证` as human-proof or machine-proof evidence.

No canonical Lean target is frozen at intake because the repository source names a method, not a
proposition.

