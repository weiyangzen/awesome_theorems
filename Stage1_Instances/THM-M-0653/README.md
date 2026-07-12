# THM-M-0653 rev-5.6 statement

This directory is the fail-closed `planned` intake dossier for Beth's definability theorem. The
repository gloss, "equivalence of implicit and explicit definability", is frozen at human level as
the standard first-order result for a new finite-arity relation symbol: if a theory determines that
relation uniquely on every fixed reduct, then one formula in the old language defines it uniformly
in every model of the theory.

`Statement.lean` now freezes and elaborates that target. It represents the extension as the sum of
`L` with a relational language whose `k`-ary symbols are `PLift (k = n)`, hence it adds exactly one
`n`-ary relation and no functions. Implicit definability quantifies over two expanded structures on
the same carrier, requires both to model `T` and their pulled-back `L`-structures to be equal, and
requires agreement on the distinguished relation. Explicit definability places the existential
old-language formula outside the model quantifier, so the formula is parameter-free and uniform.
The statement includes `n = 0`, empty `T`, inconsistent `T`, and arbitrary nonempty carriers.

The lifecycle remains `planned`, now at `[H2, M3, R4]`: the exact statement is locally elaborated,
but no proof body or formal-candidate audit is credited. Primary-source pinpointing and every later
gate remain open. No accepted proof state, audit completion, or theorem completion is claimed.
