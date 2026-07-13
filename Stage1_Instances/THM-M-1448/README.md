# THM-M-1448 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `QR分解` (QR
decomposition). The repository gives only the gloss `矩阵的正交三角分解` ("an orthogonal-triangular
factorization of a matrix"), attributes it to Alston Householder in 1958, and labels it `已验证`.
Those are uncited inventory fields. Under rev-5.6 they are not an admitted source statement, an
exact Lean proposition, or proof evidence.

## Planned scope

The conventional finite-dimensional QR family is preserved for source review: a real or complex
matrix is expressed exactly as `A = Q * R`, where `Q` is square orthogonal/unitary or has
orthonormal columns, and `R` is upper triangular or upper trapezoidal. This is a family description,
not a frozen proposition. The catalog does not specify the scalar field, shape, rank hypothesis,
full versus reduced factorization, factor dimensions, diagonal normalization, uniqueness, or
empty-dimensional cases.

Sheldon Axler's author-hosted *Linear Algebra Done Right*, fourth edition, was inspected as an
authoritative modern lead. Theorem 7.58 on printed page 264 proves existence and uniqueness for a
square real or complex matrix with linearly independent columns: `Q` is unitary, `R` is upper
triangular with positive diagonal, and `A = Q R`. This is a complete disambiguating proof source,
but it is not cited by the catalog, is narrower than an unqualified arbitrary-matrix reading, and
has not been admitted as immutable source evidence or independently reviewed. It supports
provisional `H1`, not `H0`.

Pinned mathlib supplies Gram-Schmidt orthogonalization, normalized orthonormal systems and bases,
triangular coefficient results, unitary matrices, and upper-triangular predicates. In particular,
`InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular` is a close ingredient. A bounded
intake search found no declaration named or documented as QR decomposition or QR factorization.
`IntakeProbe.lean` authenticates adjacent interfaces only; it neither declares the target nor gives
root proof credit.

The repository also contains `THM-M-0046`, a likely duplicate with a more explicit QR gloss. That
target's dossier and status are read-only discovery inputs here, not shared evidence. Identity and
scope reconciliation remains a master decision.

The provisional vector is `[H1, M3, R3]`: a complete modern proof lead was inspected but source
fidelity is unaccepted; substantial formal prerequisites exist but no exact terminal QR
declaration is credited; and this dossier maps scope without reconstructing the proof. All six
downstream phases remain open. No exact Lean target, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
