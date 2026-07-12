# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1399`, the label `向后微分公式` (backward differentiation
formula), the gloss `刚性方程的数值方法` (a numerical method for stiff equations), a collective
twentieth-century attribution, and an untrusted `已验证` status. Intake preserves this numerical-ODE
method-family boundary. It does not turn the name into a proposition or select a formula or theorem
without source authority.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- whether the root is a method definition, recurrence identity, interpolation/coefficient theorem,
  consistency or order theorem, zero-stability or convergence theorem, absolute/A/L-stability
  result, or existence and uniqueness theorem for the implicit update;
- the BDF order, admissible order range, coefficient normalization, sign and index direction, and
  whether the derivative is evaluated at the newest or another grid point;
- constant or variable steps, the time grid, positive-step and step-ratio assumptions, and the
  precise relation between interpolation nodes and solution samples;
- scalar, finite-dimensional, or Banach-space state; autonomous or nonautonomous ODE; real or
  complex scalars; and the regularity, Lipschitz, stiffness, and initial-value assumptions;
- exact versus approximate starting values, number of starting values, recurrence start index,
  finite or infinite horizon, and the norm and mode of convergence;
- the nonlinear or linear implicit solve, existence and uniqueness of each new value, solver
  tolerance, and whether an algorithmic root finder is part of the claim; and
- one truth-valued conclusion with ordered binders, all constants and dependencies, and all
  exceptional and boundary cases.

These choices define inequivalent propositions. They are a resolution ledger, not a canonical
claim.

The literal gloss also lacks a quantifier and a mathematical predicate. It does not say that BDF
exists, is consistent, converges, is stable, or performs better on stiff equations. A definitional
reading needs an exact formula and convention; a performance reading needs a metric and comparison
class. Intake cannot silently rewrite the gloss as either one.

## Candidate families not credited

- A fixed-step `k`-step implicit recurrence with source-selected coefficients.
- The construction obtained by differentiating the polynomial interpolating recent solution
  values at the newest time node.
- The BDF1/backward-Euler or BDF2 special case.
- A consistency, local-truncation-error, order, zero-stability, convergence, A-stability, or
  stability-region theorem for a specified range of orders.
- A variable-step algorithm with step-ratio restrictions or an existence/uniqueness theorem for
  its implicit update.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor boundaries and exclusions

- `THM-M-1395` finite differences, `THM-M-1396` Runge-Kutta methods, `THM-M-1397` Adams methods,
  and `THM-M-1398` stiff equations remain separate scheduled targets. Their statements and future
  evidence cannot replace or close this BDF target.
- Backward Euler is only one possible first-order BDF specialization; proving a fact about it does
  not establish an unidentified general BDF claim.
- A backward finite-difference derivative formula without an ODE update, or an arbitrary implicit
  multistep scheme, cannot be treated as the scheduled target merely because terminology overlaps.
- A numerical table, floating-point experiment, stability plot, solver run, or benchmark on a
  stiff test equation is not a kernel-checked proof of a source-selected theorem.
- A structure field or hypothesis that directly assumes the desired recurrence, convergence, or
  stability supplies an interface, not a proof.
- Generic derivative, interpolation, ODE, and existence APIs receive no target statement or proof
  credit.
- The catalog label `已验证` supplies neither a human proof nor a machine artifact.

## Boundary cases

The statement phase must decide order zero and order one; empty histories and insufficient starting
values; zero, negative, repeated, or nonmonotone time steps; coincident interpolation nodes;
constant and zero vector fields; nonunique or nonexistent implicit updates; singular leading
coefficients; exact solutions of insufficient regularity; inconsistent starting data; variable
step-ratio extremes; finite versus infinite horizons; scalar versus vector states; and the precise
treatment of truncation, rounding, and nonlinear-solver errors.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks generic derivative,
integral-curve, Picard-Lindelof, and Lagrange-interpolation interfaces. A bounded exact-topic search
found no backward-differentiation, BDF-method, linear-multistep, or stiff-equation occurrence in
pinned mathlib or repo-local Lean sources. This is an intake discovery observation, not an
exhaustive anchor audit or a global absence claim.
