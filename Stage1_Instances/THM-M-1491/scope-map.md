# THM-M-1491 scope map

## Preserved Repository Scope

The repository supplies the label `凸优化`, the gloss `凸函数的优化`, the collective attribution
`众多数学家`, the period `20世纪`, high importance, and an untrusted verified-status label. This
identifies convex optimization as a subject family. It does not state one mathematical theorem.

A familiar abstract model minimizes a convex objective on a convex feasible set. A familiar
finite-dimensional standard form minimizes a convex objective subject to convex inequalities and
affine equalities. These descriptions help expose missing choices, but neither is frozen as the
canonical target.

## Decisions Required At Statement Freeze

1. Select one immutable source proposition and decide whether the root concerns problem structure,
   minimizer existence, minimizer uniqueness, local-to-global optimality, first- or second-order
   conditions, KKT conditions, duality, sensitivity, an algorithm, convergence, or complexity.
2. Fix the optimization orientation and model: unconstrained or constrained, abstract or standard
   form, finite- or infinite-dimensional, real-valued or extended-real-valued, and exact or
   computational.
3. Fix the decision space, scalar field, topology, norm, order, domain, codomain, universes, and
   every typeclass assumption.
4. Fix the feasible-set representation, constraint index types, objective and constraint
   functions, equality/inequality direction, and all convexity, properness, continuity,
   semicontinuity, closedness, compactness, coercivity, differentiability, and qualification
   hypotheses actually used.
5. Fix the ordered quantifiers and the conclusion: existence or attainment, uniqueness, a local
   versus global comparison, derivative/subgradient condition, zero duality gap, error bound,
   convergence mode, rate, or computational complexity.
6. Fix whether minimizers are points, sets, infima in an extended order, approximate solutions, or
   values, and whether an optimum is assumed to exist or proved to exist.
7. Resolve empty domains and feasible sets, infeasible or unbounded problems, unattained infima,
   constant or affine objectives, non-strict versus strict convexity, boundary minimizers,
   nonunique minimizers, zero-dimensional spaces, and empty constraint families.
8. If an algorithm is intended, fix its update rule, oracle model, initialization, parameters,
   stopping rule, arithmetic model, convergence notion, error criterion, and cost model.
9. Admit an immutable source edition and exact theorem/page or definition locator; map every
   incorporated definition, assumption, conclusion, proof boundary, correction, and erratum; and
   obtain independent source and scope review.

## Explicit Exclusions

- Do not select local-minimum-implies-global merely because pinned mathlib already proves it.
- Do not substitute minimizer existence, uniqueness under strict convexity, Jensen's inequality,
  subgradient or derivative conditions, KKT, weak or strong duality, or an algorithmic convergence
  theorem without a source-approved identity decision.
- Do not collapse this target into the separately cataloged optimization-theory, linear-programming,
  simplex, interior-point, ellipsoid, KKT, Lagrangian-duality, or saddle-point targets.
- Do not replace the missing proposition with a finite-dimensional quadratic example, numerical
  optimizer run, benchmark, floating-point trace, or an assumed structure containing an optimum.
- Do not encode the requested conclusion as a hypothesis, axiom, opaque predicate, oracle, or
  unchecked certificate.
- Do not treat the catalog's `已验证` label, a textbook family definition, or the discovery-only
  mathlib probe as source identity or theorem proof evidence.

## Neighbor Target Boundaries

| Target | Boundary |
|---|---|
| `THM-M-1490` optimization theory | Broader optimization-theory topic; no scope or evidence is inherited. |
| `THM-M-1492` linear programming | Linear objectives and constraints form a specialized neighboring target. |
| `THM-M-1493` simplex method | A specific linear-programming algorithm, not generic convex optimization. |
| `THM-M-1494` interior-point method | An algorithm family requiring its own model and convergence theorem. |
| `THM-M-1495` ellipsoid method | A separate oracle/complexity algorithm target. |
| `THM-M-1506` KKT conditions | A specific optimality-conditions family, not automatically the root here. |
| `THM-M-1507` Lagrangian duality | A separate constrained-optimization duality family. |
| `THM-M-1508` saddle-point theorem | A separate minimax/optimality theorem family. |

## Prospective Proof-Route Boundary

If reviewers select the local-to-global theorem, a source-aligned route would restrict the convex
problem to the segment from a purported local minimizer to any better feasible point and derive a
nearby feasible point with smaller objective value. Existence, uniqueness, KKT, duality, and
algorithmic targets require different architectures. These are candidate planning boundaries only;
no obligation registry, proof tree, leaf budget, or closure credit is frozen at intake.
