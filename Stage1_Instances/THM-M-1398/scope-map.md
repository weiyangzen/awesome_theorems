# Scope map

## Preserved source boundary

The intake preserves only the received topic: numerical treatment of a source-selected stiff
ordinary differential equation problem. An eventual exact root must include every mathematical
object and conclusion in its approved source passage; intake does not select one candidate.

## Proposition-changing decisions

The statement phase must obtain an immutable source proposition and freeze:

1. The definition or diagnostic of stiffness, including whether it uses separated decay scales,
   eigenvalue or Jacobian information, a stability-versus-accuracy step restriction, or another
   problem-and-method-dependent criterion.
2. The equation class: scalar or system, real or complex, autonomous or nonautonomous, linear or
   nonlinear, initial or boundary value, finite-dimensional or function-space valued.
3. The time interval, initial data, solution concept, existence and uniqueness assumptions,
   regularity, dissipativity, spectral, Jacobian, Lipschitz, and norm hypotheses.
4. The exact numerical method and every coefficient, stage, recurrence, implicit solve, starting
   value, step grid, variable- or fixed-step restriction, and solvability assumption.
5. Whether arithmetic is exact, floating point, interval, or certificate based, and what rounding,
   nonlinear-solver, stopping-tolerance, and failure model is allowed.
6. The truth-valued conclusion: well-definedness, consistency, order, stability, convergence,
   global/local error, stiffness-independent bound, computational complexity, or an exact bundle.
7. Ordered binders, constants, parameter dependencies, quantifier scope, strictness, endpoint
   conventions, and every boundary or degenerate case.

These choices produce materially different propositions. They are requirements for target repair,
not a canonical statement.

## Candidate families not credited

- Analysis of backward Euler on the scalar test equation `y' = lambda y`.
- A-stability or L-stability of a source-selected one-step method.
- Stability and convergence of a source-selected implicit Runge-Kutta method.
- Zero-stability, consistency, convergence, or a barrier theorem for a linear multistep method.
- Stability or convergence of a backward differentiation formula on a source-selected stiff IVP.
- An error estimate comparing a discrete interpolant with an exact ODE trajectory.

No candidate in this list is selected or credited at intake.

## Explicit exclusions

- `THM-M-1399`, the separately cataloged backward differentiation formula target.
- `THM-M-1476`, `THM-M-1477`, and `THM-M-1478`, which separately own stiff stability,
  A-stability, and L-stability topic labels.
- Replacing the arbitrary source topic with the Dahlquist scalar test equation, implicit Euler, a
  low-dimensional worked example, or a single numerical experiment.
- Treating a definition of stiffness, a plotted decay curve, benchmark results, or successful
  floating-point runs as a theorem.
- Assuming consistency, stability, convergence, existence of an implicit step, or the desired
  error estimate as a structure field or hypothesis and then projecting it.
- Crediting generic mathlib ODE existence, uniqueness, or Gronwall results as a numerical-method
  theorem merely because they are relevant substrate.
- Crediting the catalog's `已验证` label as primary-source or Lean-kernel evidence.

## Degenerate and boundary scope

The exact source must decide zero step size, empty or reversed time intervals, zero-dimensional
state, constant or zero vector fields, zero or purely imaginary eigenvalues, singular Jacobians,
nonunique exact or implicit-step solutions, repeated or clustered modes, inconsistent initial
data, variable steps, rejected steps, and any method-order or stability-region boundary. Intake
silently excludes none of them.

No canonical Lean target or obligation registry is frozen in this phase.
