# THM-M-1465 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10693-10698` supplies exactly the title `有限差分法`, an
attribution to many mathematicians, the twentieth century, the gloss `偏微分方程的差分离散`,
importance `high`, and status `已验证`. All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no PDE, domain, data, mesh,
stencil, hypothesis, conclusion, theorem/page locator, proof, erratum record, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:39838-39863` projects the record as `THM-M-1465` while explicitly leaving
the exact definitions and premises, proof route, dependencies, alternate statements, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

The repository also contains a distinct `有限差分法` entry at
`Docs/researches/math_theorems.md:10160-10165`. Its gloss is `ODE的数值解法`, and Stage0 assigns it
to `THM-M-1395`. It is a same-name ownership boundary, not a source alias.

## Inspected source-family lead

Randall J. LeVeque, *Finite Difference Methods for Ordinary and Partial Differential Equations:
Steady-State and Time-Dependent Problems*, SIAM, 2007, DOI `10.1137/1.9780898717839`, ISBN
978-0-898716-29-0, was inspected through Crossref metadata and the author's companion site. Its
table of contents separates finite-difference approximations, elliptic five-point and nine-point
Laplacians, parabolic method-of-lines and fully discrete analysis, hyperbolic schemes, stability,
convergence, von Neumann analysis, and CFL conditions. That separation confirms the catalog
wording is materially ambiguous.

The companion errata correct finite-difference boundary formulas and PDE scheme formulas, among
other items. Thus an eventual source gate must freeze the exact edition and applicable corrections.
The catalog does not cite this book, and no exact proposition, incorporated definition, proof
passage, or page has been selected, preserved as the root, or independently reviewed. It is a
source-family lead only and supplies no `H0` credit.

## Literal crosswalk

| Repository component | Material choices still required | Prospective Lean surface | Intake result |
|---|---|---|---|
| `偏微分方程` / PDE | equation/class, coefficients, dimension, domain, data, boundary/initial conditions, solution notion, regularity | exact continuous problem and solution predicates | unspecified |
| `差分` / difference | spatial/time mesh, stencil, boundary treatment, step restrictions, refinement | indexed grid and source-defined discrete operators | unspecified |
| `离散` / discretization | semidiscrete or fully discrete scheme, recurrence/algebraic system, discrete solution, arithmetic | scheme and discrete-solution definitions | unspecified |
| theorem conclusion | consistency, order, solvability, stability, convergence, error, or exact conjunction | exact proposition with norm, constants, limits, and ordered binders | absent; hard statement blocker |
| many mathematicians / twentieth century | genealogy, edition, result attribution | source provenance after theorem selection | catalog metadata only |
| `已验证` | claimed formal status | accepted source and kernel receipts | explicitly untrusted; no credit |

Every unresolved choice is proposition-changing. A consistent stencil need not be stable; a stable
scheme need not be selected for the catalog's PDE; and a finite residual computation cannot prove
convergence as the mesh tends to zero.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Algebra.Group.ForwardDiff` defines `fwdDiff h f x = f (x + h) - f x` and proves the
algebraic Newton identities `fwdDiff_iter_eq_sum_shift` and `shift_eq_sum_fwdDiff_iter`.
`Mathlib.Analysis.InnerProductSpace.Laplacian` defines the continuous Laplacian on finite-
dimensional real inner-product spaces and relates it to iterated derivatives.
`Mathlib.Analysis.Calculus.Taylor` supplies `exists_taylor_mean_remainder_bound` for smooth
one-dimensional functions.

These declarations are adjacent mathematical substrate, not a finite-difference PDE method. They
define no mesh, stencil, discrete PDE, stability relation, convergence limit, or error estimate for
a scheme. A bounded exact-topic search over pinned mathlib and tracked repo-local Lean found no
source-identical finite-difference PDE theorem. This observation is discovery only, not the later
immutable external anchor audit and not proof of global absence.

## Source gate and retry condition

An accountable correction must preserve one lawful immutable source edition, select one exact
numbered proposition or explicitly sourced conjunction, incorporate every definition, and map its
PDE, domain, data, solution regularity, grid, stencil, scheme, binders, hypotheses, conclusion,
norm, constants, proof nodes, boundary cases, and errata. Independent numerical-analysis and source
review must approve that crosswalk and the `THM-M-1395`/neighbor boundaries. Only then may the
statement phase freeze and mutation-test an exact Lean expression. Until then the canonical
mathematical and Lean targets remain null and the catalog target is provisionally `H5`.
