# THM-M-1140 rev-5.6 intake

This is the planned dossier for the strong maximum principle for harmonic functions. The terse
Stage0 phrase is interpreted as the classical real-valued Euclidean theorem: on a nonempty,
connected open domain, a harmonic function that attains an interior maximum is constant. This
interpretation must still pass source and Lean statement review.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Harmonic `u : Omega -> Real`, connected open `Omega`, attained interior maximum, global constancy | Mathematical claim frozen; Lean encoding absent |
| Domain | Finite-dimensional real Euclidean space | Dimension-zero behavior remains a statement mutation probe |
| Extremum | Global maximum at a domain point | Local-maximum formulation is only an equivalent candidate |
| Dual form | Strong minimum principle via `-u` | Requires a checked transport and is not root proof credit |
| Analytic route | Mean-value property, positivity of the averaging gap, local constancy, connected propagation | Architecture hint only; no obligation registry or proof credit |
| Exclusions | Weak boundary principle, general elliptic operators, subharmonic/manifold/discrete variants | Separate theorems; no broadened claim |
| Foundations | Lean 4 kernel and pinned mathlib | Exact imports, harmonic API, trust profile, TCB, and environment fingerprint remain open |

The structured binder order, assumptions, exclusions, and status vector are authoritative in
`intake.json`. Source wording and candidate formal surfaces are crosswalked in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed gate is exact
statement identification: the repository has no selected Lean declaration/expression, elaboration
hash, environment fingerprint, or checked encoding transport. No machine closure or theorem
completion is claimed.

## Validation

`validation.md` records the intake-only structural checks. They validate manifest membership,
repository consistency, JSON syntax, and dossier hygiene, not the theorem in the Lean kernel.
