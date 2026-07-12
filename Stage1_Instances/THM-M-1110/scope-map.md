# Scope map

## Included theorem family

- Dimension-indexed real symmetric or complex Hermitian Wigner random matrices in the symmetry
  class fixed by the selected primary theorem.
- Local eigenvalue statistics in the interior of the limiting semicircle spectrum, at mean-spacing
  scale of order `1/n` after the source's density normalization.
- A source-specified observable, such as rescaled `k`-point correlation functions tested against
  compactly supported observables or local gap statistics.
- Universality expressed by convergence to the corresponding GOE/GUE statistic, with any energy
  averaging or comparison formulation stated explicitly.

## Decisions required at statement freeze

The statement phase must select and inspect one exact primary theorem. It must freeze: real versus
complex symmetry; Hermitian/symmetric encoding; independence and identical-distribution rules;
centering and variance normalization; diagonal distribution; tail, moment, smoothness, or Fourier
decay assumptions; the bulk-energy interval and distance from spectral edges; fixed energy versus
energy averaging and the averaging-window scale; the definition and normalization of correlation
functions; test-function regularity and support; the order of `n`, `k`, energy, and error
quantifiers; and the exact limiting Gaussian observable. Boundary cases such as zero variance,
atoms, heavy tails, edge energies, and small dimensions must not be silently absorbed.

These choices distinguish different results in the Erdos-Schlein-Yau program and change the Lean
binders, hypotheses, and conclusion.

## Explicit exclusions

- The global Wigner semicircle law, eigenvector delocalization, a local semicircle estimate, level
  repulsion, or a Wegner estimate alone as a substitute for local-statistics universality.
- Tracy-Widom edge universality, the Tao-Vu four-moment theorem, or universality only for GOE/GUE
  matrices as a substitute for the selected Wigner class.
- A statement with energy averaging removed, weaker entry assumptions, or fixed-energy convergence
  unless that exact strengthening is the selected and audited source theorem.
- Convergence of expected empirical spectral measures or finitely many spectral moments.
- A simulation, asymptotic heuristic, or a structure/hypothesis containing the desired limiting
  correlation identity as input data.
- The repository metadata value `已验证` as source or kernel evidence.

No canonical Lean expression is frozen at intake. A later target must expose the random-matrix
ensemble, eigenvalue observable, rescaling, limiting statistic, and convergence mode concretely.
