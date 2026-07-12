# THM-M-0013 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:114-119` names the fundamental theorem of Galois theory,
attributes it to Evariste Galois in 1832, and states only that field extensions correspond to
subgroups of the Galois group. `Docs/Stage0_Blueprint.md:474-499` repeats that gloss while leaving
the exact definitions, premises, proof path, axioms, and formal artifact open. The manifest carries
`verified` only as untrusted source metadata. These records do not distinguish finite from infinite
Galois theory or identify which standard supplementary clauses belong to the root.

The six catalog lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; their blob and excerpt digests are recorded in
`instance.json`. This freezes the repository wording, not its mathematical or historical fidelity.

## Inspected modern source

J. S. Milne, *Fields and Galois Theory*, version 5.10, September 2022, is author-hosted at
`https://www.jmilne.org/math/CourseNotes/FT.pdf`. The inspected PDF has SHA-256
`5c43ea0bf4ec190b819727fe720414a80e09f9e762533d08bad5b8a0b6de7273`.

- Theorem 3.17, pages 39-40, assumes a Galois extension `E/F`. In Milne's Definition 3.9 this means
  finite, normal, and separable. It gives inverse maps between all subgroups of `Gal(E/F)` and
  intermediate fields, reverses order, and also states index/degree, conjugacy, normality, and
  quotient conclusions.
- Theorem 7.13, pages 98-99, assumes a possibly infinite Galois extension and instead corresponds
  intermediate fields with closed subgroups in the Krull topology. It includes analogous
  order/open-degree/conjugacy/normality/quotient clauses.
- The version history reports revisions and corrections through version 5.10, but this intake did
  not establish a theorem-specific errata ledger or independent source review.

Milne is an authoritative modern exposition, not the catalog's alleged 1832 primary source. The
catalog does not say whether it means the finite theorem, the infinite theorem, or only their core
correspondence. The source supports `H1` discovery and disambiguation, not `H0` acceptance.

## Immutable Stacks source

The Stacks Project source at commit `3683021e95ea1610e2250658d59abc18fdf0bd7b`, source blob
`7908ad0050110bdddb7d0fe656c30b4b180a89e0`, was inspected at `fields.tex:2783-2822`. The file has
SHA-256 `87e07f0373dc60cfc284e2f19078bc9bc7ab0b89c40eef83941f6c38c765c549`.
Its theorem `theorem-galois-theory`, rendered as Tag `09DW`, assumes a finite Galois extension,
states the fixed-base-field identity and subgroup/subextension bijection, and characterizes the
normal-subgroup/Galois-subextension correspondence. The same pinned source separately states the
infinite theorem with closed subgroups at lines 3053 onward. Pinned mathlib annotates
`IsGalois.intermediateFieldEquivSubgroup` with `[stacks 09DW]`, making this a direct source lead for
the formal candidate. It remains uncredited pending exact root selection, full proof-node and
errata mapping, historical-source policy, and independent review.

## Component crosswalk

| Catalog component | Finite source candidate | Infinite source candidate | Intake decision |
|---|---|---|---|
| field extension | finite normal separable `E/F` | algebraic Galois `Omega/F` | unresolved |
| Galois group | `Gal(E/F)` | Krull-topological `Gal(Omega/F)` | unresolved |
| subgroup | every subgroup | every closed subgroup | unresolved and material |
| field on the other side | intermediate fields `F <= M <= E` | intermediate fields `F <= M <= Omega` | family preserved |
| correspondence maps | fixed field and fixing subgroup | fixed field and fixing subgroup | family preserved |
| order | inclusion reversing | inclusion reversing | must be explicit in final root |
| supplementary clauses | Milne: index, conjugacy, normality, quotient; Stacks `09DW`: base fixed field and normality | open/degree, conjugacy, normality, quotient | root membership unresolved |

## Lean candidate crosswalk

| Candidate | Exact observed type boundary | Source relationship | Credit boundary |
|---|---|---|---|
| `IsGalois.intermediateFieldEquivSubgroup` | `IntermediateField F E` order-equivalent to the order dual of `Subgroup Gal(E/F)` under finite-dimensional and Galois instances | matches the core of finite Theorem 3.17 | candidate only; no accepted statement identity or proof-body audit |
| `InfiniteGalois.IntermediateFieldEquivClosedSubgroup` | `IntermediateField k K` order-equivalent to the order dual of closed subgroups of `Gal(K/k)` under `IsGalois k K` | matches the core of infinite Theorem 7.13 | candidate only; catalog variant unresolved |
| finite inverse lemmas | fixed field of a fixing subgroup and fixing subgroup of a fixed field | establish the inverse maps | components only; not independently the full selected root |
| normality/quotient APIs | normal fixed fields and quotient-to-automorphism equivalences | address part of standard supplementary clause (d) | scope and provenance audit deferred |

The bounded intake probe checks only that these pinned declarations elaborate. It does not inspect
terminal bodies, transitive dependencies, axioms, placeholders, historical alignment, all clauses,
or proof architecture. Those belong to statement and anchor-audit phases after root selection.

## H0 work still required

The source phase must select an exact versioned theorem, map every assumption and conclusion,
record theorem-specific corrections or errata, decide the historical-source role and 1832
attribution, map all source nodes into the obligation registry, and obtain independent qualified
review. Until then no source or human-proof completion is accepted.
