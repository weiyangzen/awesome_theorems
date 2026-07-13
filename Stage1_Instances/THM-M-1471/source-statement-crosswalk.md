# THM-M-1471 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10735-10740` supplies exactly the title `先验误差估计`, an
attribution to many mathematicians, the twentieth century, the gloss `数值解的收敛阶`, importance
`high`, and status `已验证`. All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no problem, scheme, space,
parameter, norm, hypothesis, rate, theorem/page locator, proof, erratum record, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:40000-40025` projects the record as `THM-M-1471` while explicitly leaving
the exact definitions and premises, proof route, dependencies, alternate statements, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`. The target's score and
lane are scheduling metadata, not selection of a numerical theorem.

No primary or authoritative mathematical source has been admitted for this intake. In particular,
the catalog does not choose a Cea theorem, an interpolation estimate, a PDE discretization, an ODE
method, or a convergence-order definition. Named examples are discrimination aids only and supply
no `H0` credit.

## Literal crosswalk

| Repository component | Material choices still required | Prospective Lean surface | Intake result |
|---|---|---|---|
| `先验误差估计` | numerical problem, method, pre-computation information allowed, error quantity | exact problem, approximation, and error predicates | result-family label only |
| `数值解` / numerical solution | continuous and discrete objects, existence/uniqueness, data, scheme | typed exact and discrete solutions with a relation | unspecified |
| `收敛` / convergence | refinement parameter/filter, topology or norm, uniformity | `Tendsto`, eventual inequalities, or source-defined predicate | unspecified |
| `阶` / order | exponent, explicit constant, big-O/limit semantics, local or global error | exact inequality or `Asymptotics.IsBigO` expression | unspecified |
| many mathematicians / twentieth century | genealogy, edition, theorem/page, corrections | source provenance after proposition selection | catalog metadata only |
| `已验证` | claimed formal status | accepted source and kernel receipts | explicitly untrusted; no credit |

The gloss supplies no predicate, equation, inequality, binder, or rate. For example,
`error(h) = O(h^p)` is still ambiguous without the error family, norm, filter, exponent, method,
uniformity, and hypotheses. Every unresolved choice is proposition-changing.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.Asymptotics.Lemmas` exposes `Asymptotics.IsBigO`, `isBigO_iff`, and
`IsBigO.trans_tendsto`. These encode generic asymptotic bounds but select no numerical error.
`Mathlib.Analysis.InnerProductSpace.LaxMilgram` exposes coercive variational solvability, while
`Mathlib.Analysis.InnerProductSpace.Projection.Basic` proves
`Submodule.starProjection_minimal`. These are possible ingredients for one special theorem family,
not a source-statement match.

The discovery-only probe elaborated those interfaces in the pinned environment. A bounded
exact-topic search over pinned mathlib and tracked repo-local Lean found no source-identical a
priori numerical error theorem. This observation is not the later immutable external anchor audit,
not proof of global absence, and not target proof evidence.

## Source gate and retry condition

An accountable correction must preserve one lawful immutable source edition, select one exact
numbered proposition or explicitly sourced conjunction, incorporate every definition, and map its
problem, exact/discrete solutions, spaces or scheme, parameter/filter, binders, hypotheses,
conclusion, norm, exponent, constants, proof nodes, boundary cases, and errata. Independent
numerical-analysis and source reviewers must approve that crosswalk and the neighboring-target
boundaries. Only then may the statement phase freeze and mutation-test an exact Lean expression.
Until then the canonical mathematical and Lean targets remain null and the catalog target is
provisionally `H5`.
