# THM-M-1192 rev-5.6 intake

This directory is the `planned` instance for the source label “Gaussian upper bound” in the
differential-equations / PDE category. The only inherited mathematical wording is “a Gaussian-type
upper bound for the heat kernel.” That phrase names a family of theorems, not one proposition: it
does not identify the operator, space, coefficient assumptions, kernel normalization, boundary
conditions, or constants. Intake therefore fails closed rather than silently substituting a
convenient theorem.

## Scope map

| Surface | Candidate scope | Intake boundary |
|---|---|---|
| Exact root | A Gaussian upper estimate for a heat/fundamental kernel | No exact root is frozen |
| Classical PDE candidate | Aronson's upper estimate for the fundamental solution of a uniformly parabolic divergence-form equation on `R^n` | Primary candidate only; selecting it requires source-owner confirmation or stronger repository provenance |
| Elementary candidate | The explicit Euclidean Laplacian kernel `(4 pi t)^(-n/2) exp(-|x-y|^2/(4t))` | Strictly narrower and must not be substituted |
| Geometric variants | Heat kernels on Riemannian manifolds under curvature/volume hypotheses | Different hypotheses and conclusions; excluded until selected |
| Domain variants | Dirichlet/Neumann heat kernels | Boundary and regularity assumptions are absent |
| Lean surface | A proposition in Lean 4 with pinned minimal imports | Deferred to `S56-M-1192-STATEMENT`; no declaration is claimed |
| Foundations | Lean 4 kernel plus an accepted foundation/TCB profile | Cannot be frozen before the analytic model |

The candidate Aronson shape is
`Gamma(x,t;xi,tau) <= C (t-tau)^(-n/2) exp(-c |x-xi|^2/(t-tau))` for `t > tau`,
with constants controlled by dimension, ellipticity, coefficient bounds, and the time horizon.
This formula is orientation only and is deliberately not recorded as the canonical statement.

## Open task DAG

1. `SCOPE-1`: identify the intended theorem family from primary provenance.
2. `SCOPE-2`: pin an edition and map every coefficient, ellipticity, regularity, domain, time, and constant assumption.
3. `STMT-1`: encode the selected operator, fundamental solution, Gaussian expression, and constant dependencies in Lean.
4. `STMT-2`: elaborate the exact target, fingerprint the environment, and mutation-test dropped hypotheses and boundary cases.
5. `AUDIT-1`: only after statement freeze, search mathlib and external Lean artifacts without awarding anchor-only proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed gate is exact
source-statement identification. The retry condition is authoritative selection of one theorem
family plus its complete assumptions. No theorem-completion or machine-proof claim is made.

## Validation

The commands and exact results in `validation.md` establish target membership, standard consistency,
JSON syntax, and dossier-local structural checks only.
