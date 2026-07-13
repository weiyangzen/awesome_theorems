# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6460-6465` supplies exactly the title `Margulis构造`, attribution
Grigory Margulis, year 1973, gloss `扩展图的显式构造`, importance `高`, and status `已验证`. All six
uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, definition,
bibliography, theorem number, assumptions, proof boundary, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:24062-24087` mechanically repeats the gloss while explicitly leaving
precise definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
`source_status_untrusted`, resets the target to `L0 / rework_required`, and states
`theorem_complete=false`.

## Historical publication lead

A plausible match to the catalog's author, date, and subject is:

> G. A. Margulis, "Explicit constructions of concentrators," *Problemy Peredachi Informatsii*
> 9(4) (1973), 71-80; English translation, *Problems of Information Transmission* 9 (1973),
> 325-332.

This is a bibliographic discovery lead, not an accepted source. The catalog does not cite it; no
edition was preserved in the dossier; and no exact definition, numbered proposition, page-level
proof boundary, translation comparison, correction/errata disposition, or independent review was
completed. The two pagination conventions must be verified against an admitted edition.

The later G. A. Margulis paper "Explicit constructions of graphs without short cycles and low
density codes," *Combinatorica* 2(1) (1982), 71-78, DOI `10.1007/BF02579283`, was identified during
bibliographic discrimination. It is not the 1973 source and is explicitly non-substitutable.

## Clause crosswalk

| Supplied or candidate phrase | Mathematical component | Lean component required later | Intake result |
|---|---|---|---|
| `Margulis construction` | one historically identified construction or equivalent family | exact source-selected graph/generator definition | named family only |
| `explicit construction` | formula, algebraic family, or effective generator | construction data plus a proved well-formedness/effectiveness contract | explicitness standard open |
| `expander graphs` | vertex, edge, conductance, or spectral expanders | one exact expansion predicate, normalization, constants, and transports | predicate open |
| `concentrators` | source-specific bipartite or network concentration property | exact source definition and a checked bridge to any expander formulation | relationship unproved |
| Grigory Margulis / 1973 | historical provenance | immutable edition, locator, translation, errata, and source-node map | publication lead only |
| `已验证` | untrusted catalog metadata | inspected human proof and kernel receipts would be required | no H or M credit |

## Missing source-to-statement map

Before leaving `H1`, reviewers must admit an immutable source edition and map its exact graph model,
carrier, generator maps, modulus restrictions, degree/regularity convention, expansion or
concentration definition, constants, ordered quantifiers, exceptional cases, and conclusion. They
must also decide whether a familiar later Margulis-Gabber-Galil formulation is identical, a proved
transport, a strengthening, or a distinct result. A second reviewer must approve this mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks `SimpleGraph.fromRel`, neighborhood, degree, regularity, adjacency-matrix, and `ZMod` APIs.
A bounded source-name query found no exact Margulis graph, graph-expander, concentrator, vertex-
expansion, edge-expansion, or Cheeger-constant declaration in pinned mathlib or repo-local Lean.
Generic graph and modular arithmetic infrastructure neither identifies nor proves the target.

This bounded query is intake discovery, not the downstream immutable anchor audit or a global
absence theorem. The canonical module/expression, elaborated hash, environment-expression
fingerprint, checked alternate encodings, and statement mutations remain null.
