# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2055-2060` records the Chinese title `叶戈罗夫定理`, Dmitri
Egorov, 1911, the gloss `几乎处处收敛与一致收敛的关系`, importance "high," and status
`已验证`. Git blame places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, quantifier, domain,
codomain, measure, finiteness or measurability premise, exceptional-set convention, theorem/page,
proof, translation, correction record, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7900-7925` repeats the gloss while explicitly leaving precise definitions
and premises, proof history, dependencies, equivalent forms, axioms, machine state, and artifact
links open. Its generic theorem-tree language is planning metadata. The rev-5.6 manifest retains
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Human-source discovery

Encyclopedia of Mathematics revision 28515 (2012-10-18) identifies D. F. Egorov, *Sur les suites
de fonctions mesurables*, *C. R. Acad. Sci. Paris* 152 (1911), pages 244-246. Its modern statement
uses a sigma-additive measure, a measurable finite-measure set, real-valued measurable functions,
almost-everywhere convergence, and a retained measurable subset whose discarded complement has
measure strictly below epsilon. It also says the finite-measure premise cannot generally be
dropped and that Egorov's original case concerned Lebesgue measure on the line.

The immutable API response was 4,686 bytes with SHA-256
`220e5c0ae02eba5c3c6911b89ac47503fcfd74f66b4fbf7f010880fb24799c2d`. It is a secondary
source and its generalized statement is not a transcription of the 1911 note. A BnF catalog
response for journal record `ark:/12148/cb343481087` corroborated the journal and institutional
digitization lead; the observed 102,129-byte response had SHA-256
`b2893ea88be0bc4daf458d4280af84bd09377c62cc5479135ed387644b351faa`.

The actual primary pages 244-246 were not retrieved. No reviewed French transcription,
incorporated definitions, exact assumption map, proof boundary, translation, corrections or
errata audit, or independent review is admitted. This supports provisional `H1`, not `H0`, and the
modern secondary formulation cannot silently replace the narrower original line/Lebesgue result.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `几乎处处收敛` | pointwise convergence outside a null set, globally or on a subset | measure, working set, filter, limit and exact `ae` predicate | open |
| `一致收敛` | uniform convergence after discarding a small set | retained/exceptional set and exact uniform-convergence predicate | open |
| relationship | the Egorov implication, a converse, equivalence, or explanatory gloss | exact conclusion and direction | open |
| functions | real-, metric-, or extended-metric-valued measurable functions | universes, domain/codomain structures and measurability notion | open |
| 1911 / Dmitri Egorov | historical provenance | admitted edition, theorem locator, translation and attribution map | open |
| `已验证` | untrusted inventory label | accepted human and kernel receipts | no credit |

## Formal-candidate crosswalk

All declarations below are from pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `IntakeProbe.lean` checks their interfaces and
axiom reports only; it does not establish source identity or credit a root.

| Declaration | Candidate role | Why it is not selected |
|---|---|---|
| `tendstoUniformlyOn_of_ae_tendsto_of_measurable_edist` | finite measurable subset; measurable distances | catalog omits every domain, finiteness and measurability choice |
| `tendstoUniformlyOn_of_ae_tendsto` | same subset result from strong measurability | strong measurability of sequence and limit is not supplied by the catalog |
| `tendstoUniformlyOn_of_ae_tendsto_of_measurable_edist'` | globally finite measure; measurable distances | global finiteness and complement form may specialize or repackage the intended result |
| `tendstoUniformlyOn_of_ae_tendsto'` | globally finite measure; strong measurability | combines both proposition-changing choices |

The module header states the familiar theorem informally and mathlib's `docs/1000.yaml` maps
Wikidata Q1191709 to `MeasureTheory.tendstoUniformlyOn_of_ae_tendsto`. Those are useful discovery
metadata, not a source-to-Lean identity certificate.

## Open gates

Before H0, reviewers must admit an immutable primary proof source, pinpoint the exact result and
incorporated definitions, map all premises, conclusion, exceptional-set conventions and proof
transitions, audit translation and corrections, and independently approve the mapping. Before
statement acceptance, Lean work must freeze exact binders and minimal imports, serialize an
elaborated expression and environment fingerprint, compile alternate-form transports, and pass
all required mutations. Formal terminal-body provenance and trust inspection belong to the later
anchor-audit phase.
