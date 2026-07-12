# THM-M-0663 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "o-minimal
structures". The only repository statement is "properties of o-minimal structures". That wording
does not identify a unique theorem: o-minimality is a definition, while monotonicity, definable
choice, dimension results, and cell decomposition are distinct theorems with different hypotheses.

The provisional root family is the one-variable monotonicity theorem for definable functions in an
o-minimal expansion of a dense linear order. This choice is not yet canonical. It must be confirmed
against an inspected primary source in the statement phase; in particular, it must not absorb the
separate cell-decomposition target `THM-M-0664`.

`IntakeProbe.lean` checks only nearby pinned mathlib ingredients: first-order structures,
one-variable definability, dense linear orders, and order intervals. The scoped search found no
o-minimality predicate or monotonicity theorem. These are discovery results, not statement or proof
credit. The lifecycle remains `planned` with root vector `[H3, M4, R4]`; there is no accepted proof
state, audit completion, or theorem completion.
