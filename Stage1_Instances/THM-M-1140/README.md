# THM-M-1140 rev-5.6 dossier

This is the planned dossier for the strong maximum principle for harmonic functions. The terse
Stage0 phrase is interpreted as the classical real-valued Euclidean theorem: on a nonempty,
connected open domain, a harmonic function that attains an interior maximum is constant. This
interpretation must still pass source review. The exact Lean proposition is now frozen in
`Statement.lean` and described by `statement.json`.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Harmonic ambient `u : Space n -> Real`, connected open `Omega`, attained interior maximum, global constancy | Exact proposition elaborated; no proof credit |
| Domain | Finite-dimensional real Euclidean space | Dimension-zero behavior remains a statement mutation probe |
| Extremum | Global maximum at a domain point | Local-maximum formulation is only an equivalent candidate |
| Dual form | Strong minimum principle via `-u` | Requires a checked transport and is not root proof credit |
| Analytic route | Mean-value property, positivity of the averaging gap, local constancy, connected propagation | Architecture hint only; no obligation registry or proof credit |
| Exclusions | Weak boundary principle, general elliptic operators, subharmonic/manifold/discrete variants | Separate theorems; no broadened claim |
| Foundations | Lean 4 kernel and pinned mathlib | Minimal import and statement environment fingerprint frozen; later trust gates remain open |

The structured binder order, assumptions, exclusions, and status vector are authoritative in
`intake.json`. Source wording and candidate formal surfaces are crosswalked in
`source_statement_crosswalk.md`.

## Statement verdict

Lifecycle remains `planned`. `Stage1Instances.THM_M_1140.HarmonicStrongMaximumPrinciple` elaborates
with the pinned toolchain and the single direct import
`Mathlib.Analysis.InnerProductSpace.Harmonic.Basic`. A proved iff checks the transport between an
ambient maximizing point plus membership and the subtype binder recorded at intake. This closes
only the worker statement phase pending master acceptance. No maximum-principle proof or theorem
completion is claimed.

## Validation

`validation.md` records both the intake checks and the statement elaboration recipe. The Lean run
checks the proposition, structural mutation declarations, and encoding transport, not the strong
maximum principle itself.

## Anchor audit

`anchor-audit.json` and `anchor-audit.md` record the bounded repo-local, pinned-mathlib, and public
Lean search at immutable revisions. Mathlib supplies harmonic regularity/sign operations, a
complex-plane mean-value theorem, and close complex maximum-modulus analogues, but no declaration
closing the arbitrary-dimensional real harmonic root. Two external projects were source-audited;
neither supplies a trusted matching proof. The root remains `M3`, with no proof credit.
