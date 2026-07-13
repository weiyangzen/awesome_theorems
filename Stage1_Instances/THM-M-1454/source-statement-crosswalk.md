# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10616-10621` supplies exactly the title `GMRES`, attribution to
Yousef Saad and Martin Schultz, the year 1986, the gloss `广义最小残差法` (`generalized minimal
residual method`), importance "high," and status `已验证`. Git history places all six uncited fields
in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no source, mathematical
definitions, binders, hypotheses, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:39541-39566` repeats the gloss while leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 target manifest retains `已验证` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

## Inspected primary source

Youcef Saad and Martin H. Schultz, "GMRES: A Generalized Minimal Residual Algorithm for Solving
Nonsymmetric Linear Systems," *SIAM Journal on Scientific and Statistical Computing* 7(3), July
1986, pages 856-869, DOI `10.1137/0907058`, was inspected through a Stanford-hosted scan. The scan
has SHA-256 `4e90d7387751887455ee519208e83d8f40dc4b8972e4ea382d9a51e7c7db387d`.
It is a primary source lead, not repository-owned or independently accepted evidence.
The publication spells the first author's name `Youcef`; the repository catalog says `Yousef`.

The paper contains several distinct formalizable targets:

- Abstract and Section 3.1, equations (3)-(8): the `k`th approximation minimizes the residual norm
  over the affine Krylov space and the large least-squares problem reduces to a Hessenberg problem.
- Proposition 1, page 862: a rotated Hessenberg right-hand-side component gives the residual norm.
- Proposition 2, page 865: exactness at step `j`, Arnoldi breakdown, vanishing next vector and
  Hessenberg subdiagonal, and the minimal-polynomial degree condition are equivalent.
- Corollary 3, page 865: an `N x N` unrestarted GMRES problem terminates in at most `N` steps.
- Proposition 4, Theorem 5, and Corollary 6, pages 866-867: conditional residual bounds and
  convergence criteria for restarted GMRES(m).

The same page that states Corollary 3 warns that restarted GMRES need not converge and gives a
GMRES(1) stationary example. Consequently, `GMRES` cannot truthfully be expanded into an
unconditional convergence slogan. The repository does not identify any one of these results as its
canonical proposition. No source is accepted as `H0`, and independent source review remains open.

## Component crosswalk

| Catalog component | Primary-source alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "GMRES" | Algorithm 3 or restarted Algorithm 4 | source-faithful iteration data and invariants | algorithm version and root claim open |
| "generalized" | nonsymmetric real `N x N` systems derived from Arnoldi rather than symmetric MINRES | `Matrix (Fin N) (Fin N) R` or a finite-dimensional operator | scalar and representation open |
| "minimal residual" | minimize `||f - A(x0 + z)||` over `z in K_k`; reduce via `A V_k = V_(k+1) H_k` | norm, affine subspace, finite least squares, isometric basis map | existence, uniqueness, and chosen minimizer open |
| termination | lucky breakdown is exact; at most `N` unrestarted steps | Krylov stabilization and minimal-polynomial degree | cannot be transferred to arbitrary restart length |
| convergence | conditional positive-real or spectral bounds | eigenvalue, diagonalization, polynomial and norm bounds | hypotheses and exact result open |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | no H or M credit |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks matrix-vector linear maps, Gram-Schmidt orthogonality and span preservation,
finite-dimensional orthogonal projection, norm-preserving maps, and dot products. A bounded
case-insensitive search for `GMRES` and `generalized minimal residual` found no exact-topic theorem
in pinned mathlib or the repo-local Lean tree. This does not establish global absence and is not the
later immutable external anchor audit.

Before leaving `H1`, accountable reviewers must choose one primary-source proposition, transcribe
all definitions and hypotheses it incorporates, audit corrections, resolve algorithm-version and
exact-arithmetic boundaries, and independently approve the catalog mapping. Only then may the
statement phase freeze minimal imports, an elaborated expression, checked transports, and the
required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
