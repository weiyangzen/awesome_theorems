# Source-statement crosswalk

## Repository source record

The only repository-supplied record is `Docs/researches/math_theorems.md:4657-4662`, introduced in
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`:

| Catalog field | Received value | Statement consequence |
|---|---|---|
| title | `局部紧性定理` | Names a broad theorem family, not one proposition. |
| attribution | many mathematicians | Does not identify a source, definition, or proof. |
| time | twentieth century | Does not select a work or edition. |
| statement | `局部紧空间的性质` | Names a topic and supplies no binders, assumptions, or conclusion. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; supplies no human or machine proof credit. |

The generated Stage0 record at `Docs/Stage0_Blueprint.md:17179-17204` repeats that gloss while
marking the formal system, definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links as pending. It does not enrich the statement.

The catalog is a secondary compilation with no bibliography for this entry. No primary source
edition, theorem/page locator, proof boundary, dependent result, correction history, errata check,
translation, or independent reviewer has been supplied or accepted. Thus the received source
record is E5 intake provenance, not H0 or H1 evidence for an exact proposition.

## Phrase-to-statement map

| Received or candidate component | Required source decision | Prospective Lean component | Intake result |
|---|---|---|---|
| locally compact space | exact definition and separation convention | `WeaklyLocallyCompactSpace` or `LocallyCompactSpace` | unresolved; interfaces are not interchangeable in general |
| compact neighborhood | membership, openness/closedness, and compactness convention | `exists_compact_mem_nhds` or `LocallyCompactSpace.local_compact_nhds` | candidate definition/characterization only |
| neighborhood basis | compact versus compact-and-closed sets | `compact_basis_nhds` or `isCompact_isClosed_basis_nhds` | candidate consequence only |
| relatively compact open set | whether closure must be compact and which separation assumptions apply | `exists_isOpen_mem_isCompact_closure` | R1-dependent candidate only |
| properties | one exact preservation, existence, implication, or equivalence theorem | products, subspaces, embeddings, quotients, Baire or other declarations | no result selected |
| compactification | construction, topology, Hausdorff assumptions, universal property | future target-specific encoding | belongs to separate `THM-M-0629` unless explicitly reconciled |

There are consequently no ordered binders, hypotheses, exact conclusion, credited alternate
encoding, statement fingerprint, canonical obligation, or proof body.

## Formal-source boundary

A bounded repository-local and pinned-mathlib inspection found the following adjacent declarations
at mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `WeaklyLocallyCompactSpace`, `exists_compact_mem_nhds`;
- `LocallyCompactSpace`, `LocallyCompactSpace.local_compact_nhds`;
- `compact_basis_nhds`, `local_compact_nhds`, `exists_compact_subset`, and
  `exists_compact_between`;
- in an R1 context, `isCompact_isClosed_basis_nhds`,
  `exists_mem_nhds_isCompact_isClosed`,
  `WeaklyLocallyCompactSpace.locallyCompactSpace`, and
  `exists_isOpen_mem_isCompact_closure`.

Their differing types confirm rather than resolve the catalog ambiguity. The probe authenticates
names and types only. This bounded inspection is not the dependency-ordered anchor audit, does not
claim exhaustive discovery, and gives no statement or proof credit.

## Human-source gate

To leave `H5`, an accountable reviewer must first approve a stable truth-valued target and an
immutable primary or authoritative source. The crosswalk must then bind the exact theorem and
incorporated definitions, every assumption and conclusion, proof and dependency boundaries,
corrections and errata, translation, and each source component to the mathematical and Lean
encodings. Until that happens, ordinary statement and theorem-proof execution remains blocked.
