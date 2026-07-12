# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1377`, the ODE-category label `变分法` (calculus of
variations), the gloss `泛函极值的必要条件` (necessary conditions for extrema of functionals), a
collective seventeenth-century attribution, and an untrusted `已验证` status. Intake preserves this
necessary-condition family boundary. It does not turn the gloss into a quantified proposition or
select a familiar theorem without source authority.

## Proposition-changing decisions

An approved source correction must freeze all of the following before statement elaboration:

- whether the functional acts on curves, functions, sections, measures, shapes, controls, or an
  abstract topological or normed space, including scalar field, codomain, universes, and topology;
- the admissible set, its ambient structure, and whether extrema are global, local, strict, weak,
  strong, interior, boundary, minimum, maximum, or either;
- differentiability and regularity notions, such as Frechet, Gateaux, directional, first variation,
  weak derivative, convex subdifferential, or a source-specific alternative;
- allowed variations, constraint qualifications, endpoint or boundary conditions, integral
  regularity, and any topology in which nearby admissible objects are compared;
- whether the conclusion is derivative zero, vanishing first variation, Euler-Lagrange equations,
  a natural boundary or transversality condition, a multiplier rule, or another condition;
- local versus almost-everywhere or weak conclusions, quantifier order, equality conventions,
  coordinate or chart choices, exceptional cases, and converse directions; and
- one theorem-bearing source with exact edition, theorem/section/page, assumptions, proof boundary,
  corrections, and an independently approved relationship to this repository target.

These choices define inequivalent propositions. They are a resolution ledger, not a canonical
claim. In particular, the word "functional" does not determine a normed-space Frechet derivative,
and "necessary conditions" is plural and does not select one conclusion.

## Candidate families not credited

- The abstract Fermat condition that the Frechet derivative of a real-valued functional at an
  unconstrained local extremum in a real normed space is zero.
- Vanishing first variation for every admissible endpoint-fixed variation of an integral
  functional.
- A classical Euler-Lagrange differential equation under source-specific smoothness and boundary
  hypotheses.
- Lagrange-multiplier, isoperimetric, natural-boundary, corner, or transversality conditions.
- Convex-analytic or nonsmooth conditions using subgradients or normal cones.
- A direct-method existence theorem or an application-specific PDE or mechanics theorem.

No family in this list is selected, conjoined, asserted, or credited at intake.

## Neighbor boundaries and exclusions

- `THM-M-1378` separately owns the Euler-Lagrange equation. Its future statement and proof cannot
  be silently adopted as this more ambiguous target.
- `THM-M-1381` Maupertuis' principle and `THM-M-1382` least action are mechanics principles, not
  interchangeable with an unspecified functional-extremum necessary condition.
- `THM-M-1264` variational methods for PDE, `THM-M-1265` the direct method, `THM-M-1266` Tonelli's
  theorem, and `THM-M-1267` through `THM-M-1269` lower-semicontinuity and minimizing-sequence
  targets remain distinct existence or analytic infrastructure families.
- `THM-M-1517` Lagrangian mechanics and `THM-M-1518` least action remain separate mathematical-
  physics targets. Their legacy files are discovery inputs only and have no proof credit here.
- A predicate, structure field, or hypothesis that directly assumes derivative vanishing,
  stationarity, or the desired Euler-Lagrange equation supplies an interface, not a proof.
- A finite-dimensional example, polynomial functional, numerical optimizer, symbolic variation,
  or plotted extremal cannot replace a source-selected general theorem.
- The catalog label `已验证`, generic calculus APIs, and an unrelated successful build supply no
  human or machine proof credit.

## Boundary cases

The statement phase must decide empty admissible classes; constant or nowhere-differentiable
functionals; isolated points and vacuous local extrema; zero-dimensional spaces; boundary versus
interior points; constrained versus unconstrained extrema; nonunique extrema; one-sided or weak
variations; degenerate intervals; fixed, free, or mixed endpoints; nonsmooth extremals; singular
Lagrangians; abnormal multipliers; null directions; equality almost everywhere versus pointwise;
and whether minima, maxima, or both are covered.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks generic local-extremum,
Frechet-derivative, and Fermat-condition interfaces. A bounded exact-topic search over pinned
mathlib found no terminal declaration documented as calculus of variations, first variation, or
Euler-Lagrange. Repo-local legacy files contain adjacent theorem-specific planning, but none is the
source-identical target. These are intake discovery observations, not an exhaustive anchor audit or
a global absence claim.
