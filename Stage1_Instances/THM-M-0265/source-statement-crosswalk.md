# THM-M-0265 source-statement crosswalk

## Repository record

The source inventory at `Docs/researches/math_theorems.md:1908-1913` contains exactly:

- title: `魏尔斯特拉斯逼近定理` (Weierstrass approximation theorem);
- proposer: Karl Weierstrass;
- time: 1885;
- statement gloss: `连续函数可用多项式一致逼近` (continuous functions can be uniformly
  approximated by polynomials);
- importance: high; and
- formalization status: `已验证` (verified).

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no primary source, edition, theorem or
page locator, formula, definition chain, ordered binders, assumptions, conclusion, proof boundary,
errata, reviewer, or machine artifact. The Stage0 projection repeats the gloss while explicitly
leaving the missing components open. Under rev-5.6, the verified label is untrusted metadata.

## Literal crosswalk

| Repository phrase | Material ambiguity | Required source component | Intake status |
|---|---|---|---|
| `连续函数` | function domain, codomain, and continuity-on-set encoding | exact domain/scalars/function carrier/continuity premise | open |
| `多项式` | coefficient field, carrier, evaluation, degree constraints | polynomial type and evaluation map | open |
| `一致逼近` | density, closure, epsilon inequality, or convergent sequence | topology/norm and exact quantifier/conclusion | open |
| Karl Weierstrass / 1885 | historical attribution without a work or edition | stable source ID, edition, theorem/page, definitions, proof | open |
| `已验证` | inventory label only | no human or machine proof component | explicitly untrusted |

The rows do not determine one canonical statement. Therefore the intake leaves the human claim and
Lean expression null instead of inventing a source formula.

## Human-source lead and primary-source status

The repository cites no primary source. A bounded Crossref lookup of DOI
`10.1017/CBO9781139567886.002` returned an authoritative Cambridge University Press edition record
for Karl Weierstrass, *Über die analytische Darstellbarkeit sogenannter willkürlicher Functionen
reeller Argumente*, in *Mathematische Werke*, pages 1-38, issued 2013-04-18, ISBNs
9781108059152 and 9781139567886. The 1,881-byte JSON response observed on 2026-07-13 had SHA-256
`fe4fc307bfb6cc1959ca1cf5523034818843759aba077fe097490351c4bee44b`.

That metadata supplies a stable named source lead, not E4 or H0: this intake did not retrieve or
inspect the chapter text, determine its relationship to the 1885 parts, locate the exact theorem or
incorporated definitions, map its assumptions and proof, audit corrections or errata, or obtain an
independent review. The provisional status is therefore `H1`, with explicit source-reconstruction
debt rather than human proof credit.

## Pinned formal candidates, not root identity

The bounded intake inspection used mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The following interfaces all elaborate from
`Mathlib.Topology.ContinuousMap.Weierstrass`:

| Declaration | Candidate meaning | Unresolved relationship |
|---|---|---|
| `polynomialFunctions_closure_eq_top'` | polynomial functions are dense on `[0,1]` | source may intend another interval/form |
| `polynomialFunctions_closure_eq_top` | density on every real `[a,b]`, including degenerate orientation | density equality is not literally in catalog |
| `continuousMap_mem_polynomialFunctions_closure` | every bundled continuous map lies in polynomial closure | requires bundled subtype transport |
| `exists_polynomial_near_continuousMap` | positive-epsilon supremum-norm approximation | norm form and binders are source choices |
| `exists_polynomial_near_of_continuousOn` | total real function continuous on `[a,b]` has pointwise uniform epsilon approximation | most literal candidate, but adds unstated real interval, continuity, epsilon, and evaluation clauses |

`IntakeProbe.lean` checks these interfaces and representative axiom reports in the pinned
environment. The module describes them as Weierstrass forms and derives them from Bernstein
approximation, but module documentation is not the missing primary-source crosswalk. No declaration
is designated as the canonical root and no proof body, wrapper, or M0 status is credited.

The broader `polynomialFunctions.topologicalClosure` result in the Stone-Weierstrass module is an
unselected candidate at intake: it changes the domain from a closed interval to an arbitrary
compact real set, its source relationship is unreviewed, and its general proof route overlaps the
separately cataloged `THM-M-0266`.

## Gate result

The intake freezes `[H1, M3, R4]`. Retry of the statement gate requires an independently reviewed,
immutable exact source proposition that resolves every scope row, followed by elaboration of that
same proposition with minimal imports, expression and environment fingerprints, checked alternate
transports, and the required mutations. Until then, the statement and every dependent phase remain
open.
