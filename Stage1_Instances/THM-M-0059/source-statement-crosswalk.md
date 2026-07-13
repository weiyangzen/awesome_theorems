# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:440-445` supplies exactly the title `阿达马不等式`, attribution
Jacques Hadamard, year 1893, gloss `行列式的上界估计`, importance `中`, and status `已验证`.
Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, formula, coefficient domain, dimension, row/column convention, norm, binders,
hypotheses, equality clause, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:1726-1751` repeats the sparse record while explicitly leaving the target
formal system, foundation, precise definitions and premises, proof route, dependencies, alternate
forms, axiom policy, machine status, and artifact links open. The rev-5.6 manifest preserves
`已验证` only as untrusted metadata and resets the target to `L0 / rework_required`.

## Historical source lead

The commonly cited original source is Jacques Hadamard, "Resolution d'une question relative aux
determinants," *Bulletin des Sciences Mathematiques*, second series, volume 17 (1893), pages
240-246. This matches the catalog author, year, and determinant subject. During intake, however,
no lawful immutable scan or exact passage was admitted. Its proposition, notation, coefficient
domain, premise set, equality boundary, proof nodes, corrections, and errata were not transcribed
or independently reviewed. It is therefore a bibliographic lead only and cannot support `H0`.

## Clause crosswalk

| Catalog component | Conventional candidate reading | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| determinant | determinant of a finite square matrix | `Matrix.det` | scalar, dimension, and matrix encoding not selected |
| upper bound | absolute determinant bounded by a product | `abs`, `Finset.prod`, ordered real inequality | exact formula is absent from the catalog |
| factors | Euclidean norms of rows or columns | inner-product norm on coordinate vectors | row/column and norm conventions unresolved |
| geometric form | volume of `n` vectors bounded by product of lengths | `Orientation.abs_volumeForm_apply_le` | direct real coordinate-free candidate, not yet source-mapped |
| matrix bridge | basis determinant equals matrix determinant | `Basis.det_apply`, `Pi.basisFun_det_apply` | exact row/column and volume-form composition remains unchecked |
| equality | equality for orthogonal rows; perhaps iff orthogonality under nonzero assumptions | `abs_volumeForm_apply_of_pairwise_orthogonal` | catalog does not say whether equality belongs to the root |
| verified | untrusted inventory label | no declaration or receipt | explicitly rejected as evidence |

## Pinned Lean candidates

Pinned mathlib module `Mathlib.Analysis.InnerProductSpace.Orientation` proves:

```text
Orientation.abs_volumeForm_apply_le
  (o : Orientation Real E (Fin n)) (v : Fin n -> E) :
  abs (o.volumeForm v) <= product i, norm (v i)
```

The module is pinned at revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; its source
SHA-256 is `d3a27e4111ddcf0e84e1b0672d830323279c044cc4fee21516268ea13f6f3375`.
The proof uses a Gram-Schmidt orthonormal basis, determinant factorization, and the real
Cauchy-Schwarz bound. `Orientation.volumeForm_robust'` connects the absolute volume form to a
basis determinant. `Basis.det_apply` identifies a basis determinant with `Matrix.det` of the
coordinate matrix, and `Pi.basisFun_det_apply` gives the ordinary function-space matrix form.

`Orientation.abs_volumeForm_apply_of_pairwise_orthogonal` supplies equality for pairwise
orthogonal vectors. It does not by itself provide a full equality characterization.
`Matrix.det_le` supplies only a factorial uniform-entry bound, while `Matrix.hadamard` defines an
entrywise product. Neither may be substituted for the source-selected root.

`IntakeProbe.lean` verifies the candidate interfaces and prints the direct axioms of
`Orientation.abs_volumeForm_apply_le`. It does not freeze the canonical target, implement the
matrix bridge, inspect terminal proof bodies exhaustively, close transitive trust, run statement
mutations, or create a proof receipt. The formal findings therefore support provisional `M3`,
not `M0-W`.

## Required statement/source admission

Before statement execution, an independent reviewer must preserve and hash a lawful primary or
authoritative source, select one exact inequality and any equality clause, transcribe all
definitions, binders, hypotheses, conclusions, and degenerate cases, audit corrections, and
approve the mapping to the exact Lean expression. Real/complex, row/column, matrix/volume-form,
squared/unsquared, Gram-determinant, orientation, and equality transports must be kernel-checked
wherever credited. Until then the canonical mathematical and Lean targets remain null.
