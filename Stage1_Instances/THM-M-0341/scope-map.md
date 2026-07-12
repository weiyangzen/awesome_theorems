# Scope map

## Included topic boundary

- An inversion theorem for a precisely defined Fourier transform and inverse transform.
- A source-selected domain, codomain, measure, additive character, and normalization convention.
- Exact regularity and integrability hypotheses and the source-selected equality mode.
- Both directions only if the selected source explicitly asserts both.

## Ambiguities to resolve at statement freeze

The repository record does not decide among these non-equivalent claims:

1. Pointwise inversion for an integrable function whose Fourier transform is integrable, at a
   continuity point.
2. Function equality under global continuity plus integrability of the function and transform.
3. Almost-everywhere or `L2` inversion for equivalence classes.
4. Inversion on Schwartz functions or distributions.
5. Fourier-series inversion on a circle or torus rather than Fourier-transform inversion on a
   vector space or locally compact abelian group.

It also omits the sign and `2 * pi` convention, forward/inverse direction, scalar and vector-valued
setting, dimension, and measure normalization. The statement phase must obtain a source passage and
freeze all of these choices, including ordered binders and boundary cases.

## Explicit exclusions

- Plancherel's theorem, Parseval identities, Poisson summation, and the Riemann-Lebesgue lemma as
  substitutes for inversion.
- Fourier-series convergence as a substitute for transform inversion.
- A definition of an inverse operator followed by a tautological equality.
- The deprecated alias `MeasureTheory.Integrable.fourier_inversion` as distinct proof credit from
  its terminal declaration.
- The manifest label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake. The pinned declarations are candidates whose exact
fit can only be decided after source selection.
