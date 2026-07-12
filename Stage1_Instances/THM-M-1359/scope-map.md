# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1359`, the title `鞍结分岔` (saddle-node bifurcation), the gloss
`平衡点消失的分岔` (a bifurcation in which equilibria disappear), the generic attribution to many
mathematicians, and the 20th-century date. Importance `high` and status `已验证` are catalog
metadata, not source-fidelity or Lean evidence.

The intended subject is a parameter-dependent dynamical system whose equilibrium set undergoes a
fold. This subject-level boundary does not determine one theorem.

## Candidate families not credited

The following are distinct discovery hypotheses, not accepted formulations:

1. Prove directly that the scalar normal form `x' = mu + x^2` has two equilibria for `mu < 0`, one
   double/nonhyperbolic equilibrium for `mu = 0`, and none for `mu > 0`, with the two branches having
   opposite stability.
2. For a scalar equation `f(x, mu) = 0`, derive a local two/one/zero root classification from a
   critical zero, vanishing state derivative, nonzero parameter derivative, and nonzero second state
   derivative.
3. For a smooth finite-dimensional vector-field family, prove a local saddle-node theorem under a
   simple zero eigenvalue, exclusion of other center spectrum, and source-specific transversality and
   quadratic nondegeneracy conditions, usually through reduction to a scalar normal form.
4. State a fold of fixed points for a parameterized discrete map rather than equilibria of an ODE.
5. Prove only a necessary condition for changing the number of equilibria, such as failure of the
   ordinary implicit-function hypothesis, rather than the sufficient generic bifurcation theorem.

These claims are not interchangeable. In particular, the scalar example cannot stand in for a
general vector-field theorem, and an implicit-function obstruction does not establish a fold.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from an immutable source:

- whether the dynamics is a scalar ODE, a parameterized equation, a finite-dimensional vector field,
  a flow, or a discrete map, together with the phase space, parameter space, dimensions, scalar field,
  and regularity;
- the critical state and parameter, the equilibrium or fixed-point equation, and the exact local
  neighborhoods in which an existence, uniqueness, and root-count assertion is made;
- whether the derivative condition is scalar `f_x = 0`, a simple zero eigenvalue, a one-dimensional
  kernel/cokernel, or another Fredholm condition, and which other spectrum is excluded;
- the left/right nullvectors or projections used to state parameter transversality and the nonzero
  quadratic coefficient in a multidimensional formulation;
- whether the conclusion is a normal-form conjugacy, orbital/topological equivalence, a smooth
  solution curve with a fold, an exact local zero count, stability of branches, or a conjunction;
- allowed coordinate, time, state, and parameter reversals and how they determine which parameter
  side has zero or two equilibria;
- whether center-manifold or Lyapunov-Schmidt reduction is assumed, derived, or part of the proof
  obligations; and
- every ordered binder, hypothesis, conclusion, incorporated definition, proof boundary, correction
  or errata decision, and boundary convention.

## Boundary cases to resolve

- failure of parameter transversality or a vanishing quadratic coefficient, producing a higher-order
  degeneracy rather than a generic saddle-node;
- a zero eigenvalue of multiplicity greater than one or additional imaginary-axis/center spectrum;
- nonsmooth families, incomplete flows, nonisolated continua of equilibria, and other equilibria
  entering the chosen neighborhood;
- the critical equilibrium counted once, twice by multiplicity, or only as a branch-collision point;
- parameter or time reversal and the resulting stable/unstable label swap;
- global equilibrium claims inferred from a theorem that is only local; and
- zero-dimensional/trivial phase spaces, boundary equilibria, constrained domains, and discrete-map
  fixed points confused with ODE equilibria.

## Explicit exclusions

- `x' = mu + x^2` or another convenient normal form substituted for an unspecified general theorem;
- a plot, numerical continuation trace, sampled trajectory, or floating-point root count;
- the statement "equilibria disappear" without the critical case, occupied parameter side, local
  quantifiers, uniqueness/count convention, and nondegeneracy hypotheses;
- a structure or premise that assumes the desired fold, normal form, branch count, or stability;
- Hopf, transcritical, pitchfork, cusp, or generic bifurcation theory substituted by proximity or
  terminology;
- failure of the implicit-function theorem presented as sufficient proof of a saddle-node; and
- the catalog's untrusted `已验证` label used as source or proof evidence.

No canonical proposition or excluded degenerate case is frozen at intake. The exact-source
statement phase owns those decisions, and all downstream nodes remain open.
