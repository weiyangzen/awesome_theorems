# THM-M-1459 scope map

## Preserved method family

The intake preserves the particle-interaction fast multipole family named by the catalog: replace
selected distant pairwise interactions by hierarchical multipole/local expansions so that an
N-body potential or force can be approximated more quickly than a direct all-pairs evaluation.
This is a scope description, not a frozen theorem.

The historical 1987 paper is titled *A fast algorithm for particle simulations*. The catalog's
broader phrase "N-body problem" does not say whether it means evaluating one static interaction
field, computing forces, or integrating an N-body dynamical system through time. These are
different specifications and must not be conflated.

## Proposition-changing decisions

An independently reviewed source correction must decide all of the following:

1. The mathematical task: static potentials, static forces, matrix-vector products, or time
   evolution; a static summation theorem must not silently become an N-body integrator theorem.
2. Ambient dimension and coefficient domain, and whether positions are real vectors, planar
   complex coordinates, or another sourced representation.
3. The interaction kernel, such as the two-dimensional logarithmic potential, its complex
   derivative/force form, a three-dimensional Laplace kernel, Coulomb/gravitational kernels, a
   screened kernel, or a kernel-independent interface.
4. Source strengths, target points, whether sources and targets coincide, self-interaction
   exclusion, collision/nonzero-distance hypotheses, and normalization or physical constants.
5. The exact direct quantity being approximated and the output norm: per-target absolute or
   relative error, uniform error, energy error, force error, or another source-selected metric.
6. Accuracy input and expansion order, including how truncation is chosen and how zero or extreme
   tolerances behave.
7. The spatial hierarchy: fixed-depth quadtree/octree or adaptive tree, box geometry, leaf
   occupancy, balancing, depth, interaction lists, and empty or coincident boxes.
8. The near/far separation rule and every multipole-to-multipole, multipole-to-local,
   local-to-local, and direct-neighbor translation included in the correctness result.
9. Whether the conclusion is an analytic expansion identity, truncation bound, end-to-end
   correctness theorem, arithmetic-operation bound, storage bound, parallel bound, or a conjunction.
10. The cost model: real/complex operations, fixed requested accuracy, dependence on expansion
    order or tolerance, constants, preprocessing, evaluation, memory, and uniform versus adaptive
    distribution assumptions.
11. Exact arithmetic, floating-point arithmetic, roundoff, accumulated translation error, and
    whether empirical timing or implementation behavior is excluded from theorem evidence.
12. Ordered binders, universes, all hypotheses, equality/inequality orientation, alternate
    encodings with checked transports, foundation and TCB profiles, and every boundary case.

## Boundary cases

The statement phase must resolve zero or one particle; zero source strengths; an empty target set;
coincident particles; targets at source locations; all particles in one box; empty boxes; points on
box boundaries; zero tree depth; unbounded/adversarial tree depth; expansion order zero; requested
error zero, negative, or above the natural scale; exact cancellation; degenerate cluster radii;
failed near/far separation; complex versus real-valued output; and exact versus finite-precision
arithmetic.

## Excluded substitutions

- A geometric-series identity or analytic power-series theorem alone is an ingredient, not an FMM
  correctness or complexity result.
- Barnes-Hut/treecode, particle-mesh, Ewald, FFT, or generic hierarchical-matrix algorithms cannot
  replace a source-selected FMM theorem.
- A two-dimensional logarithmic-kernel theorem cannot silently stand for a three-dimensional
  gravitational/Coulomb N-body theorem, or conversely.
- An error bound for one expansion or one translation does not establish an end-to-end algorithmic
  guarantee unless the selected root says so and all composition steps are modeled.
- A declaration that assumes an abstract oracle, cost certificate, hierarchy, approximation, or
  desired error bound as a field supplies no construction or proof.
- Source-code execution, benchmark timings, asymptotic slogans, API checks, a theorem-name match,
  and the untrusted `已验证` label supply no source or machine-proof credit.

## Neighbor boundaries

The FFT target `THM-M-1458` and multigrid target `THM-M-1457` describe different algorithms and
provide no inherited evidence. The finite-element and spectral-method neighbors likewise cannot
substitute for a particle-interaction FMM result. A later corrected root must also distinguish
classical FMM from adaptive FMM, kernel-independent FMM, and fast direct solvers.

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, finite sums satisfy a
norm bound, complex numbers provide the expected normed-field operations, and geometric series have
summability, sum, and norm-bound theorems. A bounded exact-topic search found no declaration named
for fast multipole, multipole, Greengard, or Rokhlin in pinned mathlib or the repository's Lean
sources. The probe is bounded intake discovery, not the downstream exhaustive anchor audit, and
the analytic substrate is not a source-selected FMM theorem.
