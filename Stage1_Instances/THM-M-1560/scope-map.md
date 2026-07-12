# Scope map

## Included claim family

- An explicitly selected matrix Riemann-Hilbert problem with oriented contour, normalized unknown,
  jump matrix, and source-required regularity and invertibility conditions.
- Oscillatory dependence on large space-time parameters and a fixed asymptotic regime.
- The source-supported deformation sequence: factorization, contour deformation, normalization,
  local parametrices near stationary points, an outer model, and a small-norm error problem.
- Solvability and quantitative estimates at every transformation needed by the selected theorem.
- Reconstruction of the associated integrable-system solution from the Riemann-Hilbert solution.
- The exact leading asymptotic term and uniform error estimate asserted by the selected source.

The 1993 modified-KdV application is the leading candidate because it agrees with the repository's
authors and date and with the official journal title. It is not silently promoted to an exact
canonical claim during intake.

## Decisions required at statement freeze

The statement phase must pin an immutable primary-source edition and one theorem/page, then freeze:

- the modified-KdV normalization or another explicitly justified integrable evolution;
- initial-data/scattering-data spaces, reality and symmetry conditions, and decay assumptions;
- treatment of reflection coefficients, poles/discrete spectrum, and spectral singularities;
- contour geometry, orientation, jump relation, normalization, and matrix dimension;
- the space-time scaling variable and sector, including stationary and transition points;
- the model problem and special-function conventions used in the leading term;
- reconstruction formula, all constants and phases, error norm/rate, and uniformity quantifiers;
- degenerate data and boundary rays, ordered Lean binders, universes, typeclasses, and imports.

The selected source statement must be separated from the method's general reusable architecture.
If the root is a specific modified-KdV asymptotic theorem, a general nonlinear-steepest-descent
framework may support it but cannot substitute for its conclusion.

## Explicit exclusions

- Classical finite-dimensional steepest descent or saddle-point integration alone.
- A generic statement saying that a method works, without a quantified proposition.
- The separately scheduled Riemann-Hilbert problem `THM-M-1559` as a substitute for the asymptotic
  theorem; the latter requires deformation, estimates, and reconstruction in addition to a problem
  formulation.
- A structure whose fields assume solvability, small-norm estimates, or the desired final
  asymptotic formula and a theorem that merely projects those fields.
- Only a formal contour rewrite, matrix factorization, stationary-phase lemma, or special case when
  the reviewed source claims a full long-time asymptotic result.
- Claims about nonlinear Schrödinger, KdV, random matrices, orthogonal polynomials, or later
  applications unless source review explicitly changes and re-approves the target scope.

No obligation registry or Lean expression is frozen at intake. Those artifacts depend on selecting
the exact theorem without broadening or weakening it.
