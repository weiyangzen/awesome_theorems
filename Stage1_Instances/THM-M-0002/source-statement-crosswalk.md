# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names the five lemma and gives only the gloss "an isomorphism
property of morphisms in a commutative diagram." It supplies no author, edition, theorem number,
page, diagram, or hypotheses. The `已验证` field is metadata, not primary-source or kernel evidence.

## Candidate primary-source family

Saunders Mac Lane, *Homology*, Springer, 1963, is a candidate classical primary exposition of the
diagram lemmas in homological algebra. A stable scan must still be inspected to record the exact
chapter/theorem/page and wording. This citation is a discovery anchor only and does not establish
H0. A later reviewer must also check edition differences and errata.

## Statement crosswalk

| Repository/source concept | Conventional mathematical meaning | Anticipated Lean representation | Intake status |
|---|---|---|---|
| "five lemma" | two exact five-object rows in a commutative diagram | two `ComposableArrows C 4` objects and a morphism between them | family identified, not frozen |
| exact rows | consecutive image/kernel agreement | `R₁.Exact` and `R₂.Exact` or source-faithful component hypotheses | exact scope unresolved |
| outer map conditions | epi, iso, iso, mono on vertical maps 1, 2, 4, 5 | `Epi`, `IsIso`, `IsIso`, `Mono` on indexed components | candidate only |
| isomorphism property | middle vertical map is an isomorphism | `IsIso` on component 3 | candidate conclusion |

## Lean discovery boundary

The unaccepted legacy module points to
`CategoryTheory.Abelian.isIso_of_epi_of_isIso_of_isIso_of_mono` and proposes a
`ComposableArrows` wrapper in an abelian category. This is strong evidence that an exact Lean
candidate is locally discoverable, but rev-5.6 requires the later statement and anchor-audit nodes
to inspect the pinned source, elaborate the exact type, fingerprint the environment, test scope
mutations, and audit terminal provenance. No result from that module is inherited here.

Before H0, an independent reviewer must crosswalk every source assumption and conclusion, including
diagram orientation and exactness locations, to the canonical claim and record source errata.
