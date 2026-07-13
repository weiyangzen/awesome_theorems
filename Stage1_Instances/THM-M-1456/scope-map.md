# THM-M-1456 scope map

## Catalog scope preserved

- Target identity: `THM-M-1456`, named `预处理技术` (preconditioning techniques).
- Catalog attribution and date: many mathematicians, twentieth century.
- Literal gloss: `加速迭代收敛的技术` (techniques for accelerating iterative convergence).
- Subject boundary: transformations or auxiliary solves used with iterative methods in numerical
  analysis.

This is all the mathematical scope fixed by the repository. It does not determine a proposition.

## Decisions required before statement freeze

An approved target correction must select one immutable source proposition and freeze:

1. The problem class: finite linear system, operator equation, nonlinear equation, eigenproblem,
   or optimization problem.
2. The coefficient domain, dimensions or spaces, matrix/operator representation, normed or inner
   product structure, and all universe and finiteness assumptions.
3. The iterative method and recurrence: stationary/Richardson, CG, GMRES, another Krylov method,
   nonlinear iteration, or a source-specified algorithm.
4. The preconditioner object and action: exact or approximate inverse, left, right, split, or
   symmetric placement, and whether applying it is itself an exact solve or an algorithm.
5. Invertibility, symmetry, positive-definiteness, spectral-equivalence, sparsity, regularity, and
   compatibility hypotheses on the original problem and preconditioner.
6. The convergence observable: error or residual norm, energy norm, spectral radius, condition
   number, eigenvalue clustering, asymptotic factor, iteration count, operation count, or wall time.
7. The comparator and quantifier order: unpreconditioned method versus another preconditioner,
   initial points and right-hand sides, tolerance, strict versus weak improvement, and uniform or
   instance-specific bounds.
8. Exact versus floating-point arithmetic, setup and application costs, stopping rule, breakdown
   behavior, ordered binders, conclusion, boundary cases, and every credited alternate encoding.

These choices change truth conditions and proof obligations. They are a resolution checklist, not
a canonical claim.

## Candidate theorem families not credited

- Solution equivalence of `A x = b` and `M^-1 A x = M^-1 b` when `M` is invertible.
- A stationary iteration converges when a source-specified iteration matrix has spectral radius
  less than one, together with the effect of a selected transformation.
- An SPD preconditioned-CG error estimate in terms of the condition number of a transformed
  operator.
- A theorem for a specific Jacobi, SSOR, incomplete LU/Cholesky, domain-decomposition, polynomial,
  or multigrid preconditioner.
- An implementation theorem balancing setup/application work against iteration count or runtime.

None is selected, stated, or credited at intake. The elementary equivalence lemma alone would not
prove accelerated convergence.

## Boundary and degenerate cases

The statement phase must resolve identity and scalar-multiple preconditioners, exact `M = A`,
singular or indefinite preconditioners, zero and identity systems, empty and one-dimensional
spaces, inconsistent or nonunique systems, already-convergent and divergent iterations, zero
residual at the initial point, breakdown, equality rather than strict improvement, and a poor
preconditioner that worsens the chosen metric. It must say whether setup and inner-solve work count.

The identity preconditioner gives no strict acceleration in the usual comparison. Exact `M = A`
can move the entire solve into applying the preconditioner. These cases are enough to prohibit an
unsourced universal reading of the catalog slogan.

## Explicit exclusions

- `THM-M-1455` conjugate gradients, `THM-M-1454` GMRES, and `THM-M-1457` multigrid are separate
  roots. They may become dependencies of a selected theorem but share no status or proof credit.
- Matrix invertibility, positive definiteness, norm submultiplicativity, a fixed-point limit, or
  solution equivalence alone is substrate, not an acceleration theorem.
- A theorem that assumes the desired convergence improvement, spectral bound, or iteration-count
  reduction as a hypothesis does not construct or justify it.
- A fixed numerical example, floating-point experiment, residual plot, or timing benchmark cannot
  substitute for a source-selected theorem.
- The catalog label `已验证`, a theorem-name match, or a successful `#check` supplies no H or M
  credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib exposes matrix inverse cancellation,
matrix-vector multiplication, positive-definite matrices and inverses, entrywise operator-norm
bounds, and generic fixed-point limits. A bounded exact-topic search found no numerical
preconditioner, condition-number, or iterative-solver theorem matching the catalog. These are
intake discovery facts only, not a complete anchor audit or a global absence claim.
