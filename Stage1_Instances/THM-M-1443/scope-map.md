# Scope map

## Preserved repository scope

The repository fixes only the label `不动点迭代`, the gloss `方程求根的迭代方法`, the collective
attribution `众多数学家`, the period `20世纪`, importance "high," and an untrusted `已验证`
status. This identifies fixed-point iteration as a numerical root-finding method, but supplies no
bibliographic source, theorem locator, definition, premise, or conclusion.

The intake preserves only that topic boundary. It does not infer a canonical proposition from the
usual recurrence `x_(n+1) = g(x_n)`.

## Proposition-changing decisions

An approved source correction must freeze:

- the equation `F(x) = 0` and the exact transformation or equivalence connecting its roots to
  fixed points of a specified self-map `g`;
- the scalar or general metric/normed space, domain and codomain, subset or interval, metric or
  norm, topology, completeness assumptions, and all universes and typeclasses;
- the initial point or class of initial points, the recurrence and iterate-index convention, and
  whether the iterates remain in a source-specified invariant domain;
- all continuity, differentiability, Lipschitz, contraction, monotonicity, derivative-bound,
  compactness, or localization hypotheses, including where they hold;
- the exact conclusion: well-definedness, existence or uniqueness of a fixed point/root,
  convergence of iterates, convergence mode, local or global basin, rate, a priori or a posteriori
  error bound, stopping criterion, or an exact conjunction;
- the ordered binders, uniformity of constants and exceptional sets, numerical representation, and
  whether finite-precision computation or a certificate is part of the claim; and
- every boundary case and the precise relation to the separately cataloged Banach fixed-point
  theorem `THM-M-1444`.

These choices yield inequivalent propositions. They are a resolution checklist, not a canonical
statement.

## Candidate families not credited

- A purely definitional recurrence `x_(n+1) = g(x_n)`.
- A limit-transfer theorem: if the iterates converge and `g` is continuous at their limit, the
  limit is a fixed point.
- The Banach/Picard iteration theorem for a contraction on a complete nonempty metric space,
  including existence, uniqueness, convergence, and geometric error estimates.
- A one-dimensional interval theorem based on derivative bounds or monotonicity.
- A local convergence theorem around an already known fixed point.
- Correctness and termination of a finite-precision fixed-point solver with a stopping rule.

No family in this list is selected or credited at intake.

## Explicit exclusions

- `THM-M-1444` Banach fixed-point theorem as a silent replacement. The neighboring catalog entry
  separately names it and gives the different gloss `压缩映射的不动点`.
- Newton, secant, or bisection methods (`THM-M-1440`, `THM-M-1441`, and `THM-M-1442`), even if they
  can be represented using an iteration map.
- A theorem that assumes the desired root, fixed point, convergence, error estimate, or solver
  correctness as a hypothesis or structure field.
- A constant or identity-map toy example, finite sampled trajectory, plot, floating-point run, or
  empirical stopping event presented as a general convergence theorem.
- Pinned mathlib's iteration, fixed-point, continuity, or contraction APIs without an accepted
  source-to-target mapping.
- The untrusted catalog label `已验证` as evidence of human proof or kernel closure.

## Degenerate and boundary scope

The statement phase must decide empty and singleton domains, maps that are not self-maps, starting
points outside the invariant set, zero iterates, stationary initial points, multiple or absent
fixed points, convergence to a non-root when root/fixed-point equivalence fails, cycles or divergent
orbits, contraction factor zero or one, endpoint and derivative-bound equality, local versus global
basins, pseudometric zero without equality, infinite distances, and exact versus approximate
arithmetic. None is silently excluded at intake.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.Topology.MetricSpace.Contracting` contains
`ContractingWith.exists_fixedPoint`, `tendsto_iterate_fixedPoint`, and geometric error estimates;
`Mathlib.Dynamics.FixedPoints.Topology` contains `isFixedPt_of_tendsto_iterate`; and core iteration
syntax is available through `Function.iterate`. These declarations show plausible substrate and
materially different candidate conclusions. They do not identify the catalog target, and the
contraction candidate overlaps `THM-M-1444`. The API probe is therefore discovery evidence only,
not a statement gate, anchor audit, or proof.
