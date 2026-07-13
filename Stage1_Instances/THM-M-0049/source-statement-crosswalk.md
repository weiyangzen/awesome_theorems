# THM-M-0049 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:370-375` contains the complete catalog record:

- name: `弗罗贝尼乌斯不等式`;
- attribution: Ferdinand Frobenius;
- date: 1911;
- statement: `矩阵秩的不等式`;
- importance: medium;
- formalization status: `已验证`.

All six lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no
bibliography, displayed inequality, scalar domain, matrix dimensions, assumptions, definitions,
proof, or formal artifact. `Docs/Stage0_Blueprint.md:1456-1481` repeats the gloss and explicitly
leaves exact definitions and premises, proof route, equivalent forms, axioms, logic dependencies,
machine status, and artifact links open. Rev-5.6 resets the item to `L0 / rework_required` and
marks the catalog verification label untrusted.

## Human-source leads

Alex Taylor, *An Algorithmic Approach To Solving B = BCX + YAB Using Quotient Spaces*,
arXiv `1909.13202v1` (29 September 2019), was inspected from the immutable versioned PDF on
2026-07-13. Printed page 1 states the Frobenius rank inequality for matrices over a field:

`rank (A * B * C) + rank B >= rank (A * B) + rank (B * C)`.

The same page gives a quotient-space proof via the surjection
`range B / range (B * C) -> range (A * B) / range (A * B * C)` induced by multiplication by `A`.
This is a precise complete modern source lead. It is not `H0`: it is neither the historical
Frobenius source nor a source named by the catalog; it cites equality work rather than supplying a
historical attribution audit; and complete notation, assumption, errata, source-to-node, and
independent-review gates remain open.

Edward T. H. Wang, *A combinatorial application of the Frobenius inequality on rank function to
maximum set of commuting nilpotent matrices*, *Linear and Multilinear Algebra* **8** (1979), no. 1,
79-82, DOI `10.1080/03081087908817301`, is a second bibliographic lead confirming the theorem name
in rank literature. Crossref metadata was inspected, but its exact theorem passage, assumptions,
proof, and source genealogy were not admitted. It provides no additional H credit.

The catalog's Frobenius attribution and 1911 date remain unverified leads. No primary title,
edition, page, displayed inequality, proof, translation, or correction record was located and
admitted during intake. These gaps keep the provisional human status at `H1`, not `H0`.

## Clause crosswalk

| Catalog or lead component | Candidate mathematical reading | Pinned Lean interface | Intake status |
|---|---|---|---|
| "matrix ranks" | natural-number dimensions of column spaces | `Matrix.rank` | interface authenticated; convention not source-frozen |
| composable `A`, `B`, `C` | shapes `m x n`, `n x p`, `p x q` | `Matrix`, matrix multiplication | candidate shape elaborates |
| `rank (A * B)` | rank after the first composition | `Matrix.rank_mul_le_left/right` | adjacent upper bounds only |
| `rank (B * C)` | rank after the second composition | same | adjacent upper bounds only |
| `rank (A * B * C)` | rank of the triple composite | `Matrix.mul_assoc`, `LinearMap.rank_comp_le` | association and target identity open |
| quotient dimension proof | compare quotients of nested ranges | rank-nullity and submodule APIs | prospective proof architecture only |
| zero-product specialization | ranks bounded by the middle dimension | `Matrix.rank_add_rank_le_card_of_mul_eq_zero` | related theorem, not the root |
| Frobenius / 1911 | historical attribution | none | primary-source audit open |
| `已验证` | catalog status | none | no H/M/R credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.LinearAlgebra.Matrix.Rank` supplies:

- `Matrix.rank_mul_le_left`, `Matrix.rank_mul_le_right`, and `Matrix.rank_mul_le` for two-factor
  upper bounds;
- `Matrix.rank_eq_finrank_range_toLin` for matrix/linear-map rank transport;
- `Matrix.rank_add_rank_le_card_of_mul_eq_zero` for a zero-product rank bound.

Imported modules also supply `LinearMap.rank_comp_le_left`, `LinearMap.rank_comp_le_right`,
`LinearMap.rank_comp_le`, and `LinearMap.finrank_range_add_finrank_ker`. `IntakeProbe.lean`
authenticates these signatures and verifies that one finite field-valued triple-product inequality
shape elaborates as a proposition.

A bounded exact-topic search of repository Lean and pinned mathlib found no declaration named or
documented as the Frobenius rank inequality and no terminal theorem matching the candidate full
triple-product lower bound. This is an intake observation, not a frozen discovery protocol,
exhaustive anchor audit, declaration-dependency audit, or proof-body provenance result.

## Exactness gaps

The statement gate must admit a pinpoint source and resolve theorem identity, coefficient domain,
matrix shapes, finite-index and universe assumptions, multiplication association, rank convention,
inequality orientation, alternate encodings, and every boundary case. It must then elaborate and
fingerprint the canonical expression, check all credited transports, and run removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. Neither the candidate shape nor any adjacent
mathlib declaration closes those gaps.

