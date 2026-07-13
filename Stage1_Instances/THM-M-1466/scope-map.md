# Scope map

## Preserved theorem family

The intake preserves finite-volume discretization of conservation laws as the named family. A
later statement phase may select a canonical root only after an immutable primary-source
proposition and every incorporated definition are mapped and independently reviewed. Candidate
components, none credited as the theorem, include:

- a scalar or system conservation law, its flux, spatial domain, time interval, and initial and
  boundary data;
- a weak, entropy, measure-valued, or other solution concept and its uniqueness regime;
- a conforming mesh or control-volume complex with cells, faces, orientations, measures, and
  neighbor or boundary incidence;
- cell averages, reconstructions, quadrature, and a numerical flux with consistency and
  conservativity properties;
- a semidiscrete or fully discrete update, time step, and CFL or other step restriction;
- exact local balance and global cancellation of internal numerical fluxes;
- monotonicity, positivity, invariant-domain, entropy, total-variation, or norm stability;
- consistency, compactness, convergence to a weak or entropy solution; and
- a qualitative or quantitative truncation, discretization, or solution error result.

## Decisions required at statement freeze

The statement phase must freeze these choices from an approved source, not from a convenient
modern convention:

1. The exact source edition, theorem or formula locator, incorporated definitions, proof boundary,
   corrections, and independent review.
2. Scalar law or system; steady or time-dependent problem; spatial dimension and domain; flux;
   source terms; and initial, boundary, interface, and far-field conditions.
3. The continuous solution concept, regularity and admissibility assumptions, uniqueness regime,
   and scalar field or value space.
4. Mesh/control-volume geometry; cell and face indexing; measures, normals and orientations;
   interior/boundary incidence; shape regularity; and refinement family.
5. Cell unknowns or averages; reconstruction; physical and numerical fluxes; consistency,
   conservativity, Lipschitz, monotonicity, entropy, and boundary-flux conventions.
6. Semidiscrete versus fully discrete time evolution; explicit or implicit update; time-step and
   CFL conditions; initialization; and exact-real, rational, interval, or floating-point semantics.
7. Whether the root asserts local/global conservation, consistency, stability, convergence,
   entropy admissibility, a quantitative rate, or a source-approved conjunction.
8. Ordered binders, universes, dependent indices, all hypotheses and constants, conclusion,
   logic strength, and every excluded boundary case.

## Degenerate and boundary cases

Source review must explicitly decide an empty cell set; empty or zero-measure cells and faces;
zero-dimensional or empty spatial domains; periodic, closed, inflow/outflow, or absent boundary;
zero flux and constant states; self-neighboring cells; duplicate or unoriented faces; nonmanifold
incidence; degenerate or nonconforming meshes; zero time step; final time zero; CFL equality;
vacuum or loss of positivity; discontinuous exact solutions and shocks; nonunique weak solutions;
inconsistent or nonconservative numerical fluxes; boundary and source terms; irregular refinement;
and exact cancellation versus roundoff in floating-point arithmetic.

## Substitution exclusions

- A finite-sum cancellation identity alone is not a finite-volume discretization theorem.
- The divergence theorem, a weak conservation law, or an entropy-solution theorem alone does not
  define or validate a discrete finite-volume scheme.
- Finite differences, finite elements, Galerkin, Petrov-Galerkin, discontinuous Galerkin, and
  spectral elements are separately cataloged method families and cannot replace this target.
- A one-dimensional scalar linear-advection or fixed-grid example cannot silently replace the
  unspecified conservation-law family.
- Exact conservation does not imply stability, convergence, an entropy condition, or an error rate;
  none may be substituted for another without a source-selected root and its full hypotheses.
- Kruzkov uniqueness, the Oleinik condition, compensated compactness, or shock theory cannot
  substitute for correctness of a finite-volume discretization.
- A mesh generator, solver run, residual plot, convergence table, floating-point experiment, or
  structure storing the desired balance or convergence result is not a proof.
- The catalog label `verified` supplies no source or kernel credit.

No canonical statement, Lean target, expression fingerprint, checked alternate encoding,
discovery protocol, obligation registry, or proof state is frozen at intake.
