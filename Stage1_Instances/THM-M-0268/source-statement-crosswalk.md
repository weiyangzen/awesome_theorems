# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1929-1934` records the Chinese title
`勒贝格控制收敛定理`, Henri Lebesgue, 1902, the gloss `积分与极限交换的条件`, importance
"high," and status `已验证`. Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, domain, binder,
hypothesis, theorem/page, proof passage, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7414-7439` repeats the gloss while explicitly leaving precise definitions
and premises, proof history, dependencies, equivalent forms, axioms, machine state, and artifact
links open. Its generic theorem-tree language is planning metadata. The rev-5.6 manifest retains
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Human-source discovery

Crossref DOI `10.1007/BF02420592` identifies H. Lebesgue, *Intégrale, Longueur, Aire*, pages
231-359, published in December 1902. This matches the catalog's author and year and is a plausible
primary-source lead for the underlying Lebesgue integration theory. Only bibliographic metadata was
inspected: no exact dominated-convergence proposition, incorporated definitions, premise map,
proof passage, translation, or correction record was obtained. The lead therefore helps support
provisional `H1`; it is not an H0 source record and does not select the canonical claim.

## Literal crosswalk

| Repository element | Candidate mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `控制收敛` | one integrable function dominates a convergent function sequence | exact domination predicate and integrability premise | title-level inference only; open |
| `积分与极限交换` | convergence of integrals to the integral of the pointwise limit | exact integral, filter, topology, and conclusion | open |
| functions and limit | real, complex, normed-space, or `ENNReal` functions | carrier, codomain, universes, measurability and convergence | open |
| conditions | measurable sequence, a.e. convergence, uniform integrable dominator | complete ordered hypothesis list and boundary cases | open |
| Henri Lebesgue, 1902 | historical source provenance | admitted edition, exact locator, translation and errata map | bibliographic lead only |
| `已验证` | untrusted inventory label | accepted human and kernel receipts | no credit |

## Formal-candidate crosswalk

All declarations below are from pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `IntakeProbe.lean` checks their interfaces and
representative axiom reports only; it does not inspect or credit root identity or terminal bodies.

| Declaration | Candidate role | Why it is not selected |
|---|---|---|
| `MeasureTheory.tendsto_integral_of_dominated_convergence` | natural-number Bochner-integral DCT for real normed-space-valued functions | strong exact-topic candidate, but the catalog does not select its codomain, a.e. conventions, or conclusion bundle |
| `MeasureTheory.tendsto_integral_filter_of_dominated_convergence` | countably generated filter generalization | materially broader index/filter encoding than the conventional sequence form |
| `MeasureTheory.tendsto_lintegral_of_dominated_convergence` | measurable nonnegative `ENNReal` sequence DCT | different integral, order domination, and codomain |
| `MeasureTheory.tendsto_lintegral_of_dominated_convergence'` | almost-everywhere-measurable nonnegative variant | variant-specific measurability choice is absent from the catalog |
| `MeasureTheory.tendsto_lintegral_filter_of_dominated_convergence` | nonnegative filter generalization | combines both filter and `lintegral` alternatives |
| `MeasureTheory.hasFiniteIntegral_of_dominated_convergence` | integrability of the pointwise limit | companion conclusion only, not integral convergence by itself |
| `MeasureTheory.tendsto_lintegral_norm_of_dominated_convergence` | convergence of the `L1` norm difference | stronger companion route, not the literal exchange-of-integral-and-limit conclusion |

The pinned Bochner file itself calls its first declaration the Lebesgue dominated convergence
theorem. That documentation and a successful interface check establish a credible exact-topic
formal candidate, hence provisional `M3`; they do not establish source-statement identity or M0.

## Open gates

Before H0, reviewers must admit an immutable primary proof source, pinpoint the exact result and
incorporated definitions, map every premise, conclusion, and proof transition, audit translation
and corrections, and independently approve the mapping. Before statement acceptance, Lean work
must freeze exact binders and minimal imports, serialize an elaborated expression and environment
fingerprint, compile each credited alternate-form transport, and pass required mutations. Formal
proof-body provenance, trust inspection, and exhaustive candidate search belong to the later
anchor-audit phase.
