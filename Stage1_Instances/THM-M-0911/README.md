# THM-M-0911 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0911`, the binomial
theorem. The repository catalog supplies only the phrase `(a+b)^n` expansion formula, attributes
the result to many mathematicians in antiquity, and labels it verified. Under rev-5.6 these
uncited fields are discovery metadata, not an accepted source statement or proof receipt.

The phrase identifies the classical finite binomial-expansion family, but it does not fix the
coefficient algebra, commutativity premise, coefficient casts, summation bounds, exponent order,
or exact formula. Intake preserves the conventional family in which a natural power of a sum is
expanded using `Nat.choose`. It does not silently select a commutative-semiring theorem over the
more general commuting-elements theorem, and it does not freeze a canonical Lean expression.

Pinned mathlib contains the exact-topic declarations `add_pow`, `Commute.add_pow`, and
`Commute.add_pow'` in `Mathlib.Data.Nat.Choose.Sum`. `IntakeProbe.lean` authenticates their types,
axiom reports, agreement of the commutative and commuting-element forms, and the `n = 0` and
`n = 2` boundaries in the manifest-pinned environment. This is discovery evidence only: source
identity, exact target selection, proof-body provenance, trust closure, and anchor acceptance
remain downstream.

`instance.json` is the structured scope authority. `scope-map.md` records proposition-changing
choices and exclusions, `source-statement-crosswalk.md` maps the catalog phrase to source and Lean
components, and `task-dag.json` leaves all six dependent phases open.

The provisional vector is `[H1, M3, R4]`. No `H0`, `M0`, `R0`, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
