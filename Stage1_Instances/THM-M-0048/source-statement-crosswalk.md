# THM-M-0048 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:363-368` contains the complete catalog record:

- name: `柯西-比内公式`;
- attribution: Augustin Cauchy / Jacques Binet;
- date: 1812;
- statement: `矩阵乘积的行列式公式`;
- importance: high;
- formalization status: `已验证`.

All six lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They include no
bibliography, displayed formula, scalar domain, dimensions, assumptions, definitions, proof, or
formal artifact. `Docs/Stage0_Blueprint.md:1429-1454` repeats the gloss and explicitly leaves exact
definitions and premises, proof route, equivalent forms, axioms, logic dependencies, machine
status, and artifact links open. Rev-5.6 therefore resets the item to `L0 / rework_required`.

## Human-source leads

Takis Konstantopoulos, "A multilinear algebra proof of the Cauchy-Binet formula and a multilinear
version of Parseval's identity," arXiv `1305.0644v1` (3 May 2013), was inspected from the immutable
versioned PDF on 2026-07-13. Printed page 1, formula (1), states that for `A` and `B` over the reals
or any field, of sizes `n x N` and `N x n` with `n <= N`, `det(A B)` is the sum over strictly
increasing `n`-subsets of `det(A_sigma) det(B^sigma)`, where columns of `A` and rows of `B` are
selected. Section 3, Theorem 1 on printed page 3 proves the more general exterior-power identity
(6); printed page 4 derives determinant identity (9), recovers formula (1) for `R^n` and `R^N`, and
states that `N = n` gives determinant multiplicativity.

This is a strong complete modern source lead, not `H0`. It is not a primary Cauchy/Binet source or
a citation supplied by the catalog; its field scope does not authorize the wider prospective Lean
`CommRing` claim; complete definition and proof-node mapping, independent review, and historical
attribution remain open. The inspected text also contains the grammatical phrase "is requires" on
printed page 2 and an apparent `2986` year in one bibliography entry on printed page 8. Those
observed defects do not alter formulas (1), (6), or (9), but require explicit errata review.

Jiang Zeng, "A bijective proof of Muir's identity and the Cauchy-Binet formula," *Linear Algebra
and its Applications* **184** (1993), pages 79-82, DOI
`10.1016/0024-3795(93)90371-T`, is a second credible published complete-proof lead. Publisher and
bibliographic metadata were inspected, but its theorem passage and proof were not available as an
admitted immutable input. It receives no additional H credit.

The catalog's Cauchy/Binet attribution and 1812 date are another lead, not a source packet. No
primary edition, page, translation, formula, proof, or correction record was inspected. These
limitations keep the human status at `H1`, not `H0`.

## Component crosswalk

| Catalog component | Candidate mathematical reading | Pinned Lean interface | Intake status |
|---|---|---|---|
| "matrix product" | `A : m x n`, `B : n x m`, product `A * B : m x m` | `Matrix`, matrix multiplication | shapes not source-ratified |
| "determinant" | determinant of the square product | `Matrix.det` | interface authenticated |
| "formula" | sum over `m`-element intermediate subsets of products of complementary minors | `Set.powersetCard`, `Matrix.submatrix`, `Matrix.det` | candidate expression elaborates; no proof |
| subset order | increasing enumeration of each finite subset | `Set.powersetCard.ofFinEmbEquiv.symm` | one candidate convention only |
| square case | `det (M * N) = det M * det N` | `Matrix.det_mul` | strict specialization/related anchor, not root credit |
| Cauchy/Binet, 1812 | historical attribution | none | primary-source audit open |
| `已验证` | catalog status | none | no H/M/R credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.LinearAlgebra.Matrix.Determinant.Basic` supplies `Matrix.det_apply`, `Matrix.det_mul_aux`,
`Matrix.det_mul`, `Matrix.submatrix`, and `Matrix.det_submatrix_equiv_self`. The proof of
`Matrix.det_mul` expands the product determinant and eliminates nonbijective intermediate maps. It
is relevant architecture, but its two matrices share one square index type.

`Mathlib.Order.Hom.PowersetCard` supplies an equivalence between order embeddings `Fin m` into a
linear order and `m`-element finite subsets. This supports an order-stable candidate encoding of
the full rectangular sum. `IntakeProbe.lean` verifies that the corresponding proposition shape
elaborates over a commutative ring.

A bounded exact-topic search of repo-local Lean and pinned mathlib found no declaration named or
documented as Cauchy-Binet/Binet-Cauchy and no terminal theorem matching the general minor-sum
formula. That is an intake observation, not a precommitted exhaustive anchor audit or terminal-body
provenance result.

Outside the pinned dependency closure, `leanprover/hex-determinant` at immutable revision
`20f5785e9c85e9faa481d6b67c1382b6655b842e` contains module
`HexDeterminant.CauchyBinet` and declarations
`Hex.Matrix.det_columnSumMatrix_eq_sum_columnTuples` and
`Hex.Matrix.det_gramMatrix_eq_sum_columnTuples`. The inspected source file had SHA-256
`1b75c932339f8f89864fcbc5c1a924321d3e4dde2065962eee45812769a624d6` and no bounded forbidden-token
match. It uses a custom matrix/determinant implementation and an ordered-column-tuple or Gram
form, targets Lean 4.32.0-rc1, is absent from this repository's dependency lock, and exposes no
checked bridge to the candidate standard subset-minor root. It is a later anchor-audit lead only,
not M0 or proof credit.

## Exactness gaps

The source statement gate must fix the full versus square theorem identity, coefficient domain,
dimension relation, subset and ordering conventions, matrix orientation, product order, and every
degenerate case. It must then admit a pinpoint source, elaborate and fingerprint the canonical Lean
expression, check transports for alternate encodings, and run the required mutation classes. The
candidate expression and `Matrix.det_mul` cannot close any of those gaps by themselves.
