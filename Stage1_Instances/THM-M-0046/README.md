# THM-M-0046 rev-5.6 intake

This directory is the fail-closed `planned` dossier for the catalog item named the QR
decomposition theorem. The repository says that a matrix is a product of an orthogonal matrix and
an upper-triangular matrix, attributes the result to Alston Householder in 1958, and labels it
verified. Those are uncited inventory fields. Under rev-5.6 they are not an admitted human source,
an exact Lean proposition, or proof evidence.

## Planned scope

The conventional finite-dimensional QR family is preserved for source review: a real or complex
matrix is expressed as `A = Q * R`, where `Q` has orthonormal columns or is square
orthogonal/unitary and `R` is upper triangular or upper trapezoidal. This description is not a
frozen proposition. The catalog does not specify the scalar field, matrix shape, rank hypothesis,
full versus reduced factorization, factor dimensions, complex-unitary convention, diagonal
normalization, uniqueness, or empty-dimensional cases.

Sheldon Axler's author-hosted *Linear Algebra Done Right*, fourth edition, was inspected as a modern
source lead. Theorem 7.58 on printed page 264 proves existence and uniqueness for a square real or
complex matrix with linearly independent columns: `Q` is unitary, `R` is upper triangular with
positive diagonal, and `A = Q R`. This is a strong disambiguating proof source, but it is not cited
by the catalog, is narrower than an unqualified arbitrary-matrix reading, and has not been admitted
as an immutable source or independently reviewed. It supports provisional `H1`, not `H0`.

## Formal boundary

Pinned mathlib provides Gram-Schmidt orthogonalization, normalized orthonormal systems and bases,
triangular coefficient results, unitary matrices, and upper-triangular predicates. In particular,
`InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular` is a close ingredient. A bounded
intake search found no declaration named or documented as QR decomposition or QR factorization.
`IntakeProbe.lean` authenticates adjacent interfaces only; it neither declares the target nor gives
root proof credit.

The provisional vector is `[H1, M3, R3]`: a complete modern proof source lead was inspected but
source fidelity remains unaccepted; substantial formal prerequisites exist but no exact terminal QR
declaration is credited; and the dossier maps scope without reconstructing the proof. All six
downstream phases remain open. No accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
