# Scope map

## Preserved theorem family

The intake preserves adaptive finite-element analysis driven by a posteriori error information as
the repository's named family. A later statement phase may select a canonical root only after one
immutable primary-source proposition and all incorporated definitions are mapped and independently
reviewed. Candidate components, none credited as the theorem, include:

- a continuous weak boundary-value problem and its well-posedness assumptions;
- conforming or nonconforming finite-element spaces on admissible meshes;
- a computable or approximately computable residual, recovery, hierarchical, or other estimator;
- local indicators and a global estimator assembled from them;
- reliability, local or global efficiency, oscillation terms, or estimator equivalence;
- a marking rule, refinement operation, conformity closure, and adaptive solve-estimate-mark-refine
  loop; and
- estimator reduction, contraction, convergence, rate optimality, work optimality, or termination.

## Decisions required at statement freeze

An approved source decision must freeze all of the following rather than importing modern AFEM
conventions:

1. The exact edition, theorem/page/formula locator, incorporated definitions, proof boundary,
   corrections, and independent review.
2. The differential equation or variational problem, dimension, domain and boundary conditions,
   coefficients and data, scalar field, spaces, norms, solution concept, and well-posedness.
3. Initial and refined meshes, cell shapes, admissibility and shape regularity, conformity,
   polynomial degree, nestedness, refinement closure, and mesh-size convention.
4. The discrete problem and solver; whether solves are exact; and the treatment of quadrature,
   geometry, algebraic, and floating-point error.
5. The estimator and local indicators, residual or recovery terms, jumps, patches, data oscillation,
   localization, computability convention, and every hidden constant and dependency.
6. The adaptive loop, marking strategy and parameter, refinement rule, coarsening policy, stopping
   condition, and indexing of meshes, spaces, solutions, and estimators.
7. The selected root conclusion: an upper or lower a posteriori bound, two-sided equivalence,
   estimator reduction, contraction, plain convergence, quasi-optimal rate, complexity, or an
   approved conjunction.
8. Exact ordered binders, universes, typeclass context, quantifier dependencies, hypotheses,
   conclusion, foundation strength, and computation boundary.

## Degenerate and boundary cases

Source review must explicitly decide the zero solution and zero load; vanishing estimator; empty or
zero-dimensional domain; empty mesh and degenerate cells; singular continuous or discrete problem;
nonconforming data; zero or extreme marking parameter; marking no cells or all cells; a refinement
that makes no progress; nonnested spaces; exact representation of the solution; data oscillation
equal to zero or dominating the residual; early stopping; infinite refinement; constants depending
on the mesh or solution; and exact-real versus finite-precision execution.

## Substitution exclusions

- `THM-M-1461` finite-element method, `THM-M-1462` Galerkin method, and `THM-M-1468` hp finite
  elements cannot replace this adaptive family.
- `THM-M-1470` separately owns a posteriori error estimation. An estimator theorem transfers no
  adaptive-loop, convergence, rate, or complexity credit here.
- `THM-M-1471` a priori error estimation cannot substitute for an a posteriori adaptive result.
- Lax-Milgram well-posedness, orthogonal projection, Galerkin orthogonality, or Cea
  quasi-optimality alone is not an adaptive finite-element theorem.
- Reliability does not imply efficiency, convergence, contraction, rate optimality, or complexity;
  no one result may silently stand for another.
- An abstract structure that stores the desired estimate, contraction, or convergence as a field is
  not a proof.
- A mesh generator, numerical run, residual plot, benchmark, or floating-point stopping rule is not
  kernel evidence for an exact mathematical target.
- The pinned fixed-point theorem `ContractingWith.aposteriori_dist_iterate_fixedPoint_le` concerns
  contraction iterates, not finite-element residual estimation or mesh adaptivity.
- The catalog label `verified` supplies no source, statement, or proof credit.

No canonical statement, Lean target, expression fingerprint, checked alternate encoding, discovery
protocol, obligation registry, or accepted proof state is frozen at intake.
