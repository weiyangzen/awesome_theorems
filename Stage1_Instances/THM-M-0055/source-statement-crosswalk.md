# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:412-417` supplies exactly the title `瑞利商定理`, attribution to
John William Strutt (Rayleigh), year 1870, the gloss `Hermite矩阵特征值的变分刻画`, importance
"medium," and status `已验证`. Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula,
definition, binder, hypothesis, conclusion, proof boundary, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:1618-1643` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof process, dependencies, alternate forms, axioms,
machine status, and artifact links open. Rev-5.6 preserves `已验证` only as untrusted source
metadata and resets the target to `L0 / rework_required`.

The literal adjective `Hermite` may be a translation or spelling error for Hermitian. That likely
interpretation is a source-review question, not authority to change the received claim silently.

## Historical attribution lead

Crossref metadata identifies J. W. Strutt, "Some General Theorems relating to Vibrations,"
*Proceedings of the London Mathematical Society*, series 1, volume 4, issue 1 (November 1871),
pages 357-368, DOI `10.1112/plms/s1-4.1.357`. This is a plausible early Rayleigh variational-method
source, but its date already differs from the catalog's 1870. Only bibliographic metadata was
inspected: publisher full text was access-controlled, and no exact matrix theorem, definitions,
premises, or proof passage was admitted. It is a historical discovery lead, not H0 evidence.

## Inspected modern proof lead

Daniel A. Spielman, *Spectral and Algebraic Graph Theory*, incomplete draft dated April 2, 2025,
was inspected from the author-hosted PDF linked in the document. The observed 400-page,
2,902,506-byte file had SHA-256
`6b70ebd45e3369754ae597a42fda8531a8cb35407d16afef65dfff509369861c`.

Chapter 2, printed page 21, defines the Rayleigh quotient of a nonzero vector for a real symmetric
matrix `M` as `x^T M x / x^T x`. Theorem 2.0.1 states, for eigenvalues ordered
`mu_1 >= ... >= mu_n`, that the largest eigenvalue is the maximum quotient and the smallest is the
minimum; it then gives the full indexed Courant-Fischer subspace formulas and extremizing
eigenvectors. Section 2.1 proves the theorem from an orthonormal eigenbasis. Theorem 2.2.1 and its
proof on printed pages 24-25 give a self-contained optimization argument that any nonzero maximizer
is a top-eigenvalue eigenvector and state that the minimum is achieved by eigenvectors of the
smallest eigenvalue. Intake does not infer a stronger full extremizer iff beyond the inspected text.

This is a complete, pinpointed modern proof lead but is not canonical or H0. It treats real
symmetric matrices, whereas the catalog likely intends complex Hermitian matrices; it combines the
two extreme cases with the separately neighboring indexed Courant-Fischer family; the author-hosted
draft is mutable; and the catalog does not cite it. Edition preservation, corrections, exact
premise/proof mapping, complex transport, target-variant selection, and independent review remain
open.

## Clause crosswalk

| Catalog/source element | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `瑞利商定理` | extremal or indexed variational characterization via a homogeneous quotient | `ContinuousLinearMap.rayleighQuotient` plus one exact source-selected `Prop` | recognizable family; exact root open |
| `Hermite矩阵` | likely a finite complex Hermitian matrix, but literal wording is unresolved | `A : Matrix n n Complex`, `A.IsHermitian`, or an approved `RCLike` generalization | source correction, scalar, index and transport open |
| `特征值` | largest/smallest or all ordered eigenvalues, with multiplicity | `Matrix.IsHermitian.eigenvalues` or `LinearMap.IsSymmetric.eigenvalues` | order, endpoints and matrix/map identity open |
| `变分刻画` | max/min quotient equality, attainment, extremizer iff, or indexed min-max | quotient over nonzero vectors/sphere or subspaces | exact extrema and conclusion open |
| Rayleigh, 1870 | historical provenance lead | source record only | exact work and catalog date unresolved |
| Spielman 2.0.1 / 2.2.1 | real-symmetric complete modern result and proof | close abstract self-adjoint APIs plus matrix transport | H1 lead; no complex/source-approved mapping |
| `已验证` | untrusted inventory field | accepted source and kernel receipts would be required | no proof credit |

## Lean discovery boundary

Pinned `Mathlib.Analysis.InnerProductSpace.Rayleigh` defines
`ContinuousLinearMap.rayleighQuotient`, equates nonzero-vector and sphere extrema, turns attained
global extrema into eigenvectors, and proves that the finite-dimensional global `iSup` and `iInf`
are eigenvalues. `Mathlib.Analysis.Matrix.Hermitian` proves
`Matrix.isHermitian_iff_isSymmetric`, bridging a finite Hermitian matrix to its Euclidean linear
map. `Mathlib.Analysis.InnerProductSpace.Spectrum` and `Mathlib.Analysis.Matrix.Spectrum` supply
decreasing eigenvalue enumerations and eigenvectors.

These interfaces closely cover one plausible extremal reading, but the `hasEigenvalue_iSup` and
`hasEigenvalue_iInf` results do not themselves identify those values with the first and last entries
of `Matrix.IsHermitian.eigenvalues`, give every extremizer iff, or state an indexed min-max theorem.
No source-selected exact conjunction or checked matrix wrapper exists at intake. The canonical
module, expression, fingerprint, alternate transports, and statement mutations remain null. No
statement elaboration, proof, audit completion, or theorem completion is claimed.

## Remaining source gate

An accountable reviewer must admit one immutable source result and incorporated definitions,
resolve the Rayleigh/1870 attribution and `Hermite` wording, select the extremal versus indexed root,
map every assumption and proof node, audit corrections, and approve any real-to-complex or
matrix-to-operator transport. An independent reviewer must repeat that check before H0 or a frozen
canonical target is possible.
