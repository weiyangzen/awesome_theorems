# Scope map

## Preserved scope

The only scope supported by the repository is a Lagrangian-duality theorem family for constrained
optimization. A familiar finite-dimensional minimization template would introduce an objective,
inequality and equality constraints, a Lagrangian, its infimum over decision variables, nonnegative
inequality multipliers, and a maximization over multipliers. This template is useful for listing
missing decisions, but it is not the accepted target.

## Decisions required at statement freeze

1. Whether the root is a definition/construction result, weak duality, strong duality, attainment,
   complementary slackness, sensitivity, or an equivalence involving optimality or saddle points.
2. Whether the primal is a minimization or maximization problem and whether it is general
   nonlinear, convex, linear, quadratic, conic, Fenchel-type, finite-dimensional, or
   infinite-dimensional.
3. The decision space, scalar field, topology, objective codomain (`Real` or an extended-real
   type), and all universe and typeclass assumptions.
4. The inequality and equality constraint indices, constraint functions, feasible set, sign and
   feasibility conventions, and treatment of absent constraint families.
5. The multiplier spaces, sign restrictions, Lagrangian sign convention, and ordered binders.
6. The definitions of primal value, dual function, dual feasible set, dual problem, dual value,
   and duality gap, including `inf`/`sup` and infinite-value conventions.
7. If strong duality is intended, the exact convexity, properness, lower-semicontinuity,
   closedness, constraint qualification, relative-interior, and primal/dual attainment hypotheses.
8. The behavior for empty or infeasible primal/dual feasible sets, unbounded objectives, zero
   constraints, redundant constraints, unattained extrema, and infinite optimal values.
9. An immutable primary source edition, exact theorem/page or definition locator, assumptions,
   errata audit, translation policy, and independent source-selection review.

## Explicit exclusions

- Do not select weak duality merely because it is broadly valid, or strong duality without the
  source-fixed constraint qualification and conventions.
- Do not substitute `THM-M-1506` (KKT conditions), `THM-M-1508` (saddle-point theorem), or
  `THM-M-1509` (von Neumann minimax), and do not inherit any future evidence from those targets.
- Do not substitute Lagrange multipliers, linear/conic/Fenchel duality, complementary slackness,
  or a special numerical optimization problem for the unspecified root.
- Do not encode the missing theorem as an opaque predicate, hypothesis, certificate field, axiom,
  or existential data projected from an assumption.
- Do not treat generic order lemmas, dual-cone separation, the catalog label `已验证`, or the
  discovery-only Lean probe as a Lagrangian-duality proof.

## Prospective proof-route boundary

Once a source-approved proposition exists, weak duality would normally reduce to the statement
that every dual-feasible multiplier gives a lower bound on every primal-feasible point, followed by
an infimum/supremum argument. Strong duality needs additional geometric or convex-analytic work and
source-specific constraint qualifications. These are only possible obligation-tree seeds; no
obligation registry or closure credit is frozen at intake.
