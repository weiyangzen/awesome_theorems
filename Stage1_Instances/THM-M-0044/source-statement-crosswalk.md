# THM-M-0044 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:335-340` names the singular value decomposition theorem,
attributes it to Eugenio Beltrami and Camille Jordan in 1873, and states
`任意矩阵可分解为UΣV*形式`: an arbitrary matrix can be decomposed in `U Sigma V*` form. These six
catalog lines originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:1321-1349` repeats the gloss while leaving exact definitions and premises,
the proof route, equivalent statements, axiom use, formal status, and artifact links open. The
rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the item to
`L0 / rework_required`.

The corpus separately contains `THM-M-1449` (`奇异值分解`) at
`Docs/researches/math_theorems.md:10581-10586`, with the gloss `矩阵的SVD分解`, the same attribution,
year, importance, and untrusted status. This is a likely duplicate, but no identity decision has
been accepted. Its scope and evidence cannot be inherited by `THM-M-0044`.

## Human-source lead

The author-hosted current fourth-edition PDF of Sheldon Axler, *Linear Algebra Done Right*, Section
7E, was inspected on 2026-07-13. Chapter 7 declares real or complex scalars and nonzero
finite-dimensional inner product spaces. Definition 7.65 defines singular values as the
nonnegative square roots of the eigenvalues of `T* T`, with multiplicity and decreasing order.
Theorem 7.70 on printed pages 273-274 states and proves that, for `T : V -> W` with positive
singular values `s_1,...,s_m`, orthonormal lists `e_k` and `f_k` exist such that
`T v = sum_k s_k <v,e_k> f_k`. The following text extends those lists to orthonormal bases and
obtains a rectangular diagonal matrix.

This provides a strong modern proof/source lead, not `H0`. The inspected PDF is not an admitted
immutable repository source; the intake has not reconciled its nonzero-space convention with empty
matrix cases, mapped every definition and proof node, audited errata or historical priority, or
obtained independent source review. The source also states the linear-map/list form rather than the
catalog's literal `U Sigma V*` equality, so the factor orientation needs a checked crosswalk.

## Component mapping

| Catalog component | Intake-selected meaning | Pinned Lean interface | Status |
|---|---|---|---|
| "arbitrary matrix" | finite rectangular matrix over `R` or `C` | `Matrix m n k` and a corresponding finite-dimensional linear map | carrier selected provisionally; exact binders open |
| `U` | square orthogonal/unitary left factor | `Matrix.unitaryGroup m k` and orthonormal-basis matrices | interface exists; no witness construction credited |
| `Sigma` | rectangular diagonal matrix with nonnegative real diagonal entries | `Matrix`, diagonal primitives, and `LinearMap.singularValues` | components exist; exact rectangular encoding open |
| `V*` | adjoint of a square orthogonal/unitary right factor | matrix `star` / conjugate transpose | notation authenticated; factor orientation open |
| decomposition | exact matrix equality | no terminal pinned declaration located by bounded intake search | canonical elaboration and proof open |
| Beltrami/Jordan / 1873 | catalog attribution and date | no formal component | primary historical-source audit open |
| `已验证` | catalog status label | no formal component | explicitly no H/M credit |

## Pinned formal candidates

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.InnerProductSpace.SingularValues` defines `LinearMap.singularValues` for maps
between finite-dimensional `RCLike` inner product spaces. It proves nonnegativity, the square-root
relationship with eigenvalues of `T.adjoint comp T`, antitonicity, and that the support is the
initial segment determined by the range rank. The file identifies its main result as
`LinearMap.support_singularValues`; it does not claim SVD witness construction.

`Mathlib.Analysis.InnerProductSpace.Spectrum` and `Mathlib.Analysis.Matrix.Spectrum` provide
orthonormal eigenvector bases and unitary diagonalization for self-adjoint/Hermitian operators.
`Mathlib.LinearAlgebra.UnitaryGroup` and matrix star/conjugate-transpose infrastructure specify the
square unitary boundary. These are plausible prerequisites, not the arbitrary rectangular SVD.

`AnchorAudit.lean` checks eleven selected declarations and prints their axiom reports. The audited
proof-bearing prerequisites use only `propext`, `Classical.choice`, and `Quot.sound`; the elementary
Gram-matrix Hermitian lemma omits `Classical.choice`. A bounded all-package search found no pinned
declaration named or documented as singular value decomposition and no theorem concluding with both
unitary factors and a rectangular diagonal equality.

At `facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`,
`Atlas.HighDimensionalStatistics.code.Chapter4.Def_4_1` defines a Real-only compact `SVD` record and
reconstruction predicate. Its vector families carry no orthonormality conditions and no theorem
establishes existence for every matrix, so it is a statement mismatch rather than a proof anchor.

At `mrdouglasny/gaussian-field@d63a28568a75d99f6cb27af1f888a49a69855a66`,
`GaussianField.nuclear_sequence_svd` is a substantive source-level SVD-like theorem for summable
sequences into separable infinite-dimensional real Hilbert spaces. It neither covers complex finite
matrices nor constructs two square unitary matrices or the frozen rectangular equality. The project
uses Lean 4.30.0 and a different mathlib pin and was not integrated. The complete candidate and
search boundary, including blocked and result-limited public searches, is recorded in
`anchor-audit.json`; global discovery saturation is not claimed.

## Exactness risks held open

The statement phase resolved the frozen representation choices. The proof still must diagonalize
`Aᴴ A`, construct and normalize left singular vectors for positive singular values, handle the zero
tail and rank-deficient cases, complete both systems to full bases, convert them to square unitary
matrices, align the `min m n` indices with the dependent rectangular `Sigma`, prove the final
multiplication identity in the selected orientation, and cover both fields and empty dimensions.
