# THM-M-0473 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0473`, the catalog entry
named Bezout's identity. The repository claim is that the equation
`a*x + b*y = gcd(a,b)` has integer solutions. Intake fixes the elementary number-theory family:
two integer inputs, two integer coefficient witnesses, and the nonnegative gcd embedded in the
integers. It does not yet claim an accepted primary-source statement or a canonical Lean target.

The catalog gives no quantifiers, input domains, gcd sign convention, coefficient/result domain,
or boundary policy. Those choices matter: a natural-coefficient reading is false for examples
that require a negative coefficient, while polynomial or general-ring Bezout identities are
different theorems. The later statement phase must admit and independently review an exact source,
then freeze and mutation-test one proposition without broadening this intake scope.

Pinned mathlib contains direct natural-input and integer-input declarations named
`Nat.gcd_eq_gcd_ab` and `Int.gcd_eq_gcd_ab`. `IntakeProbe.lean` authenticates their types and checks
existential wrappers, including the `(0,0)` boundary, against the manifest-pinned environment. This
is discovery evidence only: it does not freeze a canonical expression, audit terminal provenance,
or confer proof credit.

`instance.json` is the structured scope authority. `scope-map.md` records proposition-changing
decisions and exclusions, `source-statement-crosswalk.md` maps the catalog wording to source and
Lean components, and `task-dag.json` leaves every downstream phase open.

Status boundary: self-tested planned intake proposal only, pending integration-lane acceptance.
The provisional vector is `[H1, M3, R4]`; no H0, M0, R0, accepted execution state, audit
completion, or theorem completion is claimed.
