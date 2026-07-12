# Scope map

## Included topic boundary

- A source-specified Poisson summation identity relating samples of a function on a lattice to
  samples of its Fourier transform on the dual lattice.
- The exact Fourier-transform normalization, phase factor, translation, and lattice scale.
- The function space and all convergence, continuity, integrability, smoothness, or decay
  hypotheses needed by the selected statement.
- The exact equality notion and interpretation of both infinite sums.

## Decisions required at statement freeze

The repository gloss does not decide among materially different standard formulations:

1. A general translated identity under local uniform summability of integer translates and
   summability of Fourier samples, as in pinned `Real.tsum_eq_tsum_fourier`.
2. A sufficient polynomial-decay version for a continuous function and its Fourier transform.
3. A Schwartz-function specialization.
4. The unshifted `x = 0` identity or a scaled-lattice variant.

The statement phase must freeze ordered binders and hypotheses, the `𝓕` convention, signs and
constants, the role of `x`, and whether sums are Lean `tsum`s justified by explicit summability or
by stronger decay/Schwartz assumptions.

## Explicit exclusions

- The finite/discrete Fourier transform, Poisson point processes, and the Poisson integral formula.
- A Gaussian theta identity as a substitute for the general named formula.
- An equality with missing convergence hypotheses or an arbitrary Fourier normalization.
- Proving only the Fourier-coefficient bridge lemma while claiming the summation identity.
- Treating the repository label `已验证` or a successful `#check` as proof credit.

No canonical Lean target is frozen at intake. The pinned mathlib theorem family is a candidate
encoding surface, not yet a source-faithful target selection.
