# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10153-10158` supplies exactly the title `打靶法`, an attribution to
many mathematicians, the twentieth century, the gloss `边值问题的数值方法`, importance `high`, and
status `已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no equation, state space,
interval, boundary operator, shooting parameter, residual, algorithm, hypotheses, conclusion,
theorem/page locator, proof, or formal artifact.

`Docs/Stage0_Blueprint.md:37911-37936` projects the record as `THM-M-1394` while explicitly leaving
the exact definitions and premises, proof process, dependencies, equivalent forms, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected source-family leads

Crossref metadata identifies Paul B. Bailey and L. F. Shampine, "On shooting methods for two-point
boundary value problems," *Journal of Mathematical Analysis and Applications* 23(2), August 1968,
235-249, DOI `10.1016/0022-247X(68)90064-4`. It also identifies David D. Morrison, James D.
Riley, and John F. Zancanaro, "Multiple shooting method for two-point boundary value problems,"
*Communications of the ACM* 5(12), December 1962, 613-614, DOI `10.1145/355580.369128`.

These bibliographic records corroborate that single and multiple shooting are distinct historical
branches. The catalog cites neither work. The intake did not obtain and preserve a complete lawful
text, select an exact theorem passage, map incorporated definitions or assumptions, audit errata,
or obtain independent review. The records therefore supply family-discrimination evidence only,
not a canonical statement, H0 status, or proof credit.

## Component crosswalk

| Catalog/source component | Material choices still required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `边值问题` / boundary-value problem | ODE/system, interval, state, boundary operator/data, solution notion, existence domain | source-specific predicate built on exact trajectories | subject family identified; problem open |
| `打靶` / shooting | missing initial data, parameter space, IVP solution family, endpoint residual, single/multiple form | parameterized `IsIntegralCurveOn` family plus an explicit residual | method family identified; construction open |
| numerical method | root solver, IVP integrator, grid, arithmetic, tolerances, conditioning | source-specific iterates, discrete trajectories, and certificates | completely absent from catalog |
| theorem conclusion | equivalence, solvability, residual root, convergence, stability, or error | exact proposition with norms, constants, and ordered binders | no conclusion selected; hard statement blocker |
| many mathematicians / twentieth century | genealogy and edition | provenance after pinpoint source selection | discovery metadata only |
| `已验证` | claimed formal status | no proposition or proof object | explicitly untrusted; no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.ODE.Basic` defines `IsIntegralCurveOn`, `IsIntegralCurveAt`, and
`IsIntegralCurve`. `Mathlib.Analysis.ODE.PicardLindelof` exposes local initial-value existence, and
`Mathlib.Analysis.ODE.Gronwall` exposes uniqueness and approximate-trajectory bounds.
`Mathlib.Topology.Order.IntermediateValue` exposes `intermediate_value_Icc`.
`IntakeProbe.lean` checks these names in the pinned environment.

These APIs are adjacent substrate only. They do not define the catalog's boundary residual,
parameterized shot, multiple-shooting match equations, numerical root solver, or method-specific
convergence/error theorem. A bounded lexical search over repo-local Lean and pinned mathlib found no
named shooting-method declaration under the recorded terms. This negative result is not the later
immutable external anchor audit and does not prove absence from all Lean projects.

## Required follow-up

Because the supplied method label is not a truth-valued proposition, `H5` blocks ordinary theorem-
proof execution until an accountable target decision is made. Before statement work, reviewers
must preserve and hash one lawful immutable primary or authoritative source, select one exact
numbered proposition or explicitly sourced conjunction, include every incorporated definition,
freeze its binders, hypotheses, boundary problem, shooting construction, algorithm, conclusion,
and degenerate cases, audit corrections and errata, reconcile neighboring target ownership, and
independently approve the crosswalk. Only then may the same exact claim receive a canonical Lean
expression, checked transports, fingerprints, and mutations.
