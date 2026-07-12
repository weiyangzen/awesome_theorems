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

`IntakeProbe.lean` checks selected types and prints axiom reports for singular-value support and the
Hermitian matrix spectral theorem. A bounded exact-topic search found no pinned declaration named
or documented as singular value decomposition and no theorem concluding with both unitary factors
and a rectangular diagonal equality. That negative observation is an intake lead only, not an
exhaustive anchor audit or `M4` claim.

## Exactness risks held open

The statement phase must resolve real versus complex polymorphism, rectangular index conventions,
full versus thin factor shapes, transpose versus conjugate transpose, the precise rectangular
diagonal predicate, nonnegative-real embedding, ordering and multiplicity, empty dimensions, and
the matrix/linear-map direction. Singular values alone, or spectral diagonalization of `Aᴴ A`, do
not supply the catalog conclusion without constructing left singular vectors, completing bases,
and checking the final multiplication identity.
