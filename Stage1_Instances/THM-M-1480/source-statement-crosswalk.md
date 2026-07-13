# THM-M-1480 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10798` through `:10803` supplies exactly the title
`拟Monte Carlo方法`, Harald Niederreiter, the year 1978, the gloss `低差异序列的积分`, importance
`high`, and status `已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, formula, definition,
domain, ordered binder, hypothesis, conclusion, proof, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:40243` through `:40268` repeats the gloss while explicitly leaving the
formal system, foundation, exact definitions and premises, proof route, dependencies, alternate
forms, axioms, machine status, and artifact links open. Its generic closed-result and leaf-audit
wording is planning metadata, not evidence. Rev-5.6 preserves `已验证` only as untrusted metadata
and resets the target to `L0 / rework_required`.

## Bibliographic lead

Crossref identifies Harald Niederreiter, *Quasi-Monte Carlo methods and pseudo-random numbers*,
*Bulletin of the American Mathematical Society* 84(6), 957-1041 (1978), DOI
`10.1090/S0002-9904-1978-14532-7`. Its author, year, and subject strongly match the catalog record.
The metadata describes an 85-page survey rather than selecting one theorem inside it.

The publisher landing/full-text route returned HTTP 403 during intake. Consequently no source
body, exact definition/theorem/section/page, incorporated assumptions, proof boundary, corrections,
or source-to-catalog mapping was inspected. The bibliographic match is `E5` discovery evidence,
not a primary-source proof crosswalk or `H0`. An accepted mapping requires preserved source bytes,
pinpoint locators, correction review, and independent mathematical review.

## Literal crosswalk

| Repository element | Possible mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| quasi-Monte Carlo method | deterministic equal- or weighted-sample quadrature | sample carrier, point map, weights, estimator | method family only |
| low-discrepancy sequence | sequence or finite prefix with a chosen discrepancy bound | domain, boxes, counting measure, exact discrepancy functional | no definition selected |
| integration | approximation of an integral by sample values | integral notion, integrand, finite sum, error norm | domain and estimator absent |
| Harald Niederreiter / 1978 | likely survey provenance | immutable source edition and pinpoint proposition | strong bibliographic lead, not admitted theorem |
| `已验证` | untrusted screening label | accepted source or kernel receipt would be required | no H or M credit |

The gloss cannot determine whether the root is a finite error inequality, asymptotic convergence,
a rate after a discrepancy construction, or another result. Nor does it determine the dimension,
unit-cube convention, discrepancy type, variation or regularity class, integration semantics,
normalization, constants, or boundary cases.

## Non-substitution boundary

The Koksma-Hlawka inequality is a prominent candidate because it connects star discrepancy and
Hardy-Krause variation to integration error. It is not selected here: the repository never names
that inequality, its discrepancy convention, its function class, or its finite-point-set form.
Likewise, replacing the target with generic equidistribution convergence, one-dimensional Riemann
sums, a discrepancy rate for one construction, or a randomized QMC estimate would add
proposition-changing mathematics.

The neighboring `THM-M-1479` Monte Carlo target cannot donate a law-of-large-numbers, variance, or
sampling result. QMC's deterministic discrepancy boundary and Monte Carlo's stochastic error
boundary are materially different even when both approximate the same integral.

## Pinned formal boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, adjacent APIs cover integral
averages, countable sums of weighted Dirac measures, uniform distributions, and tagged box-integral
sums. `IntakeProbe.lean` checks seven representative declarations and selected axiom reports.

Bounded searches over repo-local Lean and pinned mathlib found no declaration or definition matching
`quasi-Monte Carlo`, `low discrepancy`, `star discrepancy`, `Koksma-Hlawka`, or an equidistributed
sequence integration theorem. Generic uses of the words `variation`, `uniform`, or `discrepancy`
were unrelated or incomplete. The probe and searches are feasibility/discovery evidence only; they
do not select the canonical claim or close any proof obligation.

## Source exit gate

Before leaving `H5`, accountable reviewers must redirect the catalog family label to one immutable,
truth-valued proposition; preserve and inspect the exact primary or authoritative edition; identify
every incorporated definition and pinpoint theorem/proof passage; settle discrepancy, variation,
domain, sequence/point-set, estimator, constants, rates, binders, and boundary cases; audit
corrections; reconcile neighbor ownership; and independently approve the crosswalk.

Only then may the statement phase select minimal imports, elaborate and serialize the identical Lean
expression and environment fingerprint, compile checked transports, and mutation-test a removed
hypothesis, changed domain, changed binder scope, and boundary case. Until then no exact statement,
H0, M0, R0, proof, audit completion, or theorem completion is claimed.
