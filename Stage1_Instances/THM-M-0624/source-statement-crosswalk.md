# Source-statement crosswalk

## Repository source

The tracked inventory at `Docs/researches/math_theorems.md:4629-4634` contains exactly the title
`Nagata-Smirnov度量化定理`, attribution to Jun-iti Nagata and Yuri Smirnov, year 1950, the gloss
`拓扑空间可度量化的充要条件`, high importance, and status `已验证`. All six uncited lines entered
the repository in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:17071-17096` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact
links unresolved. The repository therefore identifies a theorem family but not a binder-complete
proposition. The inherited status is untrusted and earns no H, M, or receipt credit.

## Candidate statement source

The immutable nLab page `Nagata-Smirnov metrization theorem`, revision 4, dated 2019-04-05, states:
a topological space is metrizable exactly when it is regular, Hausdorff, and has a countably locally
finite base. Its referenced definition describes "countably locally finite" as a countable union of
locally finite families. This is a stable E5 secondary discovery lead, not a primary proof source.
The page's only reference is Wikipedia; it contains no primary theorem/page or proof.

zbMATH metadata identifies the two original bibliographic leads:

- Jun-iti Nagata, "On a necessary and sufficient condition of metrizability," *J. Inst.
  Polytechn., Osaka City Univ., Ser. A* **1** (1950), 93-100, Zbl `0041.09801`;
- Yu. M. Smirnov, "A necessary and sufficient condition for the metrizability of a topological
  space," *Dokl. Akad. Nauk SSSR*, new series **77** (1951), 197-200, in Russian, Zbl `0042.16801`.

Their article texts were not inspected, so the conventional formulation is not represented as a
primary-text transcription. Crossref also identifies a later lead, Jun-iti Nagata, "A theorem for
metrizability of a topological space," *Proceedings of the Japan Academy* **33** (1957), 128-130,
DOI `10.3792/pja/1195525113`; its text was likewise unavailable. No exact primary theorem locator,
definition chain, proof boundary, translation, correction history, errata record, or independent
review has been admitted. The source axis is therefore H1 rather than H0.

## Component crosswalk

| Catalog or candidate component | Source decision required | Prospective Lean component | Intake status |
|---|---|---|---|
| topological space | carrier, topology, universes, binder order | `X : Type u`, `[TopologicalSpace X]` | family carrier only; exact binders open |
| metrizable | compatible-metric meaning and transport | `TopologicalSpace.MetrizableSpace X` | adjacent interface authenticated; relationship not source-reviewed |
| regular and Hausdorff | exact separation convention and redundancy | `RegularSpace X` with `T2Space X`, or a reviewed equivalent such as `T3Space X` | proposition-critical choice open |
| countably locally finite base | exact countable decomposition, family indexing, overlap, and basis convention | candidate `B : Nat -> Set (Set X)`, `LocallyFinite` on each subtype family, and `IsTopologicalBasis (Union B)` | no canonical predicate or target selected |
| necessary and sufficient | both directions with identical domains and premises | one exact `Iff` plus checked transports | catalog supplies no conditions to place on either side |
| Nagata/Smirnov, 1950 | primary works, editions, theorem/page, definitions, proof boundary, errata, translation | source records only | unresolved bibliographic lead |
| `已验证` | accepted human and machine evidence | no formal component | explicitly rejected as evidence |

## Formal-source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the local API probe
authenticates:

- `TopologicalSpace.PseudoMetrizableSpace` and `TopologicalSpace.MetrizableSpace` in
  `Mathlib.Topology.Metrizable.Basic`;
- `RegularSpace`, `T2Space`, and `T3Space` in `Mathlib.Topology.Separation.Regular`;
- `TopologicalSpace.IsTopologicalBasis` in `Mathlib.Topology.Bases`; and
- `LocallyFinite` in `Mathlib.Topology.LocallyFinite`.

The pinned source defines `MetrizableSpace` through a compatible countably generated uniformity
plus T0, and `T3Space` as T0 plus `RegularSpace`. A source-reviewed crosswalk must decide how these
library conventions represent the chosen historical or modern statement.

A bounded repository and pinned-mathlib search found no declaration named for Nagata or Smirnov, no
packaged sigma-locally-finite-basis predicate, and no theorem combining metrizability, a topological
basis, and locally finite layers. This negative result is intake discovery only, not the exhaustive
immutable formal-candidate audit owned by `S56-M-0624-ANCHOR_AUDIT`.

## Human-source gate

Before H0 or exact-statement acceptance, an independent reviewer must approve an immutable primary
or authoritative proof source and map every material definition, premise, equivalence direction,
proof dependency, and conclusion to the canonical mathematical and Lean encodings, including
translation, correction, errata, and degenerate-case decisions. Until then there is no accepted
canonical claim, Lean expression, statement fingerprint, proof body, or theorem-completion credit.
