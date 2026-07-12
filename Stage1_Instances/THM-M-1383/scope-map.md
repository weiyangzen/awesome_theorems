# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1383`, the label `边值问题` (boundary-value problems), the
gloss `两点边值问题的理论` (the theory of two-point boundary-value problems), a collective
twentieth-century attribution, and an untrusted `已验证` (`verified`) status. Intake preserves this
ordinary-differential-equations subject boundary. It does not turn the topic into a proposition or
silently select a textbook theorem.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- the independent-variable interval, its two endpoint conventions, scalar or state space,
  universes, topology, norm, and differentiability structures;
- a scalar equation, first-order system, second-order equation, linear differential operator,
  nonlinear operator, eigenvalue problem, or another precisely typed dynamics model;
- coefficient, forcing, and parameter domains and regularity, plus whether the problem is regular
  or singular and autonomous or nonautonomous;
- the solution concept and regularity, including pointwise, classical, weak, Sobolev, integral, or
  another source-defined solution;
- separated or coupled endpoint operators and data, including Dirichlet, Neumann, Robin, periodic,
  homogeneous, or inhomogeneous conditions;
- existence, uniqueness, nonexistence, multiplicity, continuous dependence, solvability,
  representation, spectral, estimate, or approximation as the exact conclusion; and
- ordered binders, all compatibility, coercivity, compactness, Lipschitz, monotonicity,
  nonresonance, eigenvalue, sign, and boundary hypotheses, plus every degenerate case.

These choices yield inequivalent propositions. They are a resolution ledger, not a canonical
claim. The word `theory` also leaves open whether the target is one theorem or a conjunction;
intake may not manufacture either interpretation.

## Candidate families not credited

- Existence and uniqueness for a two-point nonlinear ODE boundary-value problem under a
  source-specific contraction, shooting, monotonicity, upper/lower-solution, or variational regime.
- A linear solvability or Fredholm alternative theorem, including compatibility conditions at
  resonance.
- The regular Sturm-Liouville spectral theorem, oscillation theory, or endpoint eigenvalue facts.
- A Green-function or integral representation theorem for one selected operator and boundary
  condition.
- Well-posedness, an a priori estimate, or convergence and error bounds for a shooting,
  finite-difference, collocation, or finite-element scheme.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor boundaries and exclusions

- `THM-M-1384` through `THM-M-1391` separately schedule records for Sturm-Liouville theory, Sturm
  comparison and separation, oscillation theory, eigenvalue problems, Weyl asymptotics, the Courant
  min-max principle, and the Prufer transform. Their future statements or evidence do not define
  this root.
- `THM-M-1392`, `THM-M-1393`, and `THM-M-1394` separately schedule Green-function, Fredholm-
  alternative, and shooting-method records. None may replace the broad source label or donate proof
  credit.
- PDE targets `THM-M-1149`, `THM-M-1150`, and `THM-M-1151` separately schedule Dirichlet, Neumann,
  and Robin problem records, and `THM-M-1163` schedules a PDE-category Green-function record. They
  are outside this ODE target's subject boundary.
- Initial-value Picard-Lindelof existence or Gronwall uniqueness is not a two-endpoint solvability
  theorem. Replacing full initial data with two-endpoint constraints can destroy existence or
  uniqueness.
- A multipoint boundary condition is outside the literal two-point wording unless an approved
  source correction explicitly changes the target.
- An equation with the desired endpoint solution assumed as a hypothesis, a structure field that
  stores a solution, a finite example, or a numerical trajectory supplies no general proof.
- Generic interval, derivative, integral-curve, initial-value, compactness, or continuity APIs
  receive no statement or proof credit.
- The catalog label `已验证` supplies neither a human proof nor a kernel-checked artifact.

## Boundary cases

The later statement phase must decide coincident or reversed endpoints; empty or singleton state
spaces; zero-order or degenerate leading coefficients; zero-length intervals; homogeneous zero
data; incompatible endpoint data; resonance and nontrivial homogeneous kernels; singular endpoints;
nonunique initial-value dynamics; finite-time blow-up; discontinuous coefficients; weak versus
classical regularity; coupled versus separated conditions; and whether existence, uniqueness, or
both are asserted for every admissible datum.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe authenticates interval,
integral-curve, Picard-Lindelof local initial-value existence, and Gronwall initial-value uniqueness
interfaces. A bounded exact-topic search found no boundary-value occurrence in pinned mathlib and
no two-point boundary occurrence in pinned mathlib or repo-local Lean sources. Unrelated repo-local
uses of the generic words `boundary value` receive no credit. This is an intake discovery
observation, not an exhaustive anchor audit or a global absence claim.
