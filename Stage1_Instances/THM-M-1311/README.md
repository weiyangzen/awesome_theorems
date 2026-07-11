# THM-M-1311 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Choquet-Bruhat local-existence theorem for
the vacuum Einstein equations. The repository's older label, "Einstein equations have local
solutions," is only a discovery description: it is not yet an exact formal statement and carries
no proof credit.

## Scope map

| Surface | Intended scope | Boundary at intake |
|---|---|---|
| Exact root | Local-in-time existence for the vacuum Einstein Cauchy problem from suitable initial data satisfying the constraint equations | Regularity, gauge, topology, uniqueness, and geometric-equivalence clauses require primary-source audit before the statement is frozen |
| Initial data | A three-dimensional spatial manifold with a Riemannian metric and second fundamental form satisfying the vacuum constraints | Sobolev/smooth class and sign conventions remain open |
| Gauge reduction | Harmonic-coordinate reduction of the Einstein equations to a quasilinear hyperbolic system | Architecture only; no reduction lemma is credited |
| PDE engine | Local existence for the reduced hyperbolic Cauchy problem and propagation of the gauge/constraints | Architecture only; no Lean candidate or proof body is credited |
| Geometric output | A spacetime development inducing the supplied initial data, locally solving `Ric(g) = 0` | The distinct maximal globally hyperbolic development theorem (THM-M-1312) is excluded |
| Foundations | Lean 4 kernel plus a future pinned mathlib environment and an explicit classical/choice/quotient policy | No environment or dependency fingerprint exists in this phase |

The canonical human claim and its unresolved parameters are structured in `intake.json`. Source
genealogy and the statement-component audit are recorded in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact-source/statement gate: the broad historical result has been identified, but an exact
edition/page/theorem formulation, assumptions, errata check, and canonical Lean expression have not
been accepted. This intake neither elaborates nor proves a Lean theorem.

## Validation

The commands in `validation.md` establish manifest membership, repository-standard consistency,
JSON syntax, and dossier-local reference integrity only. Master acceptance and every dependent
phase remain outstanding.
