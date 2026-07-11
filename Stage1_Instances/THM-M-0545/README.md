# THM-M-0545: Hodge decomposition theorem

## Intake status

`S56-M-0545-INTAKE` is a planned rev-5.6 instance. The source metadata says only
"decomposition of differential forms". This dossier conservatively fixes the analytic Hodge
decomposition on a compact oriented Riemannian manifold: each smooth complex-valued differential
form is uniquely the sum of a harmonic form, an exact form, and a coexact form.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Space | finite-dimensional smooth compact oriented Riemannian manifold without boundary | manifolds with boundary and noncompact variants are excluded |
| Forms | smooth complex-valued differential `k`-forms, for every natural `k` | Sobolev completions and distributional forms are implementation details, not separate claims |
| Operators | exterior derivative `d`, its metric adjoint `delta`, and Hodge Laplacian | construction and analytic properties remain open obligations |
| Decomposition | unique orthogonal sum `omega = h + d alpha + delta beta`, with `Delta h = 0` | no Lean expression or proof is credited at intake |
| Cohomology corollary | harmonic representatives identify with de Rham cohomology | the compact-Kahler bidegree decomposition and Hodge conjecture are different targets |
| Boundary degrees | degree zero and degrees above the dimension remain included | eventual definitions must handle vanishing summands rather than silently exclude them |

## Open phase DAG

The dependent phases are statement elaboration, immutable source and Lean anchor audit, frozen
obligation graphs, proof implementation/integration, validation, and release. Intake supplies no
credit to any dependent node.

## Status boundary

Lifecycle is `planned`. The provisional root vector is `[H3, M3, R3]`: the repository has no
pinpoint primary-source record, the exact Lean statement is unelaborated, and no reviewed readable
reconstruction exists. This dossier does not claim audit completion, proof completion, or theorem
completion. Worker evidence is not master acceptance.

