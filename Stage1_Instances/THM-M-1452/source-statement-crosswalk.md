# THM-M-1452 source-statement crosswalk

## Repository record

The source inventory at `Docs/researches/math_theorems.md:10602-10607` says only:

```text
Lanczos算法
提出者: Cornelius Lanczos
时间: 1950
陈述: 大型稀疏矩阵的特征值
重要性: 高
形式化状态: 已验证
```

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; there is no citation, theorem locator, formula, or
proof. The Stage0 projection at `Docs/Stage0_Blueprint.md:39487-39512` explicitly leaves exact
definitions and premises, proof, equivalent statements, axioms, machine state, and artifacts as
`待补充`. The generated target manifest adds scheduling metadata but no mathematical evidence.

## Primary-source lead

C. Lanczos, "An Iteration Method for the Solution of the Eigenvalue Problem of Linear Differential
and Integral Operators," *Journal of Research of the National Bureau of Standards* 45(4), October
1950, Research Paper 2133, pages 255-282, DOI `10.6028/jres.045.026`, is a credible primary-source
lead. The observed official NIST PDF had SHA-256
`ca3f1012cb385d8060b0779b39df745dea2c922b695f383bdd4cfd8e61ecfc4b` and 28 pages; it was inspected
but was not added to the repository.

Section VII, printed pages 265-269, develops "minimized iterations." For symmetric `A`, equation
(63) states `A* = A`; equations (64)-(75) describe successive orthogonal vectors and a recurrence in
which each new step uses two correction terms. The paper then treats nonsymmetric matrices with a
biorthogonal construction. Section XIV, printed page 281, summarizes evaluation of latent roots and
principal axes. The paper contains analysis, algorithms, examples, numerical discussion, and
operator extensions rather than one numbered theorem identical to the catalog gloss. The gloss's
words "large sparse matrix" are a modern computational characterization, not a quoted proposition
from this source.

The PDF URL is mutable, no lawful immutable preservation or correction audit is recorded, no exact
source theorem has been selected, and no independent reviewer has approved a binder-by-binder or
node-by-node mapping. The lead therefore does not establish H0.

## Clause crosswalk

| Catalog or source component | Required exact statement component | Intake status |
|---|---|---|
| `Lanczos算法` | select exact, block, restarted, look-ahead, or finite-precision algorithm | unspecified |
| `矩阵` | scalar field, finite dimensions, square shape, and Hermitian/symmetric premise | unspecified |
| `大型` | formal dimension threshold or complexity/storage model | no mathematical meaning supplied |
| `稀疏` | sparsity predicate and preservation/cost conclusion, or explicit nonsemantic motivation | unspecified |
| `特征值` | exact output: all eigenvalues, Ritz values, extremal approximations, or residual bounds | unspecified |
| 1950 paper section VII | start vector, recurrence, coefficients, nonbreakdown hypotheses, orthogonality, and termination | source lead only; not selected |
| recurrence claim | exact matrix/vector identity and indexing | equations exist, but no admitted proposition crosswalk |
| numerical motivation | arithmetic model, norm, error, convergence, and stopping rule | unspecified and not kernel evidence |
| `已验证` | accepted source and kernel receipts | untrusted label; no H/M credit |

## Prospective Lean surface

A future exact statement will likely need `Matrix (Fin n) (Fin n) k`, `Matrix.IsHermitian`,
matrix-vector multiplication, inner products, orthonormal families or bases, spans of iterates, and
a tridiagonal predicate or explicit band equation. Pinned Hermitian spectral and Gram-Schmidt APIs
are ingredients only. They neither define the Lanczos algorithm nor bridge any one candidate family
to the catalog wording.

## Neighbor and substitution boundary

Arnoldi is separately cataloged as `THM-M-1453`; it may generalize a Krylov orthogonalization route
to nonsymmetric matrices but transfers no statement or proof credit. Power iteration, QR iteration,
GMRES, and conjugate gradients also own distinct repository targets. The word `Krylov` in the
repo-local diffusion and elliptic-estimate artifacts denotes unrelated analysts, not a Krylov
subspace or Lanczos implementation.

## First source gate

Before statement work, reviewers must select and lawfully preserve an immutable source proposition,
record edition/article/section/page/formula locators and corrections, map every ordered binder,
hypothesis, definition, conclusion, and boundary case, reconcile the catalog's large/sparse wording
with the chosen mathematical theorem, and approve the mapping independently. Only then may the
statement phase elaborate and mutation-test an exact Lean target. Until that happens, the correct
classification is a planned H5/M4/R4 intake with no proof credit.
