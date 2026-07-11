# THM-M-1176 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Krylov-Safonov Harnack
inequality. The manifest's historical `已验证` label is untrusted discovery
metadata and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Interior elliptic Harnack inequality for nonnegative solutions of a uniformly elliptic, nondivergence-form equation with merely measurable leading coefficients | Precise weak/strong solution class and Lean expression remain open for the statement phase |
| Geometry | A ball and a strictly interior concentric subball (provisionally `B_1` and `B_{1/2}` by rescaling) | Ball conventions, dimension assumptions, and boundary behavior must be frozen in Lean |
| Operator | `Lu = a^{ij}(x) D_ij u`, with measurable coefficients and ellipticity constants `0 < lambda <= Lambda` | Symmetry, almost-everywhere quantification, matrix representation, and optional lower-order terms are not yet credited |
| Estimate | `sup_{B_(1/2)} u <= C inf_{B_(1/2)} u`, with `C` depending only on dimension and ellipticity ratio | Essential versus pointwise extrema and regular representative require an exact analytic formulation |
| Source fidelity | Krylov-Safonov theorem family and a standard monograph formulation | Pinpoint theorem/edition, assumptions, and errata audit remain open; no `H0` claim |
| Machine surface | Lean 4 encoding of ellipticity, second derivatives, solution semantics, and extrema | No local or upstream declaration is claimed at intake |

Excluded from this root are divergence-form Harnack inequalities, the parabolic
Harnack inequality, boundary Harnack principles, nonlinear Harnack variants,
and estimates with uncontrolled lower-order coefficients. They are related
theorem families, not interchangeable statements.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first
failed theorem gate is the exact-statement gate: the source formulation and
solution semantics have not yet been frozen as an elaborated Lean expression.
No theorem completion, proof closure, or machine validation is claimed.

Validation commands and their exact scope are recorded in `validation.md`.

