# THM-M-1453 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10609-10614` supplies exactly the title `Arnoldi迭代`, attribution
to Walter Arnoldi, year 1951, gloss `非对称矩阵的特征值`, high importance, and status `已验证`. All
six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
algorithm, ordered binders, hypotheses, conclusion, proof, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:39514-39539` repeats the gloss while explicitly leaving the target formal
system, foundations, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. Its generic closed-result and leaf-audit language
is planning metadata, not source evidence. Rev-5.6 retains `已验证` only as untrusted metadata and
resets the target to `L0 / rework_required`.

## Inspected specification lead

The Arnoldi Method chapter by Yousef Saad in *Templates for the Solution of Algebraic Eigenvalue
Problems: A Practical Guide*, edited by Zhaojun Bai, James Demmel, Jack Dongarra, Axel Ruhe, and
Henk van der Vorst, SIAM, 2000, was inspected through the Netlib HTML edition on 2026-07-13.
Sections "Arnoldi Method" and "Basic Algorithm" were observed with SHA-256 digests
`ef995d676bc6e07a06a3684b0936dae53f9aa41ebff47ab13f4cf323d82fddbe` and
`f075d2f07bb23d136f9f047add18ccb25fc6f0115cc3b395eebb401ed4cc95e1` respectively.

The chapter says the method was introduced as a direct reduction of a general matrix to upper
Hessenberg form and later used iteratively to approximate eigenvalues of large sparse
non-Hermitian matrices. Its basic algorithm constructs an orthonormal basis of
`K_m(A,v)`, derives `A v_j = sum_(i=1)^(j+1) h_ij v_i`, and states the matrix relations
`A V_m = V_m H_m + h_(m+1,m) v_(m+1) e_m*` and `V_m* A V_m = H_m`. It separately states that
breakdown corresponds to an invariant Krylov subspace and exact approximate eigenvalues and
eigenvectors under its conditions.

This is a strong modern family/specification lead, not `H0`. The catalog does not cite it or select
one of its distinct claims. No lawfully preserved immutable edition, correction/errata audit,
complete incorporated-definition mapping, source-to-obligation crosswalk, or independent review
has been accepted.

Crossref metadata for DOI `10.1090/qam/42792` independently locates W. E. Arnoldi, "The principle
of minimized iterations in the solution of the matrix eigenvalue problem," *Quarterly of Applied
Mathematics* 9 (1951), 17-29. The observed Crossref response had SHA-256
`a50b805e8ea81602545f593c4e16bbaa34242f869c5c87474f3871352a0ba78b`. The primary article body
was not inspected in this run, so its propositions, assumptions, proof, and corrections receive no
`H0` credit.

## Literal crosswalk

| Repository element | Source-family component | Prospective Lean component | Intake result |
|---|---|---|---|
| `非对称矩阵` | square real or complex general/non-Hermitian matrix | `Matrix (Fin n) (Fin n) Real` or `Complex`, or an endomorphism | field, dimension, and meaning of nonsymmetry absent |
| iteration | repeated multiplication and orthogonalization | powers of an endomorphism plus `gramSchmidtNormed` | start, count, variant, and breakdown policy absent |
| Krylov basis | orthonormal basis for span of `v, A v, ..., A^(m-1) v` | spans of a finite vector family and `Orthonormal` | plausible component, not catalog-selected |
| Hessenberg relation | recurrence and the `A V_m` residual identity | matrix multiplication, conjugate transpose, finite sums | shapes, indexing, coefficients, and conclusion absent |
| eigenvalues | Ritz values/eigenvectors of projected `H_m` | eigenvalue predicates or characteristic polynomials | exactness, residual, convergence, and selection absent |
| breakdown | invariant Krylov subspace and exact Ritz data | invariant-submodule and zero-residual predicates | catalog does not mention this branch |
| `已验证` | untrusted screening label | accepted source and kernel receipts | no H or M credit |

The literal record therefore cannot populate the canonical domain, ordered quantifiers,
hypotheses, conclusion, alternate encodings, boundary exclusions, or expression fingerprint.

## Pinned Lean crosswalk

| Candidate | What is checked | Why it is not the target |
|---|---|---|
| `InnerProductSpace.gramSchmidt_orthogonal` | Gram-Schmidt outputs are mutually orthogonal at distinct indices | no Krylov input, normalization, recurrence, or eigenvalue claim |
| `InnerProductSpace.span_gramSchmidt` | Gram-Schmidt preserves the span of an indexed family | no identification with powers of the selected operator is frozen |
| `InnerProductSpace.gramSchmidt_ne_zero` | independent inputs produce nonzero orthogonalized vectors | breakdown and Krylov independence are not modeled |
| `InnerProductSpace.gramSchmidtNormed_orthonormal` | normalized outputs are orthonormal under linear independence | only the orthogonalization ingredient |
| `LinearMap.toMatrix_mulVec_repr` | a linear map's matrix acts on coordinate vectors as expected | representation interface, not Arnoldi construction |
| `LinearMap.toMatrix_comp` and `LinearMap.toMatrix_pow` | matrix representation respects composition and powers | power substrate only; no Krylov span or projection result |

A bounded exact-topic search found no source-selected terminal Arnoldi theorem in pinned mathlib or
repo-local Lean. This is discovery evidence only and is not a global absence proof or the required
immutable external-project anchor audit. `IntakeProbe.lean` checks the named adjacent APIs without
declaring a target or proof body.

## Source gate

The first downstream gate requires an accountable correction that selects an immutable source
edition and one exact truth-valued proposition; maps every definition, binder, premise, conclusion,
algorithm step, breakdown branch, boundary case, and proof node; distinguishes exact-arithmetic
correctness from convergence and floating-point behavior; reconciles the Lanczos, power, QR, and
GMRES neighbor boundaries; audits corrections; and receives independent source and numerical-
linear-algebra review. Only then may the statement phase freeze a Lean expression, minimal imports,
checked transports, and required statement mutations.

Until that correction exists, `H5` describes the catalog target's ill-posed proposition status,
`M4` records the absence of a source-identical usable formal artifact, and `R4` records the absence
of an anchorable reconstruction. These classifications do not say that standard Arnoldi results
are false or mathematically open.
