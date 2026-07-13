# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6201-6206` supplies exactly the title `图同态计数`, attribution
to many mathematicians, the twentieth century, the gloss `子图同态的计数`, importance "high," and
status `已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source ID,
theorem/page locator, definition, binder, hypothesis, conclusion, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23063-23088` repeats the gloss while explicitly leaving exact definitions
and premises, proof process, dependencies, alternate forms, axioms, machine status, and artifact
links open. Its generic planning language about a known closed result is not source evidence. The
rev-5.6 manifest preserves `已验证` only in `source_status_untrusted` and resets this target to
`L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `图同态` | adjacency-preserving map, with source/target graph classes fixed | `SimpleGraph.Hom` / `F →g G`, or a source-specific alternative | graph classes and map convention absent |
| `子图` | possibly "small/source graph," subgraph occurrence, injective copy, or induced copy | ordinary `Hom`, `Embedding`, or another predicate | wording does not distinguish them |
| `计数` | a proposition about a count, density, identity, inequality, characterization, or algorithm | `Fintype.card`, finite sum, probability, equality/bound, or complexity specification | conclusion absent |
| many mathematicians / twentieth century | an exact source-family discriminator | immutable source metadata | no theorem locator |
| `已验证` | untrusted inventory field | source proof and kernel receipt would be required | no H or M credit |

The gloss is a noun phrase, not a quantified assertion. Even the expression
`Fintype.card (F →g G)` is a term of type `Nat`, not a proposition and not a source-selected
theorem.

## Inspected source lead

Christian Borgs, Jennifer Chayes, Laszlo Lovasz, Vera T. Sos, and Katalin Vesztergombi,
*Counting Graph Homomorphisms*, in *Topics in Discrete Mathematics*, Algorithms and Combinatorics,
pages 315-371, DOI `10.1007/3-540-33700-8_18`, is a strong title and subject match. Crossref
confirmed the bibliographic metadata. A 45-page author manuscript dated February 2006 was
inspected from the Hungarian Academy of Sciences repository; its observed SHA-256 was
`2cc562e2036f3870c3b6ecfb27ff44d435a8c5e23f5db431cf640da9386c8b97`.

The manuscript confirms ambiguity rather than selecting a root. Its introduction defines
`hom(F,G)` as the number of adjacency-preserving maps and separately defines normalized density
`t(F,G)`. Section 2.1 distinguishes finite simple and weighted graphs, weighted homomorphism sums,
profiles, injective counts, induced counts, and surjective counts. Section 2.2 records distinct
identities for disjoint unions and products and conversion identities among count variants. Later
sections survey characterization, graph-limit, metric, property-testing, extremal, and statistical
physics results. The repository supplies no evidence that this survey, much less any one result in
it, is its intended source.

The manuscript is therefore discovery evidence only. It does not provide a source-to-root
crosswalk, theorem selection, proof boundary, correction audit, or independent review, and it
receives no H0 credit. The exact source may instead be an earlier Lovasz result, a later complexity
classification, or another work entirely.

## Source gate

There is no repository-selected mathematical proposition. Before leaving `H5`, an accountable
reviewer must identify and lawfully preserve the intended primary or authoritative source, select
and inspect the exact numbered result and incorporated definitions, map every binder, hypothesis,
conclusion, and proof boundary, audit corrections and errata, distinguish every count variant, and
obtain independent approval. Only then may the statement phase freeze and mutation-test an
identical Lean expression.

`H5` here does not assert that graph-homomorphism theorems are false or mathematically open. It
records that the catalog phrase is not yet a truth-valued target a Lean kernel could check.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Maps` defines `SimpleGraph.Hom` as a relation homomorphism and
the notation `F →g G`. `Mathlib.Data.Fintype.Pi` supplies `RelHom.instFintype` for finite
decidable relations. The checked discovery probe confirms that `Fintype (F →g G)` and
`Fintype.card (F →g G)` elaborate under finite decidable graph assumptions.

A bounded case-insensitive search over pinned mathlib and repository-local Lean sources found no
named general graph-homomorphism-count or homomorphism-density theorem. Pinned mathlib's triangle
counting theorem is a specialized density/uniformity result, not a general homomorphism-count
target. This bounded result is not a formal absence theorem or the later immutable anchor audit.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations remain null. No statement elaboration, formal proof,
audit completion, or theorem completion is claimed.
