# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-1396`, the label `Runge-Kutta方法`, the gloss `ODE的数值积分`,
the attribution Carl Runge/Martin Kutta, the year 1895, importance "high," and the untrusted status
`已验证`. This identifies a Runge-Kutta numerical-integration family for ordinary differential
equations. It does not identify one theorem.

## Proposition-changing decisions

Before an exact source statement can be frozen, an approved statement run must fix:

- the exact result: a stage/update identity, consistency or order characterization, local
  truncation error, global convergence or error estimate, stability result, invariant-preservation
  result, or another source-named proposition;
- the numerical scheme: explicit or implicit, number of stages, Butcher coefficients/tableau,
  stage equations, output weights, embedded pair if any, and whether the method is classical RK4,
  Euler, midpoint, Heun, or a general tableau;
- the initial-value problem: autonomous or time-dependent vector field, scalar or vector/Banach
  state, time interval, initial data, domain, and exact solution notion;
- vector-field assumptions such as continuity, local/global Lipschitz bounds, differentiability
  order, bounded derivatives, and an exact-solution existence interval;
- a fixed or variable step size, grid and final-time convention, admissible step-size bounds, and
  treatment of a last partial step;
- the norm, local/global error definition, convergence order, constants and their dependencies,
  uniformity in the grid, and whether the conclusion is finite-horizon or asymptotic;
- exact real arithmetic versus floating-point semantics, roundoff, overflow, and any computation
  or certificate policy; and
- the complete order of binders, typeclass assumptions, boundary cases, and direction of every
  implication or equivalence.

These choices produce materially different propositions. This list is a resolution ledger, not a
canonical statement.

## Candidate branches not credited

An eventual source-selected root might be one of the following, but none is asserted or credited:

- the one-step equations for a fixed explicit Runge-Kutta tableau;
- the classical fourth-order method's local truncation or global error bound under specified
  differentiability and Lipschitz assumptions;
- necessary and sufficient rooted-tree/Butcher order conditions for a general tableau;
- convergence of a consistent Runge-Kutta method on a finite interval under a stability or
  Lipschitz hypothesis;
- a source-specific absolute-stability function or stability-region theorem; or
- preservation of positivity, monotonicity, energy, symplectic structure, or another invariant by
  a specially constrained method.

The separate repository target `THM-M-1475` owns the topic "stability of Runge-Kutta methods" and
the gloss "stability regions of RK methods." Its statement and evidence cannot be absorbed into
this target without an accepted target-identity decision.

## Explicit exclusions

- Treating the method name or an update definition as a theorem.
- Silently selecting classical RK4, Euler, midpoint, Heun, Gauss, Radau, or another convenient
  method from the broad catalog label.
- Replacing this target by `THM-M-1395` finite differences, `THM-M-1397` Adams methods,
  `THM-M-1398` stiff equations, `THM-M-1399` backward differentiation formulas, or
  `THM-M-1475` Runge-Kutta stability.
- Assuming order, consistency, convergence, stability, or the desired error estimate in a
  structure field and projecting it as a proof.
- Proving only a scalar, linear, one-step, finite-grid, or low-order special case when the selected
  source has a broader domain.
- Replacing an exact theorem by a floating-point experiment, plot, simulation, sampled error
  table, unchecked symbolic order calculation, or generated tableau.
- Treating generic ODE existence, Picard iteration, Gronwall bounds, finite sums, or analytic
  derivatives as the Runge-Kutta theorem.
- Crediting the catalog label `已验证`, a paper title, the API probe, or a bounded no-match search as
  source fidelity or machine proof.

## Boundary cases

The statement phase must explicitly decide zero stages, empty or zero-length time intervals, zero
step size, a final time not on the grid, negative or variable steps, implicit stages with no or
multiple solutions, a vector field evaluated outside its domain, equilibrium and zero vector
fields, nonsmooth vector fields, exact solutions that cease to exist before the numerical horizon,
degenerate tableaux, vanishing weights, and whether constants remain uniform as the step tends to
zero.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides `ODE.IsIntegralCurveOn`, the
Picard integral operator, local ODE existence, Gronwall bounds, and estimates between approximate
ODE trajectories. Those are plausible ingredients for a future exact scheme and error theorem,
not a target selection or proof. The statement phase must first select and review one immutable
source proposition, then implement the source-mapped scheme definitions, minimize imports,
elaborate and fingerprint the exact target, add checked transports, and mutation-test every
required hypothesis, domain, binder-scope, and boundary change.
