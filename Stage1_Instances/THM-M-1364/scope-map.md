# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1364`, the title `Lorenz系统` (Lorenz system), Edward Lorenz,
the year 1963, and the gloss `混沌的经典例子` (a classic example of chaos). Importance `high`
and status `已验证` are catalog metadata, not source-fidelity or Lean evidence.

This identifies the Lorenz dynamical-system subject and its historical association with chaotic
behavior. It does not determine a theorem.

## Candidate families not credited

The following are distinct discovery hypotheses, not accepted formulations:

1. Define the Lorenz vector field
   `x' = sigma (y - x)`, `y' = x (rho - z) - y`, `z' = x y - beta z`, perhaps only for the
   conventional values `sigma = 10`, `rho = 28`, and `beta = 8/3`.
2. Prove an elementary analytic property such as equilibrium classification, symmetry, local
   existence, global boundedness, volume contraction, or existence of an absorbing region.
3. Prove a named chaos property for the classical flow: sensitive dependence, topological
   transitivity, dense periodic orbits, positive entropy, a horseshoe, or another exact predicate.
4. Prove existence of a geometric Lorenz attractor for an abstract class of singular hyperbolic
   flows rather than for the original polynomial equations.
5. Prove a rigorous strange-attractor statement for a source-selected parameter interval or point,
   possibly with computer-assisted estimates and an explicit certificate boundary.
6. Reproduce Lorenz's 1963 numerical nonperiodicity observations or phase portraits, which are
   historical evidence but not automatically a theorem in exact real dynamics.

No branch is selected or credited at intake. In particular, writing down the familiar equations is
not proof that the resulting flow satisfies an unspecified meaning of "chaos."

## Proposition-changing decisions

An approved statement phase must freeze all of the following from an immutable source:

- whether the root is a definition, an elementary property, a qualitative dynamics theorem, a
  geometric-model theorem, or a computer-assisted result for the polynomial Lorenz equations;
- the exact vector field, sign and coordinate conventions, state space, time domain, scalar field,
  regularity, solution and maximal/global-flow semantics, and whether parameters are variables or
  fixed constants;
- all parameter domains and exact values, including whether decimal values are exact rationals and
  whether the source uses `b`, `beta`, `r`, or `rho` conventions;
- the exact definition of attractor and of chaos, including invariant set, compactness, basin,
  transitivity, sensitive dependence, periodic-orbit, entropy, SRB-measure, singular-hyperbolic, or
  geometric-return-map clauses;
- whether a conclusion is analytic, topological, measure-theoretic, computational, or a conjunction,
  and the exact locality, uniformity, constants, exceptional sets, and certificate tolerances;
- how a theorem about a geometric Lorenz model, nearby vector fields, a Poincare return map, or a
  parameter interval transports to the original three-dimensional equations; and
- every ordered binder, hypothesis, conclusion, incorporated definition, proof boundary,
  correction or errata decision, and boundary convention.

## Boundary cases to resolve

- zero or negative `sigma`, `rho`, or `beta`, including degenerate invariant planes, nonisolated
  equilibria, and loss of ordinary dissipativity assumptions;
- the bifurcation thresholds `rho = 1` and other source-specific critical parameter values;
- initial data at an equilibrium, on a stable manifold, on a symmetry-related orbit, or outside a
  proposed absorbing set;
- finite-time versus global solutions and forward semiflow versus two-sided flow semantics;
- empty, singleton, noncompact, or nonmaximal invariant sets counted as attractors by weak
  definitions;
- exact real dynamics versus floating-point or interval arithmetic, including rounding, enclosure,
  termination, and trusted-certificate boundaries; and
- sensitivity measured over all points, a dense set, almost every point, or only numerically sampled
  trajectories, with the metric and time quantifiers made explicit.

## Explicit exclusions

- the Lorenz equations alone presented as a theorem that chaos exists;
- a rendered butterfly plot, sampled trajectory, numerical divergence, or floating-point Lyapunov
  exponent presented as exact proof;
- a simple fact such as local ODE existence, equilibrium enumeration, or negative divergence
  substituted for the unspecified full chaos claim;
- a geometric Lorenz flow, horseshoe, shift map, or abstract attractor theorem substituted without
  a checked source-prescribed bridge to the selected polynomial system;
- a structure or hypothesis that assumes the desired chaotic invariant set, attractor, return map,
  transitivity, sensitivity, or entropy conclusion;
- nearby targets `THM-M-1363` (chaos theory), `THM-M-1365` (Smale horseshoe), `THM-M-1403`
  (topological entropy), `THM-M-1418` (Lyapunov exponent), or `THM-M-1425` (random attractor) used
  as replacement roots; and
- the catalog's untrusted `已验证` label used as source or proof evidence.

No canonical proposition or excluded degenerate case is frozen at intake. The exact-source
statement phase owns those decisions, and all downstream nodes remain open.
