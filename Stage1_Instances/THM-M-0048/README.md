# THM-M-0048 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item named the
Cauchy-Binet formula. The repository attributes it to Augustin Cauchy and Jacques Binet in 1812,
describes it only as "the determinant formula for a matrix product," and labels it verified. The
label is untrusted inventory metadata, not an exact source statement or machine-proof evidence.

## Planned boundary

The title normally denotes the rectangular minor-sum identity: the determinant of a square product
`A * B`, formed from an `m`-by-`n` matrix and an `n`-by-`m` matrix, is the sum over `m`-element
choices of the intermediate index of the products of the corresponding minors. The catalog gloss,
however, does not distinguish that theorem from square determinant multiplicativity, and supplies
no coefficient domain, dimensions, minor convention, ordering, boundary policy, or source citation.
Intake therefore records the conventional rectangular formula as a candidate family but does not
silently promote it, or the easier square formula, to the canonical root.

Takis Konstantopoulos's immutable arXiv paper *A multilinear algebra proof of the Cauchy-Binet
formula and a multilinear version of Parseval's identity*, version 1, is an inspected complete
modern source lead. It states the rectangular field-valued formula precisely and derives it from a
proved exterior-algebra identity. It is not the catalog's cited source, does not justify the wider
candidate commutative-ring domain, has observed prose and bibliography defects, and has not passed
independent source review. Jiang Zeng's 1993 bijective proof is a second bibliographic lead. These
support `H1`, not `H0`.

Pinned mathlib provides determinants, matrix multiplication, submatrices, ordered finite-subset
encodings, and `Matrix.det_mul`. `IntakeProbe.lean` authenticates those interfaces and elaborates a
candidate rectangular proposition shape. `Matrix.det_mul` is only the square specialization, and
the candidate proposition is not a canonical statement or proof. A bounded repository and pinned
mathlib search found no named terminal Cauchy-Binet minor-sum theorem.

The provisional vector is `[H1, M3, R4]`: a published human proof lead exists but its exact source
contract is unaudited; relevant interfaces and a candidate statement shape elaborate but no exact
root or proof is credited; and no source-faithful readable proof reconstruction exists. All six
downstream tasks remain open. No accepted execution state, `H0`, `M0`, `R0`, audit completion,
theorem completion, or master acceptance is claimed.
