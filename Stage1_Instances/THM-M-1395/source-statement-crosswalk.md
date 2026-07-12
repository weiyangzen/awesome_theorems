# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10160-10165` supplies exactly the title `有限差分法`, an
attribution to many mathematicians, the twentieth century, the gloss `ODE的数值解法`, importance
`high`, and status `已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no equation, scheme, variables,
domain, mesh, hypotheses, conclusion, error norm, theorem/page locator, proof, or formal artifact.

`Docs/Stage0_Blueprint.md:37938-37963` projects the record as `THM-M-1395` while explicitly leaving
the exact definitions and premises, proof process, dependencies, equivalent forms, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The repository also contains a second `有限差分法` entry at
`Docs/researches/math_theorems.md:10693-10698`. Its gloss is `偏微分方程的差分离散`, and Stage0
assigns it to distinct target `THM-M-1465`. This is a same-name scope boundary, not a source alias.

## Inspected source-family lead

Randall J. LeVeque, *Finite Difference Methods for Ordinary and Partial Differential Equations:
Steady-State and Time-Dependent Problems*, SIAM (2007), ISBN 978-0-898716-29-0, was inspected via
the author's public companion page as a modern subject-family lead. Its contents separately list
finite-difference approximations, ODE initial-value problems, zero-stability and convergence,
absolute stability, stiff ODEs, and boundary-value problems. That separation supports the intake's
ambiguity classification.

The catalog does not cite this book, and no exact theorem passage from it is selected, preserved,
or independently reviewed. The lead supplies no H0 or canonical-statement credit.

## Component crosswalk

| Catalog/source component | Material choices still required | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `有限差分` / finite difference | derivative stencil, mesh, index range, endpoints, and step policy | `fwdDiff` plus source-specific grid and discrete operators | algebraic topic identified; numerical scheme open |
| `ODE` | initial/boundary problem, state space, vector field, data, solution notion, interval, and regularity | `IsIntegralCurveOn`, `IsIntegralCurveAt`, or a source-faithful solution predicate | adjacent API exists; exact problem open |
| `数值解法` / numerical method | recurrence or algebraic system, discrete solution, arithmetic model, and solvability | explicit scheme and discrete-solution definitions | completely absent from catalog |
| theorem conclusion | consistency, order, stability, convergence, solvability, or error estimate | exact proposition with norm, constants, limit, and ordered binders | no conclusion selected; hard statement blocker |
| many mathematicians / twentieth century | genealogy and edition | provenance after pinpoint source selection | discovery metadata only |
| `已验证` | claimed formal status | no proposition or proof object | explicitly untrusted; no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Algebra.Group.ForwardDiff` defines `fwdDiff h f x = f (x + h) - f x` and proves algebraic
Newton identities such as `fwdDiff_iter_eq_sum_shift` and `shift_eq_sum_fwdDiff_iter`.
`Mathlib.Analysis.ODE.Basic` defines `IsIntegralCurveOn`, `IsIntegralCurveAt`, and
`IsIntegralCurve`. `Mathlib.Analysis.Calculus.Taylor` supplies generic Taylor remainder theorems.
`IntakeProbe.lean` checks these names in the pinned environment.

These APIs are adjacent substrate only. The forward-difference file treats algebraic differences,
not a discrete ODE solver; the ODE predicates describe exact integral curves; and the Taylor result
does not select a stencil or establish stability and global convergence. A bounded lexical search
over repo-local Lean and pinned mathlib found no exact-topic declaration for a finite-difference
ODE scheme or its convergence theorem. This negative result is not the later immutable external
anchor audit and does not prove absence from all Lean projects.

## Required follow-up

Because the supplied method label is not a truth-valued proposition, `H5` blocks ordinary theorem-
proof execution until an accountable target decision is made. Before statement work, reviewers
must preserve one lawful complete source edition, select one exact numbered proposition or
explicitly sourced conjunction, include every incorporated definition, freeze its ordered binders,
hypotheses, mesh and scheme, conclusion and boundary cases, audit corrections and errata, resolve
the `THM-M-1465` boundary, and independently approve the crosswalk. Only then may the same exact
claim receive a canonical Lean expression, checked transports, fingerprints, and mutations.
