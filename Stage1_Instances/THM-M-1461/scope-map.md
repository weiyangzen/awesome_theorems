# Scope map

## Preserved theorem family

The intake preserves finite-element variational discretization of PDEs as the named family. A
later statement phase may select a canonical root only after an immutable primary-source
proposition and every incorporated definition are mapped and independently reviewed. Candidate
components, none credited as the theorem, include:

- a domain, boundary decomposition, differential operator, forcing data, and boundary conditions;
- a continuous weak problem in a normed, Hilbert, or Sobolev space;
- a mesh or triangulation with geometric regularity assumptions;
- a conforming or nonconforming finite-dimensional trial/test space and basis;
- the discrete variational problem and its existence or uniqueness;
- consistency or Galerkin orthogonality;
- best-approximation or Cea-type quasi-optimality;
- interpolation, energy-norm, or other a priori error estimates; and
- convergence or a rate along a specified mesh family.

## Decisions required at statement freeze

The statement phase must freeze these choices from an approved source, not from a convenient
modern convention:

1. The exact source edition, theorem or formula locator, incorporated definitions, proof boundary,
   corrections, and independent review.
2. The PDE and spatial dimension; domain and boundary regularity; boundary conditions; coefficient
   assumptions; and weak, strong, or distributional solution convention.
3. The scalar field; continuous trial and test spaces; norms, seminorms, and duality pairing; and
   the bilinear, sesquilinear, or nonlinear form and load functional.
4. The continuity, coercivity, ellipticity, inf-sup, consistency, regularity, and approximation
   hypotheses, including every constant and dependency.
5. The mesh, cell, reference-element, shape-function, conformity, polynomial-degree, quadrature,
   and shape-regularity conventions.
6. Whether the root asserts discrete existence and uniqueness, orthogonality, quasi-optimality,
   convergence, a quantitative error rate, or a source-approved conjunction.
7. Ordered binders, universes, dependent indices, hypotheses, conclusion, logic strength, and any
   computational or floating-point boundary.

## Degenerate and boundary cases

Source review must explicitly decide the empty or zero-dimensional domain; zero forcing; zero or
noncoercive forms; incompatible boundary data; an empty mesh; degenerate or inverted cells; zero
mesh size; nonconforming spaces; a trial space not contained in the continuous space; polynomial
degree zero; exact inclusion of the solution in the discrete space; singular stiffness matrices;
nonunique discrete solutions; insufficient solution regularity; quadrature and geometry error; and
whether refinement is nested, shape regular, and dense in the required norm.

## Substitution exclusions

- Lax-Milgram well-posedness alone is not a finite-element discretization or error theorem.
- Orthogonal projection or best approximation alone is not a source-selected FEM result.
- Generic Galerkin, Petrov-Galerkin, or discontinuous Galerkin theorems cannot replace this target;
  those method families also have separate catalog entries.
- Cea quasi-optimality cannot be stated without its continuity, coercivity, conformity, and
  discrete-solution hypotheses or promoted to an interpolation rate without extra approximation
  and regularity assumptions.
- A theorem for one-dimensional piecewise-linear Poisson elements cannot silently replace an
  unspecified PDE-wide claim.
- A mesh generator, stiffness-matrix assembly program, numerical example, residual plot, or
  floating-point experiment is not a proof of an exact mathematical root.
- A structure that stores the desired discrete solution, estimate, or convergence result as a
  hypothesis is not a proof.
- The catalog label `verified` supplies no source or kernel credit.

No canonical statement, Lean target, expression fingerprint, checked alternate encoding,
discovery protocol, obligation registry, or proof state is frozen at intake.
