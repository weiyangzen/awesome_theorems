# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1339`, the title "continuous dependence of solutions on
initial values", the broader gloss "continuity with respect to initial values and parameters", a
twentieth-century date, and attribution to many mathematicians. Intake preserves the ordinary
differential-equation solution-dependence family and the title/gloss mismatch. It does not turn the
catalog's untrusted status into source or kernel evidence.

## Proposition-changing decisions

An approved source selection must freeze:

- whether the equation is autonomous or time-dependent and scalar, finite-dimensional, or Banach
  space valued;
- the time domain, state domain, parameter domain, their topologies or norms, and the neighborhood
  on which every compared solution exists;
- the solution model: classical derivative, derivative within an interval, integral equation,
  local flow, maximal solution, or another source-defined notion;
- the exact continuity, local-Lipschitz, uniform-Lipschitz, boundedness, measurability, and
  completeness hypotheses that ensure existence and uniqueness;
- whether the inputs allowed to vary are initial state, initial time, vector field, an explicit
  parameter in the vector field, or a specified combination;
- whether the conclusion is epsilon-delta continuity, joint continuity, local Lipschitz
  continuity, uniform convergence on compact time intervals, or a quantitative Gronwall bound;
- whether parameter dependence requires only continuity or the stronger differentiability used by
  a neighboring theorem family; and
- all universes, ordered binders, quantifier dependencies, coercions, constants, and boundary cases.

These choices produce inequivalent propositions. They are a resolution ledger, not a canonical
statement.

## Candidate families not credited

1. A stability estimate for solutions `x` and `y` of `x' = f(t,x)` and `y' = g(t,y)`, bounding
   their distance by the initial displacement and a bound on `f - g`.
2. A local solution map `(t,s,x) -> phi(t,s,x)` that is continuous or locally Lipschitz in time,
   initial time, and initial state for a fixed locally Lipschitz vector field.
3. A parameterized local solution map `(t,s,x,lambda) -> phi(t,s,x,lambda)` that is continuous, or
   more strongly differentiable, when `f(t,x,lambda)` has source-specified regularity.
4. The pinned mathlib local flow under `IsPicardLindelof`, Lipschitz in the initial point and jointly
   continuous on a closed ball times a closed time interval.

No family in this list is selected, asserted, or credited at intake.

## Explicit exclusions

- Picard-Lindelof existence/uniqueness alone, without a solution-dependence conclusion.
- Dependence only on initial state as an automatic substitute for the catalog's parameter clause.
- Encoding an external parameter as a constant state coordinate without a checked source
  crosswalk; this changes the state space and imports additional norm and Lipschitz hypotheses.
- Differentiability with respect to parameters or the variational equation as a substitute for
  continuity; those overlap `THM-M-1340` and `THM-M-1341`.
- Global or maximal-flow continuity when the source only guarantees a common local interval.
- A theorem under nonunique Peano hypotheses without a source-defined set-valued solution notion.
- A structure containing continuity as assumed data, a projection from that structure, or the
  catalog label `已验证` as proof evidence.

## Boundary cases

The statement phase must decide zero-length time intervals, radius-zero initial balls, empty or
singleton parameter sets, zero Lipschitz and vector-field bounds, parameters that do not affect the
field, solutions approaching the domain boundary or a finite escape time, nonunique solutions,
disconnected domains, endpoint derivative conventions, and whether the common comparison domain
may shrink with initial data or parameters.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`IsPicardLindelof.exists_forall_mem_closedBall_eq_hasDerivWithinAt_lipschitzOnWith` and
`IsPicardLindelof.exists_forall_mem_closedBall_eq_hasDerivWithinAt_continuousOn` are credible
initial-state candidates. They use a fixed time-dependent vector field and do not express the
catalog's external-parameter clause. The API probe and bounded source search are discovery inputs,
not the later exhaustive anchor audit or an exact theorem proof.
