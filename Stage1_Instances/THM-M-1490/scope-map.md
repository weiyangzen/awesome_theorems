# THM-M-1490 scope map

## Preserved catalog scope

- Target identity: `THM-M-1490`, named `优化理论` (`optimization theory`).
- Literal gloss: `数学优化的理论` (`the theory of mathematical optimization`).
- Attribution and time: many mathematicians, twentieth century.
- Category: other important fields / numerical analysis.

This wording identifies a research field. Intake preserves that boundary instead of silently
turning the field into a selected existence, optimality, duality, or algorithm theorem.

## Proposition-changing decisions

An accountable correction must select one immutable proposition and freeze:

1. The claim family: optimizer existence or attainment, uniqueness, necessary or sufficient
   optimality, local-to-global transfer, perturbation or stability, duality, or algorithmic
   correctness, convergence, rate, or complexity.
2. The direction and solution object: minimization or maximization; minimizer, infimum value,
   approximate minimizer, stationary point, saddle point, multiplier, trajectory, or certificate.
3. The decision domain and universes: finite set, Euclidean space, normed or topological vector
   space, manifold, function space, combinatorial structure, or another source-defined type.
4. The scalar field, order, topology, norm, metric, measurability structure, and objective codomain,
   including whether extended values are permitted.
5. The objective and feasible set: constrained or unconstrained form, equality and inequality
   conventions, parameterization, feasibility, and any set regularity.
6. The analytical assumptions: continuity or semicontinuity, coercivity, compactness, convexity or
   strict/strong convexity, smoothness, derivative order, Lipschitz constants, or nonsmooth data.
7. The optimum notion: local or global, strict or non-strict, exact or approximate, primal or dual,
   attained or merely an infimum/supremum.
8. For an algorithmic claim, the update rule, initialization, step-size policy, stopping rule,
   oracle model, randomness and probability space, and quantifier order.
9. The arithmetic and computation model: exact real mathematics, rational or discrete arithmetic,
   floating point, certificates, external solvers, sampling, or empirical measurement.
10. The exact conclusion, constants, asymptotic regime, rates, complexity measure, and whether the
    result is deterministic, almost sure, in probability, in expectation, or high probability.
11. Every ordered binder, implicit typeclass assumption, alternate encoding, and checked transport.
12. The primary source edition and pinpoint theorem, incorporated definitions, proof boundary,
    corrections or errata, translation policy, and independent source-selection review.

## Boundary and degenerate cases

No case is excluded before a proposition is selected. A later statement must explicitly decide at
least empty and singleton domains, empty or inconsistent feasible sets, constant objectives,
unbounded objectives, unattained infima or suprema, nonunique optimizers, boundary optima, zero
dimensions, zero iterations, zero or invalid step sizes, singular derivatives or Hessians, failed
constraint qualifications, infinite values, and algorithm nontermination.

## Neighbor ownership

The following catalog targets separately own major optimization subfamilies. This intake inherits
no statement or proof evidence from them:

| Target | Separate topic |
|---|---|
| `THM-M-1491` | convex optimization |
| `THM-M-1492` | linear programming |
| `THM-M-1493` to `THM-M-1495` | simplex, interior-point, and ellipsoid methods |
| `THM-M-1496` to `THM-M-1497` | semidefinite and conic programming |
| `THM-M-1498` to `THM-M-1505` | gradient, stochastic, Newton, quasi-Newton, BFGS, conjugate-gradient, trust-region, and Levenberg-Marquardt methods |
| `THM-M-1506` to `THM-M-1509` | KKT, Lagrangian duality, saddle points, and minimax |

The extreme-value theorem (`THM-M-0635`) and Ekeland variational principle (`THM-M-1270`) are also
distinct source families, not aliases for this topic label.

## Explicit exclusions

- Do not choose a compactness existence theorem, a convex local-to-global theorem, a first-order
  condition, KKT, duality, minimax, or any named algorithm merely because it is familiar.
- Do not combine several neighboring theorems into a broader conjunction or redefine the root as a
  survey of optimization.
- Do not encode the missing claim as an opaque predicate, an assumption containing the conclusion,
  a certificate field projected from an input, or unchecked solver output.
- Do not treat a definition, API check, numerical experiment, catalog status, or successful build
  as proof of the received target.

## Retry condition

The statement phase can proceed only after accountable reviewers select and hash one immutable
source proposition, resolve every decision above without crossing neighboring ownership, map its
definitions, assumptions, conclusion, proof and errata, and independently approve the mapping.
Only then can a worker elaborate a minimal-import Lean target and run the required statement
mutations.
