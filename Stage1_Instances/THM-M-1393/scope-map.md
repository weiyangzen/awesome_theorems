# Scope map

## Preserved theorem family

The intake preserves the catalog's ODE boundary-value reading of the Fredholm alternative: a
solvability dichotomy or compatibility criterion for a linear boundary-value problem, ordinarily
obtained through an identity-minus-compact, integral-operator, or Fredholm-operator realization.
Possible components, none yet credited as the theorem, include:

- a linear differential expression or closed operator with a source-specified domain;
- boundary functionals and their adjoint boundary conditions;
- a homogeneous equation and its finite-dimensional solution space;
- an inhomogeneous equation with prescribed forcing and boundary data;
- an alternative between unique solvability and a nonzero homogeneous solution;
- a range or adjoint-kernel orthogonality condition for solvability; and
- a compact Green or integral operator reducing the boundary-value problem to `(I - lambda K)u = f`.

## Decisions required at statement freeze

1. Preserve and hash a lawful complete source edition, select an exact result and proof boundary,
   map every incorporated definition, and obtain independent source review.
2. Fix whether the root is a differential boundary-value theorem, an integral-equation theorem, an
   identity-minus-compact operator theorem, or a spectral formulation. Do not merge the contracts.
3. Fix the scalar field, interval or domain, state and forcing spaces, differential order,
   coefficient regularity, operator domain, topology, norm, and completeness assumptions.
4. Fix every boundary condition, compatibility condition, adjoint operator and adjoint boundary
   condition, pairing or inner product, and real/complex conjugation convention.
5. Fix the compactness or Fredholm hypothesis and its provenance, including any Green-kernel or
   integral-operator reduction and the sign/scalar convention for `I - lambda K`.
6. State the exact alternative: disjunction or exclusive disjunction; injectivity, surjectivity, or
   bijectivity; existence for one forcing or every forcing; uniqueness; homogeneous-nullspace
   dimension; range/cokernel relation; and any Fredholm-index claim.
7. Freeze ordered binders and quantifier dependencies, especially whether the forcing is fixed or
   universal and whether a nonzero spectral parameter is quantified or fixed.
8. Resolve all degenerate and boundary cases, foundation/choice assumptions, alternate encodings,
   and checked transports before any candidate proof receives credit.

## Degenerate and boundary cases

Source review must explicitly dispose of zero or finite-dimensional spaces; the zero operator;
`lambda = 0`; empty, zero-length, reversed, or singular intervals; zero forcing; incompatible
boundary data; repeated eigenvalues; nontrivial homogeneous solutions; failure of compactness or
closed range; nonsmooth or singular coefficients; real versus complex scalars; non-dense operator
domains; self-adjoint versus non-self-adjoint problems; adjoint kernel equal to zero; and the
difference between membership in a range and pointwise/classical solvability.

No case is excluded at intake. A statement that assumes invertibility, a solution, the range
criterion, the desired alternative, or a prepackaged Fredholm conclusion is circular.

## Neighbor and substitution exclusions

- `THM-M-0315` separately owns the functional-analysis Fredholm-alternative record with the gloss
  "solvability of compact-operator equations." Its scope, pinned candidate, and any future evidence
  cannot be copied into this ODE boundary-value target.
- `THM-M-1161` separately owns Fredholm integral equations in the PDE catalog. An integral-equation
  formulation may be a bridge only after a selected source and checked reduction; it is not this
  target by title alone.
- `THM-M-1383` owns generic boundary-value problems, `THM-M-1384` Sturm-Liouville theory, and
  `THM-M-1392` Green functions. None selects or proves this solvability alternative.
- The compact-operator spectral theorem, Riesz-Schauder theory, analytic Fredholm theorem, Fredholm
  index theory, numerical shooting, finite differences, and a single special boundary problem are
  not substitutes for the source-selected root.
- `IsCompactOperator.hasEigenvalue_or_mem_resolventSet` is a strong formal candidate, but theorem
  name agreement does not establish the differential-BVP reductions, source identity, or exact
  expression required here.
- The repository's `verified` label, an API probe, a citation, or another target's receipt supplies
  no source, statement, or proof credit.

## Formal boundary

Lean 4 with pinned mathlib is the selected backend. Pinned mathlib exposes compact continuous linear
operators, eigenvalues, spectra and resolvent sets, and generic ODE integral-curve predicates. The
probe authenticates only those interfaces. It does not define the catalog's differential operator,
boundary data, adjoint boundary problem, solvability pairing, compact reduction, or parent
composition. No canonical Lean target, expression fingerprint, checked transport, mutation suite,
or proof body is claimed at intake.
