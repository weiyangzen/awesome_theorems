# THM-M-0995 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the one-sided Bernstein inequality for a
finite sum of independent, centered, almost-surely bounded real random variables. Historical
Stage0 wording and the legacy `S1_M_275.lean` module are discovery inputs only; neither supplies
accepted statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Upper-tail bound `P(sum X_i >= t) <= exp(-t^2/(2(v + b*t/3)))`, for `t >= 0` | Canonical elaboration and expression hash belong to the statement phase |
| Random variables | A finite indexed family of real-valued variables on one probability space | Measurability, square integrability, centering, and mutual independence are explicit |
| Bounds | Common almost-sure bound `abs (X_i) <= b`, and `sum Var(X_i) <= v` | `b >= 0` and `v >= 0`; zero and denominator-degenerate cases require statement-phase probes |
| Tail variants | One-sided upper tail only | Lower-tail, two-sided, scalar-weighted, martingale, and unbounded moment-condition variants are excluded |
| Candidate Lean surface | legacy `AwesomeTheorems.Stage1.S1_M_275.StatementShape` | Unaccepted and not imported into this dossier |
| Foundations | Lean 4 kernel and pinned mathlib | Exact toolchain, imports, axioms, and TCB remain open |

The source phrase "tail probability of a sum" is under-specified. This intake selects the classical
bounded-summand form already documented by the repository, rather than silently claiming every
result called a Bernstein inequality. The structured claim and exclusions are in `intake.json`;
the source relationship and unresolved fidelity work are in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The first failed theorem gate is
the exact-statement gate: no canonical Lean elaboration, normalized expression hash, environment
fingerprint, checked transport, or mutation result has been accepted. The theorem is not complete.

## Validation

The commands in `validation.md` establish target membership, repository-standard consistency,
JSON syntax, and dossier-local hygiene only. No Lean proof or theorem-completion claim is made.
