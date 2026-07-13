# THM-M-1455 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10623-10628` supplies exactly the title `共轭梯度法`, attribution
to Magnus Hestenes and Eduard Stiefel, the year 1952, the gloss `对称正定系统的迭代解法`
("iterative solution method for symmetric positive-definite systems"), importance "high," and
status `已验证`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no source locator, definitions,
ordered binders, hypotheses, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:39568-39593` repeats the gloss while leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine state, and artifact links open. The rev-5.6 target manifest retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

## Inspected primary source

Magnus R. Hestenes and Eduard Stiefel, "Methods of Conjugate Gradients for Solving Linear Systems,"
*Journal of Research of the National Bureau of Standards* 49(6), December 1952, Research Paper
2379, pages 409-436, DOI `10.6028/jres.049.044`, was inspected through the official NIST scan. The
observed 28-page PDF has SHA-256
`0b5d99551f4aa0a960d85a8b699d7c669d91aeff0a312470bdf531d64e755262`. It is a primary-source
lead, not repository-owned or independently accepted evidence.

The paper contains several distinct formalizable targets:

- Abstract and Section 3, printed pages 409-412: a recurrence for solving `A x = k`, with solution
  in at most `n` steps when no rounding error occurs; formulas (3:1) give the symmetric
  positive-definite routine.
- Theorem 5:1, printed page 414: the residuals are mutually orthogonal and the direction vectors
  are mutually conjugate.
- Theorem 5:2, printed page 415: the conjugate-gradient method is a special conjugate-directions
  method, with a converse under stated qualifications.
- Theorem 6:1, printed page 416: each estimate minimizes the quadratic error functional on the
  generated affine plane and gives an exact decrement formula.
- Theorems 6:2-6:3 and later sections: additional Euclidean-error, geometric, polynomial, and
  rounding-error properties.

The introduction and Section 3 distinguish exact termination from actual rounded computation and
also discuss nonsymmetric extensions. The repository gloss narrows attention to symmetric
positive-definite systems but does not choose a result, recurrence version, arithmetic model, or
conclusion. No source is accepted as `H0`; correction review and independent source review remain
open.

## Component crosswalk

| Catalog component | Primary-source alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| conjugate gradient | formulas (3:1), Theorems 5:1-5:2, or later equivalent routines | source-faithful iteration data and recurrence | root and recurrence convention open |
| symmetric | real transpose symmetry in Section 2 | `Matrix.IsHermitian` over `Real`, or a symmetric linear map | scalar/representation open |
| positive definite | `(x, A x) > 0` for nonzero `x` | `Matrix.PosDef` and dot-product characterization | exact predicate/domain open |
| linear system | `A x = k`, solution `h`, residual `k - A x` | matrix-vector equation, invertibility, residual definition | binders and solution representation open |
| iterative solution | finite termination, invariant claims, minimization, or error reduction | finite sequences, recurrence, Krylov subspaces, energy norm | exact conclusion open |
| `已验证` | untrusted inventory label | no Lean proposition or proof object | no H or M credit |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only
probe checks `Matrix.PosDef`, its Hermitian, quadratic-form, and invertibility consequences, and
matrix-vector linear-map interfaces. A bounded case-insensitive search for conjugate-gradient and
CG-method names found no exact-topic theorem in pinned mathlib or the repo-local Lean tree. These
ingredients do not define the recurrence or prove any source result. The bounded search is not the
later immutable external anchor audit.

`THM-M-1503` separately catalogs `共轭梯度法(优化)` for large-scale unconstrained optimization.
Its nonlinear optimization family cannot be used as a synonym, source, statement, or proof for
this symmetric positive-definite linear-system target.

Before leaving `H5`, accountable reviewers must choose one primary-source proposition, transcribe
every incorporated definition and hypothesis, audit corrections, resolve recurrence and
exact-arithmetic boundaries, and independently approve the catalog mapping. Only then may the
statement phase freeze minimal imports, an elaborated expression, checked transports, and the
required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
