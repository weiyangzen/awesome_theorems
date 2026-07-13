# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4636-4641` supplies exactly the title `Bing度量化定理`, attribution
to R. H. Bing, year 1951, gloss `集态正规空间的可度量化`, high importance, and the untrusted status
`已验证`. `Docs/Stage0_Blueprint.md:17098-17118` repeats the gloss while leaving exact definitions,
hypotheses, equivalent forms, axioms, and machine artifacts open. These lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; they contain no bibliography or theorem locator.

## Inspected primary source

R. H. Bing, "Metrization of Topological Spaces", *Canadian Journal of Mathematics* **3** (1951),
175-186, DOI `10.4153/CJM-1951-022-3`. The Cambridge version-of-record PDF was inspected on
2026-07-13; its observed SHA-256 was
`cbd17aac867cd231618bdc8661d37e87a22205fb20897329cce33e05a432d7e6`.

Relevant pinpoints are:

- page 176: definitions of a discrete collection and collectionwise normality;
- page 176 footnote 6: a Moore space satisfies the first three parts of Moore's Axiom 1 and is a
  regular developable space;
- page 180: definition/discussion of a development;
- pages 182-183, Theorem 10: "A Moore space is metrizable if it is collectionwise normal", with a
  proof through Theorems 9 and 8;
- page 184, Theorem 14: collectionwise normality implies normality, but not conversely.

The source is a strong primary theorem-and-proof lead. It is not `H0`: no independent reviewer has
approved the transcription, incorporated definitions, background conventions, correction state,
or catalog identity, and no immutable source copy is part of an accepted evidence bundle.

## Clause crosswalk

| Catalog/source component | Source meaning | Prospective Lean surface | Intake disposition |
|---|---|---|---|
| `集态正规` | Bing's quantified separation property for every discrete collection of point sets | new source-reviewed predicate over indexed `Set X` families, using `IsOpen`, `closure`, unions, and disjointness | definition and modern-equivalence audit open |
| discrete collection | pairwise disjoint closures and closed union for every subcollection | `Set.PairwiseDisjoint` is only one ingredient; closure/subfamily-union clauses need encoding | adjacent API checked, exact predicate open |
| omitted Moore-space condition | regular developable space | `RegularSpace X` plus a new source-reviewed development predicate | catalog/source mismatch must be resolved |
| developable | countable sequence of open covers eventually star-refining every point-neighborhood | open covers, `Nat`-indexed families, stars/refinement | no pinned declaration located |
| metrizable | existence of a metric compatible with the topology | `TopologicalSpace.MetrizableSpace X` is a candidate conclusion | candidate API checked; transport to source metric convention open |
| Theorem 10 proof | collectionwise normal Moore space -> screenable -> metrizable | later obligation tree must represent Theorems 9 and 8 or an independently checked route | no proof credit at intake |
| `已验证` | metadata screening label only | accepted node receipt and kernel evidence would be required | no credit |

## Statement boundary

No canonical mathematical or Lean proposition is frozen. The catalog gloss omits the Moore-space
hypothesis present in the inspected theorem and does not identify a theorem/page. Choosing Theorem
10 is plausible but requires integration-lane source approval; deleting its Moore/developable
hypothesis would broaden the source into an unsupported and generally false implication.

Accordingly the canonical module, declaration/expression, domains, ordered binders, hypotheses,
conclusion, alternate encodings, excluded cases, expression hash, and environment fingerprint stay
unset. The next phase must resolve the source identity and every definition-level choice in
`scope-map.md`, then elaborate and mutation-test that exact target before any proof evidence is
inspected.
