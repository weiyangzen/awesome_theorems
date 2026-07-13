# Source-statement crosswalk

## Repository source record

The repository record is `Docs/researches/math_theorems.md:4678-4683`, introduced in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`:

| Catalog field | Received value | Intake consequence |
|---|---|---|
| title | `贝尔纲定理` | Identifies the Baire category theorem family, not one formal proposition. |
| attribution | Rene Baire | Historical metadata; no work or theorem locator is cited. |
| time | 1899 | Consistent with a primary bibliographic lead, but not an exact statement. |
| statement | `完备度量空间是第二纲集` | Fixes a complete-metric/category theme but not the category convention, empty-space boundary, or formal domain. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; gives no H or M credit. |

`Docs/Stage0_Blueprint.md:17260-17285` repeats the claim and explicitly leaves the formal system,
precise definitions and premises, proof route, dependencies, alternate formulations, axioms,
machine status, and artifact links pending. It does not resolve the proposition.

## Primary bibliographic lead, not credited as H0

A bounded intake search identified Rene Baire, *Sur les fonctions de variables reelles*,
*Annali di Matematica Pura ed Applicata*, series III, volume 3, pages 1-123 (1899), DOI
`10.1007/BF02419243`. Crossref supplies this immutable bibliographic identity, and the Springer
landing page identifies the article and exposes an abstract-like closing passage. The advertised
PDF endpoint returned HTML rather than a primary scan in this run.

No exact theorem/section/page containing the category result was retrieved, transcribed, translated,
mapped to modern terminology, checked for corrections or errata, or independently reviewed. This
lead is therefore discovery evidence only. It does not establish that the catalog intends this
particular formulation and cannot support H0.

## Clause crosswalk

| Catalog component | Required mathematical decision | Pinned Lean surface | Intake result |
|---|---|---|---|
| complete metric space | displayed metric and completeness versus existence of a compatible complete metric; metric versus pseudometric | `CompleteSpace`, `MetricSpace`, `PseudoMetricSpace`, `TopologicalSpace.IsCompletelyMetrizableSpace`, `TopologicalSpace.IsCompletelyPseudoMetrizableSpace` | domain and separation convention unresolved |
| Baire category property | countable intersections of dense open sets are dense | `BaireSpace`, `BaireSpace.baire_property`, `dense_iInter_of_isOpen_nat` | strong standard candidate; not yet source-selected |
| second category | whole space is nonmeagre | `not_isMeagre_of_isOpen` specialized to `Set.univ` | requires nonemptiness; not identical to the stronger property without a reviewed relationship |
| meagre | countable union of nowhere-dense sets or residual-complement encoding | `IsMeagre`, `isMeagre_iff_countable_union_isNowhereDense` | candidate encoding; source convention unresolved |
| complete-to-category bridge | the first Baire theorem | `BaireSpace.of_completelyPseudoMetrizable` | exact-topic pinned candidate; no canonical target or proof credit at intake |
| `已验证` | inventory status | source and kernel receipts would be required | no evidence credit |

The empty-space discriminator is material. Mathlib proves `IsMeagre.empty`; for an empty type,
`Set.univ` is empty, so literal whole-space nonmeagreness fails. By contrast, the
`BaireSpace` intersection property holds vacuously and the completely pseudometrizable instance has
no nonemptiness premise. An exact source statement must decide this rather than letting a convenient
formal candidate broaden or repair the catalog wording.

## Formal-source boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.Topology.Baire.CompleteMetrizable` provides
  `BaireSpace.of_completelyPseudoMetrizable` with type
  `[TopologicalSpace X] [TopologicalSpace.IsCompletelyPseudoMetrizableSpace X] -> BaireSpace X`;
- `Mathlib.Topology.Defs.Basic` defines `BaireSpace` by density of natural-number-indexed
  intersections of open dense sets;
- `Mathlib.Topology.Baire.Lemmas` exposes the definition through
  `dense_iInter_of_isOpen_nat` and derives `not_isMeagre_of_isOpen` for nonempty open sets;
- `Mathlib.Topology.GDelta.Basic` defines `IsMeagre`, gives its nowhere-dense union
  characterization, and records the empty-set and second-category boundaries.

The intake probe elaborates these interfaces and reports the candidate bridge's axiom set. This is
a bounded exact-topic inspection, not the dependency-ordered anchor audit. It does not freeze a
discovery denominator, select a source-identical expression, resolve terminal proof provenance, or
confer statement or proof credit.

## Source gate

Before leaving H1, accountable reviewers must lawfully preserve an immutable primary or
authoritative source, identify the exact theorem and incorporated definitions, map every domain,
binder, completeness and separation premise, category convention, conclusion, and boundary case,
audit translations/corrections/errata, and independently approve fidelity to `THM-M-0631`.

Only then may the statement phase choose minimal imports, freeze an elaborated expression and
environment fingerprint, check transports among the Baire-space and nonmeagreness formulations,
and run removed-hypothesis, changed-domain, binder-scope, and empty-space mutations.
