# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:10139-10144` is the repository source record. It gives the title,
George Green attribution, year 1828, Chinese gloss `边值问题的积分表示`, importance `高`, and status
`已验证`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37857-37882` projects that record as `THM-M-1392` and explicitly leaves
precise definitions, premises, proof, dependencies, equivalent forms, axioms, machine status, and
artifact links open. Neither document is a primary mathematical source, and the verified label
supplies no `H0` or machine-proof evidence.

## Inspected source lead

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society (2012), Section 5.4, pages 155-160, is an inspected
authoritative modern lead. It was obtained from the author's official page in the preliminary
edition made available with the publisher's permission; DOI `10.1090/gsm/140` independently
confirms the book metadata.

The source defines a regular Sturm--Liouville operator and separated boundary conditions in
equations (5.53)-(5.55), chooses boundary-adapted homogeneous solutions in (5.62), and, away from
zeros of their Wronskian, defines an integral resolvent and piecewise Green function in
(5.64)-(5.65). Equations (5.67)-(5.69) state the two inverse identities. The current official
errata has corrections in the surrounding chapter, including pages 154-156, but none indexed to
pages 157-160 or formulas (5.64)-(5.69).

This lead demonstrates a coherent member of the catalog family and exposes the missing choices. It
is not adopted as the canonical root: the catalog neither cites it nor says that its general Robin,
weighted Sturm--Liouville resolvent statement, one formula, or both inverse identities are intended.
No exact edition-to-catalog genealogy, complete proof audit, translation review, or independent
review has been accepted. The lead therefore supplies discovery context only, not `H0`.

## Claim crosswalk

| Catalog component | Information constrained | Source/Lean decision still required | Intake assessment |
|---|---|---|---|
| `Green函数` | a Green-function construction family | exact kernel definition, operator, normalization, and diagonal convention | family identified; proposition open |
| `边值问题` | endpoint or boundary data participates | interval/domain, boundary functionals, compatibility, and solution class | ODE category narrows context; all formal data open |
| `积分表示` | a solution or inverse is represented by an integral | integrand, measure/weight, equality notion, one or both inverse directions | intended role identified; exact identity open |
| George Green / 1828 | historical-attribution metadata | primary edition, genealogy to the selected modern theorem, and review | unverified lead only |
| `已验证` | claimed catalog status | inspectable human source and kernel receipts | explicitly untrusted |

## Candidate-source-to-formal map not credited

| Teschl component | Prospective formal surface | Missing before statement credit |
|---|---|---|
| regular Sturm--Liouville operator and weighted Hilbert space | coefficient, differential-operator, interval, measure, and function-space definitions | APIs, domains, regularity, positivity, and operator identity |
| separated boundary conditions | endpoint evaluations and linear boundary functionals | differentiability, trace/evaluation, and exact boundary encoding |
| adapted solutions and nonzero Wronskian | ODE integral-curve/derivative interfaces and a determinant-like Wronskian | source-faithful construction, normalization, and nonresonance proof |
| piecewise kernel (5.65) | conditional kernel on the two endpoint orders | diagonal convention, integrability, continuity, and derivative jump |
| resolvent integral (5.64) | Bochner or scalar interval integral with weight | measurability/integrability and equality convention |
| inverse identities (5.67)-(5.69) | exact left/right inverse propositions | operator domain/codomain, composition, boundary preservation, and checked proof |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.ODE.Basic` exposes `IsIntegralCurveOn`, `IsIntegralCurveAt`, and
`IsIntegralCurve`. `Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus` exposes
`intervalIntegral.integral_eq_sub_of_hasDerivAt`. `IntakeProbe.lean` authenticates these names and
types in the pinned environment.

The fundamental-theorem-of-calculus result is merely adjacent infrastructure: it integrates a
derivative to an endpoint difference and does not define a boundary-value operator, Green kernel,
or solution representation. A bounded repository and pinned-mathlib search found no exact
Green-function boundary-value declaration. That bounded result is not an exhaustive downstream
anchor audit and does not establish absence from external Lean projects.

Before `H0`, an independent reviewer must approve an immutable source, exact theorem and definition
chain, every assumption and conclusion, proof boundary, historical mapping, corrections and errata,
and a row-by-row source-to-Lean crosswalk. Before statement credit, the selected proposition must be
elaborated and fingerprinted with checked transports and all required mutation classes.
