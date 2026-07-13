# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1850-1855` supplies exactly the title `阿尔福斯-贝尔斯定理`,
Lars Ahlfors and Lipman Bers, 1960, the gloss `泰希米勒空间的复结构`, importance `高`, and status
`已验证`. All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. This proves repository provenance, not source
fidelity. The record gives no edition, theorem locator, definitions, quantifiers, assumptions,
conclusion, proof boundary, corrections, or formal artifact.

`Docs/Stage0_Blueprint.md:7112-7137` repeats the gloss while explicitly leaving the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic planning language gives no rev-5.6
credit. The manifest retains `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Literal crosswalk

| Catalog component | Possible mathematical component | Prospective Lean surface | Intake result |
|---|---|---|---|
| Ahlfors-Bers | joint variable-metric theorem, normalized Beltrami solution, or analytic-dependence result | exact coefficient, solution, normalization, and dependence proposition | theorem-name usage is not unique |
| Teichmuller space | marked finite-type, universal, or another source-defined space | quotient or structure with fixed marking/equivalence data | carrier and quotient model absent |
| complex structure | compatible charts, a complex manifold, a Banach manifold, dimension, or holomorphic embedding | charted-space/manifold instances or an explicit existence proposition | conclusion and strength absent |
| Lars Ahlfors / Lipman Bers / 1960 | source identity, edition, exact locator, corrections | immutable source revision and node crosswalk | several same-era candidates fit only parts of the metadata |
| `已验证` | human proof or kernel evidence | reviewed source packet or exact declaration receipt | no credit |

The gloss cannot determine domains, surface type, marking, coefficient space, norm bound,
normalization, chart model, hypotheses, conclusion, quantifier order, or boundary cases.

## Primary and same-era source leads

Crossref metadata identifies Lars Ahlfors and Lipman Bers, *Riemann's Mapping Theorem for Variable
Metrics*, *Annals of Mathematics* (2) 72(2), 385-404 (1960), DOI `10.2307/1970141`. The author,
year, and joint attribution match strongly. The paper is a source-family lead, but no exact passage,
incorporated definitions, premise map, proof boundary, corrections, or independent review is
accepted here.

The literal complex-structure wording also matches Lars V. Ahlfors, *The Complex Analytic Structure
of the Space of Closed Riemann Surfaces*, pages 45-66 in *Analytic Functions* (1960), DOI
`10.1515/9781400876709-004`. Lipman Bers's *Spaces of Riemann surfaces as bounded domains*,
*Bulletin of the AMS* 66, 98-103 (1960), DOI `10.1090/S0002-9904-1960-10415-6`, has a bounded-domain
theorem for finite-type Teichmuller space and references both Ahlfors's complex-structure work and
the joint variable-metric paper. Bibliographic metadata and an extracted opening summary were
inspected, not admitted as a complete primary-text crosswalk. A published 1961 correction to the
Bers article has DOI `10.1090/S0002-9904-1961-10637-X`; Crossref records pages 465-467. A
publisher-extracted summary says the correction invalidates a lemma in the 1960 proof sketch while
retaining the theorem and pointing to a replacement route. The correction's primary text, exact
repair, and effect on any selected root remain unreviewed. These leads make the catalog identity
and exact root materially underdetermined. None is admitted as H0.

## Theorem-name ambiguity

Modern sources use "Ahlfors-Bers theorem" for at least two related formulations: existence and
uniqueness of the normalized quasiconformal solution for a Beltrami coefficient, and holomorphic
dependence of normalized solutions on a holomorphic parameter family. Passing from either result
to a complex structure on a selected Teichmuller quotient also requires definitions and
well-definedness, chart, and compatibility arguments. Intake therefore records these as candidate
readings rather than silently choosing one or treating them as equivalent.

## Pinned Lean boundary

Pinned mathlib exposes `AnalyticAt`, `ModelWithCorners`, `ChartedSpace`, `IsManifold`,
`MDifferentiable`, `Homeomorph`, conformal predicates, `conformalGroupoid`, orbit relations, and
quotients. The discovery-only probe re-elaborates those interfaces. They do not specify the
coefficient space, solve a Beltrami equation, build the marked-surface quotient, or prove its
complex structure.

A bounded case-insensitive search over repo-local Lean and pinned mathlib found no Ahlfors-Bers,
Teichmuller-space, quasiconformal, or Beltrami target declaration after excluding algebraic
Teichmuller lifts and the unrelated Teichmuller-Tukey theorem. This is feasibility evidence, not
an exhaustive immutable candidate audit or a proof of global absence.

## Retry condition

Accountable reviewers must select one lawful immutable proposition and reconcile the catalog
identity with its source. They must map the exact theorem and incorporated-definition locators,
assumptions, proof boundary, corrections and errata, and independently approve the choice. The
surface class, marking and quotient, coefficient and equality conventions, norm bound,
normalization, chart model, ordered binders, conclusion, and every boundary case must then be
frozen. A statement worker can subsequently elaborate exactly that claim with minimal pinned
imports and run removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations.

Until then no exact statement, H0, M0, R0, proof, audit completion, or theorem completion is
claimed.
