# THM-M-0472 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0472`, the catalog entry
named the Euclidean algorithm. The repository supplies only the gloss "an algorithm for finding
the greatest common divisor", the attribution Euclid, and a date near 300 BCE. It does not specify
one mathematical proposition, input or output types, division convention, termination measure,
correctness contract, or source locator.

The intended family is the repeated-remainder algorithm for two whole-number inputs. A complete
correctness statement normally combines termination with the facts that the returned value divides
both inputs and every common divisor divides it. A recurrence identity alone, a concrete gcd
calculation, or the extended algorithm's Bezout coefficients proves a different boundary. Intake
therefore records those candidate readings without selecting a canonical statement.

Pinned Lean core exposes `Nat.gcd`, its Euclidean recurrence `Nat.gcd_rec`, well-founded induction,
and `Nat.gcd_eq_iff`, the divisibility characterization needed for a correctness specification.
`IntakeProbe.lean` authenticates those interfaces using only `Init.Data.Nat.Gcd` and checks zero and
concrete boundaries against the manifest-pinned environment. This is discovery-only `M3` evidence:
it does not freeze a canonical expression, audit a terminal body, or confer proof credit.

`instance.json` is the structured scope authority. `scope-map.md` records proposition-changing
decisions and exclusions, `source-statement-crosswalk.md` maps the catalog wording to source and
Lean components, and `task-dag.json` leaves every dependent phase open.

Status boundary: self-tested planned intake proposal only, pending integration-lane acceptance.
The provisional vector is `[H1, M3, R4]`; no H0, M0, R0, accepted execution state, audit
completion, or theorem completion is claimed.
