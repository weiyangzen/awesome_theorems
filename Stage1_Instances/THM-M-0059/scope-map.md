# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-0059`, title `阿达马不等式`, attribution Jacques Hadamard,
year 1893, and the gloss `行列式的上界估计`. The record supplies no bibliography, formula,
definition, ordered binders, hypotheses, conclusion, proof boundary, correction history, or formal
artifact. Importance `中` and status `已验证` are inventory metadata only.

The most familiar candidate is the row form for a finite real or complex square matrix `A`:
the absolute determinant is at most the product of the Euclidean norms of its rows. The analogous
column form follows by transposition. This description is a candidate family boundary, not a
frozen canonical statement.

## Decisions required at statement freeze

1. Preserve and hash a lawful source edition, select a pinpoint proposition and proof boundary,
   map every incorporated definition and assumption, audit corrections, and obtain independent
   review.
2. Fix the scalar domain: real matrices, complex matrices, or a source-justified generalization.
   The pinned volume-form theorem is specifically real.
3. Fix the square matrix representation and finite index: `Matrix (Fin n) (Fin n) Real`, an
   arbitrary finite index type, or a coordinate-free family of vectors in an `n`-dimensional real
   inner product space.
4. Choose rows or columns and machine-check any credited transpose transport. Do not identify
   them by theorem name alone.
5. Define the norm precisely as the Euclidean/inner-product norm and decide whether the displayed
   bound is unsquared, squared, or accompanied by the Gram-determinant identity.
6. Decide whether the theorem includes only the inequality, the orthogonal-row equality result,
   or a full equality iff characterization. The pinned candidate proves the inequality and a
   separate orthogonal-family equality, not the converse characterization.
7. Freeze ordered binders, universes, typeclass instances, orientation choice, determinant and
   absolute-value encodings, alternate forms, profiles, and all boundary cases.

## Degenerate and boundary cases

No case is excluded at intake. Source review must dispose of dimension zero and one, the zero
matrix, a zero row or column, singular matrices, diagonal and orthogonal-row matrices, repeated or
proportional rows, and matrices with negative or complex determinant. It must also decide whether
the empty product and zero-by-zero determinant make the dimension-zero result part of the theorem.

The pinned volume-form theorem explicitly handles dimension zero, but that implementation fact
must not silently determine the source convention. Likewise, the real coordinate-free theorem
does not justify a complex matrix statement without a checked source and formal transport.

## Explicit non-substitutions

- `Matrix.det_le` in `Mathlib.LinearAlgebra.Matrix.AbsoluteValue` gives the different factorial
  entrywise estimate `|det A| <= n! x^n`; it is not Hadamard's product-of-row-norms inequality.
- `Matrix.hadamard` is the entrywise Hadamard product and is unrelated to the determinant bound.
- Hadamard's three-lines, three-circles, maximal-determinant, and Hadamard-matrix results are
  namesakes, not substitutes.
- A Gram determinant inequality, volume-form bound, or fixed-dimensional example receives root
  credit only after a checked relationship to the source-selected matrix claim.
- An equality-only result, orthogonal special case, real-only result for a source-selected complex
  root, or row-only result for a selected column root cannot replace the exact claim.
- A structure, hypothesis, axiom, oracle, or unchecked certificate storing the desired bound is
  not a proof. The catalog's `已验证` label and the discovery probe supply no proof credit.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Analysis.InnerProductSpace.Orientation` contains
`Orientation.abs_volumeForm_apply_le`, with conclusion
`|o.volumeForm v| <= product i, norm (v i)` for `n` vectors in an `n`-dimensional real inner
product space. `Orientation.volumeForm_robust'`, `Basis.det_apply`, and
`Pi.basisFun_det_apply` are candidate bridge interfaces. The probe checks interfaces only. No
canonical Lean target, elaborated-expression hash, checked matrix transport, statement mutation
suite, accepted terminal-body provenance, obligation registry, or proof receipt is created at
intake.
