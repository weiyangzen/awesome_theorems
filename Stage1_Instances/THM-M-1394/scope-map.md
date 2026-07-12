# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1394`, the title `打靶法`, the gloss `边值问题的数值方法`, the
attribution to many mathematicians, and the twentieth-century date. Importance `high` and status
`已验证` are catalog metadata, not human-source or kernel evidence.

The wording constrains the subject to shooting as numerical treatment of boundary-value problems.
It does not identify an ODE, boundary operator, shooting construction, numerical solver, or one
proposition. A later statement phase may select a result only from an immutable, independently
reviewed source passage.

## Candidate families not credited

The following are distinct discovery hypotheses, not accepted formulations of this target:

1. Equivalence between a selected boundary-value problem and a root of the endpoint residual for a
   family of exact initial-value solutions.
2. Existence, uniqueness, continuity, differentiability, or conditioning of that residual map.
3. Existence of a shooting parameter by an intermediate-value or topological argument.
4. Single-shooting or multiple-shooting solvability for a selected linear or nonlinear problem.
5. Local or global convergence of bisection, secant, Newton, or another selected residual solver.
6. Convergence, consistency, stability, or an error bound when each initial-value problem is solved
   only approximately by a selected numerical integrator.

A method label cannot silently become the conjunction of these results, and no special case may
replace an unstated general root.

## Proposition-changing decisions

Before statement work can close, an immutable source and independent review must fix:

- the exact numbered theorem or source-defined conjunction and its incorporated definitions;
- ODE order or first-order system, time interval, scalar/vector/Banach state, and all universes;
- linear or nonlinear dynamics, autonomous or nonautonomous field, regularity, and exact solution
  notion;
- two-point, multipoint, separated, coupled, linear, or nonlinear boundary data;
- the shooting parameter and map from missing initial data to the terminal boundary residual;
- initial-value existence, uniqueness, maximal interval, continuous dependence, and domain safety;
- single versus multiple shooting, subinterval matching conditions, and every conditioning premise;
- exact root existence/uniqueness or numerical root-solver conclusion, iteration, initialization,
  tolerances, derivative/nondegeneracy conditions, and stopping rule;
- exact versus approximate IVP solves, integrator, grid/step policy, arithmetic, norm, constants,
  convergence/error/stability conclusion, and quantifier order; and
- every correction, erratum, proof boundary, boundary case, and source-to-node mapping.

## Degenerate cases to resolve

- coincident endpoints, empty or zero-length intervals, inconsistent or already-satisfied boundary
  data, and an empty shooting-parameter space;
- constant or zero vector fields, equilibrium solutions, singular boundary operators, and multiple
  or absent boundary-value solutions;
- non-Lipschitz fields, nonunique initial-value solutions, finite-time blow-up, and a shot leaving
  the vector-field domain before the terminal endpoint;
- a constant, discontinuous, nondifferentiable, flat, singular-Jacobian, or multi-root residual;
- a bracket without a sign change, a Newton iterate outside the admissible set, and multiple-
  shooting matching systems with singular Jacobians;
- exact-real versus floating-point arithmetic, IVP discretization and roundoff error, step zero or
  negative step, adaptive grids, and constants not uniform in the requested limit.

No case is excluded at intake because no proposition has been selected.

## Neighbor and substitution exclusions

- `THM-M-1383` owns the generic boundary-value-problem family; its existence or uniqueness theorem
  cannot be relabeled as shooting.
- `THM-M-1392` Green representation and `THM-M-1393` Fredholm alternative remain separate analytic
  targets.
- `THM-M-1395` finite differences, `THM-M-1396` Runge-Kutta, and `THM-M-1397` Adams methods retain
  their own ownership. A later shooting theorem may depend on an IVP integrator without consuming
  that integrator's separate target.
- An IVP existence theorem, intermediate value theorem, continuous-dependence theorem, or Gronwall
  estimate alone is substrate, not a shooting-method theorem.
- Defining a residual or calculating one sample trajectory is not a proof of BVP equivalence,
  solvability, convergence, stability, or error.
- Storing a desired BVP solution, residual root, convergence fact, or error bound in a structure or
  hypothesis supplies no proof.
- Floating-point experiments, plots, sampled residuals, or unchecked solver output receive no
  machine proof credit.
- The repository's `已验证` label and this intake probe receive no source-fidelity or kernel credit.

## Formal boundary

Pinned mathlib exposes exact integral-curve predicates, local Picard-Lindelof existence, ODE
uniqueness, approximate-trajectory estimates, and the intermediate value theorem. The probe
authenticates these adjacent interfaces only. It does not select a boundary-value problem, shooting
map, residual solver, or theorem conclusion. The exhaustive repo-local, mathlib, and external Lean
anchor audit remains downstream.
