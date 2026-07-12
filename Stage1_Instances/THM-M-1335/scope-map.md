# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1335`, the label `解的延拓定理` (solution continuation
theorem), the gloss `解的最大存在区间` (the maximal interval of existence of a solution), the
attribution "many mathematicians," and the twentieth century. Importance "high" and status
`已验证` are catalog metadata, not theorem or proof evidence.

This identifies a classical ordinary-differential-equation family concerning how a local solution
is assembled or extended to a maximal time interval. It does not select an equation, hypotheses,
solution notion, maximality relation, endpoint theorem, or proof source.

## Proposition-changing decisions

An approved statement run must fix all of the following from an immutable source:

- whether the root is existence and uniqueness of a maximal solution, an extension criterion,
  compact continuation, escape from compacta, norm blow-up, or a global-existence corollary;
- an autonomous equation `x' = f x` or a time-dependent equation `x' = f t x`, including the
  exact open domain of the vector field and whether time is part of that domain;
- scalar, finite-dimensional real, normed-space, Banach-space, manifold, or another state space;
- continuity in time, local Lipschitz or differentiability in state, uniformity conventions, and
  whether unique local solvability is assumed abstractly or derived from concrete hypotheses;
- the curve representation, initial-value predicate, derivative within the time domain, and
  equality/restriction relation used to say that one solution extends another;
- whether solution domains are open connected intervals containing the initial time, subtypes,
  set-indexed partial maps, germs, or globally defined maps with a validity predicate;
- maximality under domain inclusion and agreement, endpoint supremum/infimum packaging, uniqueness
  of the maximal pair, and one-sided versus two-sided conclusions;
- the exact compactness or convergence condition at a finite endpoint, including whether the graph
  stays in the open spacetime domain; and
- every finite/infinite endpoint, boundary, trivial, equilibrium, nonunique, and already-global
  case, together with the full order and scope of quantifiers.

These choices produce inequivalent theorems. They are a resolution ledger, not a statement.

## Candidate branches not credited

An inspected modern source, Gerald Teschl's *Ordinary Differential Equations and Dynamical
Systems*, Section 2.6, makes the ambiguity concrete. It states separately:

- Theorem 2.13: unique maximal-solution existence on a maximal open interval, assuming unique local
  solvability;
- Lemma 2.14: extension beyond a finite endpoint iff a graph subsequence converges to a point in
  the open vector-field domain;
- Corollary 2.15: a compact recurrence condition implies extension;
- Corollary 2.16: a finite endpoint of a maximal solution forces escape from suitable compact sets,
  with norm divergence only in the whole finite-dimensional state space; and
- Theorem 2.17: a separate linear-growth hypothesis gives global existence.

The catalog does not cite this source or choose among these results. None is canonical or credited
at intake.

## Explicit exclusions

Local Picard-Lindelof existence and uniqueness alone, Peano existence under continuity, a fixed
compact-interval solution, a comparison theorem, and Gronwall's inequality are supporting results,
not substitutes for a maximal-solution or continuation root. A structure that assumes the desired
maximality, extension, compact escape, blow-up, or global existence as a field is also excluded.

A norm blow-up alternative cannot replace compact escape for a proper open domain, a nonproper or
infinite-dimensional state space, or absent compactness hypotheses. Global existence cannot be
inferred without an a priori bound or growth condition. Under mere continuity maximal solutions
need not be unique, so a uniqueness conclusion cannot be silently imported. The catalog's
`已验证` label supplies neither human-source nor Lean kernel credit.

## Boundary cases

The selected source must decide finite and infinite endpoints, an all-real maximal interval,
one-sided initial-value problems, a boundary initial time, zero vector fields and equilibria,
zero-dimensional states, nonunique local branches, solutions approaching the boundary of a proper
open domain with bounded norm, and how extension agreement is expressed outside the old domain.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides `IsIntegralCurveOn`,
`IsIntegralCurveAt`, local Picard-Lindelof existence on fixed intervals, and ODE uniqueness on open
intervals. The bounded intake search found no declaration encoding a maximal solution, maximal
existence interval, endpoint continuation criterion, or compact-escape alternative. The API probe
and search are feasibility evidence only, not an exhaustive anchor audit, exact target elaboration,
or proof evidence.
