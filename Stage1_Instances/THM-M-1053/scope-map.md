# Scope map

## Included claim

- A probability space `(X, A, mu)` and a measurable, measure-preserving endomorphism `T : X -> X`.
- A real-valued integrable observable `f` and forward Cesaro averages
  `A_n f(x) = (1/n) * sum_{k=0}^{n-1} f(T^k x)` for positive `n`.
- Almost-everywhere convergence of `A_n f` to an integrable `T`-invariant limit.
- Under the additional hypothesis that `T` is ergodic, identification of the limit almost
  everywhere with the constant `integral f dmu`.

## Decisions deferred to the statement phase

The next phase must freeze the exact mathlib notions of probability measure, measurability,
measure preservation, ergodicity, integrability, iteration, and almost-everywhere convergence. It
must also decide whether the codomain is `Real` or a supported Banach-valued generalization, whether
the general limit is expressed by conditional expectation, and how the `n = 0` average is encoded.
Binder order, universes, equality mode, and normalization must then be fingerprinted.

## Explicit exclusions

- Mean ergodic convergence in `L2` or another norm as a substitute for pointwise convergence.
- A finite-state Markov-chain ergodic theorem, an individual ergodic theorem, or a continuous-time
  flow theorem as a substitute.
- "Time average equals space average" without the ergodicity hypothesis.
- Assuming the desired limit or convergence as a premise, or packaging it as structure data.
- Treating the Stage0 `已验证` label as source, statement, or machine-proof evidence.
