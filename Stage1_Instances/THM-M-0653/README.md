# THM-M-0653 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Beth's definability theorem. The
repository gloss, "equivalence of implicit and explicit definability", is frozen at human level as
the standard first-order result for a new finite-arity relation symbol: if a theory determines that
relation uniquely on every fixed reduct, then one formula in the old language defines it uniformly
in every model of the theory.

The exact Lean encoding is deliberately left to the statement phase. Pinned mathlib provides
first-order languages, language maps and reducts, theories and model satisfaction, and definable
sets. `IntakeProbe.lean` checks those ingredients in the pinned environment, but the scoped search
found no Beth theorem or ready-made predicate-expansion interface. These are discovery facts only,
not statement or proof credit.

The lifecycle is `planned` at `[H2, M4, R4]`. Primary-source pinpointing, the exact semantic
definition of implicit definability, canonical Lean elaboration, and every later gate remain open.
No accepted proof state, audit completion, or theorem completion is claimed.
