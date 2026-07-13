# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md` records `四色定理`, attributes it to Appel/Haken, gives 1976,
and supplies the complete gloss `平面图可用四种颜色着色` ("planar graphs can be colored with four
colors"). It gives no citation, definitions, quantifiers, assumptions, boundary cases, proof, or
formal declaration. The record entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/researches/classified_theorems.md` and
`Docs/researches/formalization_classification.md` add secondary claims that Gonthier completed a Coq
formalization using a combinatorial proof and computation. They cite his 2008 Notices article, but
do not themselves provide an edition-level premise/conclusion/errata crosswalk. Stage0 leaves the
exact definitions, proof tree, axioms, machine status, and artifact links open. The manifest retains
`已验证` only as `source_status_untrusted`.

## Inspected authoritative source lead

Georges Gonthier, *A computer-checked proof of the Four Color Theorem*, INRIA report deposited as
HAL `hal-04034866v1`, 58 pages, was inspected on 2026-07-13. Section 2, report pages 2-4, gives:

- the nutshell claim that any planar map can be colored with four colors;
- the more explicit claim that regions of any simple planar map can be colored with four colors so
  adjacent regions have different colors;
- definitions of a planar map as pairwise-disjoint plane subsets called regions, a simple map as
  one with connected open regions, adjacency by a shared closure point that is not a corner, and a
  corner as a point in at least three region closures;
- the formal high-level declaration (printed on report page 3) `four_color (m : map R) :
  simple_map m -> map_colorable 4 m` in the historical script vocabulary;
- the finite map and combinatorial hypermap reductions discussed in Sections 2-3.

This is an authoritative, detailed source lead and supports provisional H1. It is not H0: the
integration lane has not admitted a stable local source object, audited all incorporated definitions,
assumptions, corrections and errata, mapped every proof node, or obtained independent review.

## Formal-source lead at an immutable revision

The maintained `rocq-community/fourcolor` repository was inspected through GitHub's content API at
commit `f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2` (tree
`b2da69f860096cce9480f2645298a2d04587f360`). Its README says the library contains a formal Coq
proof and records the current dependency and license boundary. At that commit:

| File/declaration | Source proposition | Intake relevance |
|---|---|---|
| `theories/proof/fourcolor.v::four_color` | `simple_map m -> colorable_with 4 m` for an arbitrary `Real.model` | closest high-level map theorem |
| `theories/proof/fourcolor.v::four_color_finite` | `finite_simple_map m -> colorable_with 4 m` | finite map reduction |
| `theories/proof/combinatorial4ct.v::four_color_hypermap` | `planar_bridgeless G -> four_colorable G` | constructive combinatorial core |

These are external Rocq/Coq candidates, not Lean 4 declarations. The project was neither fetched
into `.lake` nor built in this worker. Full source/dependency/axiom/placeholder/proof-body provenance
and exact transport to the future Lean target belong to `ANCHOR_AUDIT`; no M1 or M0 is assigned here.

## Phrase crosswalk

| Catalog/source phrase | Mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `平面图` / planar graph | finite simple graph with a source-selected planar representation | `G : SimpleGraph V` plus a future planar predicate/embedding | graph carrier plausible; planarity API absent and convention open |
| "four colors" | a proper coloring using at most four colors | `G.Colorable 4`, definitionally `Nonempty (G.Coloring (Fin 4))` | pinned coloring encoding authenticated only |
| "simple planar map" | pairwise-disjoint connected open plane regions | future real-plane map/region structure | source-defined family; no pinned Lean representation located |
| adjacent regions | closures meet away from points in at least three closures | future adjacency relation and graph-map bridge | exact topology and bridge open |
| `four_color` | high-level external theorem over a real model | no Lean declaration | immutable Rocq/Coq source lead only |
| `four_color_hypermap` | planar bridgeless finite hypermaps are four-colorable | future combinatorial intermediate | narrower core; not a substitute for the root |
| `已验证` | repository inventory label | no formal object | explicitly rejected as evidence |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Coloring` defines proper coloring, `Colorable`, and chromatic
number. Its module TODO explicitly lists planar graphs. Bounded case-insensitive searches of pinned
mathlib and tracked Lean files found no Four Color theorem and no target-specific `THM-M-0833`
artifact. This is narrow intake discovery, not the exhaustive immutable anchor audit and not proof
of absence from all Lean projects.

The statement phase must first obtain approval for one exact source proposition and representation,
then freeze ordered binders, all hypotheses and degenerate cases, minimal pinned imports, normalized
expression and environment hashes, checked graph/map transports, and the four required mutation
classes. Until then the formal target remains null and proof inspection is ineligible.

