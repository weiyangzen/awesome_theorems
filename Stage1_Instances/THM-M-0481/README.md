# THM-M-0481 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Bertrand's postulate. The repository
supplies only the Chinese gloss `n与2n之间必有素数` ("there is a prime between `n` and `2n`"),
attributes it to Joseph Bertrand in 1845, and labels it verified. Under rev-5.6 that label is
untrusted inventory metadata, not a primary-source audit, an exact Lean proposition, or proof
evidence.

The gloss identifies the standard theorem family but does not specify the domain, require `n > 0`,
or decide whether "between" includes the upper endpoint. Those omissions matter. The unrestricted
natural-number reading is false at `n = 0`, while the positive half-closed form and the customary
strict form have different hypotheses at `n = 1`. Intake therefore preserves the family and records
the proposition-changing choices without silently selecting an exact source statement.

Pinned mathlib contains the strong discovery candidate
`Nat.exists_prime_lt_and_le_two_mul`: for a nonzero natural `n`, it supplies a prime `p` with
`n < p` and `p <= 2 * n`. `IntakeProbe.lean` authenticates that declaration, its alias
`Nat.bertrand`, and the relevant boundary behavior in the pinned environment. This is real `M3`
statement/interface discovery evidence only. Formal-candidate provenance, terminal proof bodies,
trust closure, and proof credit belong to later phases.

The provisional root vector is `[H1, M3, R4]`: the named classical theorem is known, but no pinpoint
primary-source statement, assumption and errata crosswalk, or independent source review is
accepted; a usable pinned formal statement exists but the canonical source-faithful target is not
frozen; and no reviewed readable proof reconstruction exists. `instance.json` is the structured
scope authority and `task-dag.json` leaves all six downstream phases open. No H0, M0, R0, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
