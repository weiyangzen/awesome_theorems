# THM-M-1453 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `Arnoldi迭代`
(Arnoldi iteration). The repository supplies only the gloss `非对称矩阵的特征值` ("eigenvalues
of nonsymmetric matrices"), attributes the item to Walter Arnoldi in 1951, and labels it
`已验证`. An algorithm name and intended application do not form a truth-valued proposition with
ordered binders, hypotheses, and a conclusion. The verified label is untrusted metadata and gives
neither source nor proof credit.

Arnoldi iteration can refer to construction of an orthonormal Krylov basis, the Hessenberg
decomposition relation, Ritz-pair residual identities, exactness after lucky breakdown, an
eigenvalue-approximation result, a convergence bound, a restarted variant, or a floating-point
stability result. The catalog selects none of these. It also does not fix the coefficient field,
matrix dimension, start vector, breakdown policy, number of iterations, orthogonalization variant,
eigenvalue selection, convergence notion, or arithmetic model. Choosing one would invent
proposition-changing mathematics.

The Netlib *Templates for the Solution of Algebraic Eigenvalue Problems* Arnoldi chapter was
inspected as a strong modern specification lead. Its basic-algorithm section distinguishes several
claims: the generated vectors form an orthonormal basis of a Krylov subspace, they satisfy the
Arnoldi/Hessenberg relations, and breakdown has an invariant-subspace/exact-Ritz interpretation.
The chapter separately describes Arnoldi as an eigenvalue approximation method. These distinctions
confirm the unresolved root choice. The catalog does not cite this source, and its web edition has
not been admitted as immutable evidence or independently reviewed.

The provisional vector is `[H5, M4, R4]`. `H5` classifies the catalog method gloss as not yet a
stable proposition; it does not refute established Arnoldi theorems. The pinned probe authenticates
Gram-Schmidt, span, orthonormality, linear-map power, and matrix representation interfaces only.
All downstream phases remain open. No canonical statement, target proof, accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
