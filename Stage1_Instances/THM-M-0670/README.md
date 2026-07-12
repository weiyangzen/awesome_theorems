# THM-M-0670 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository item called
"Ackermann quantifier elimination". The repository supplies only the gloss "quantifier
elimination for Presburger arithmetic", attributes it to Wilhelm Ackermann in 1928, and labels it
verified. That metadata does not identify an exact theorem or proof source.

The intended theorem family says that formulas about natural-number addition can be transformed
to equivalent quantifier-free formulas. The exact statement is not frozen: quantifier elimination
is false for the bare first-order language `(0, 1, +)` in the usual syntactic sense, so a faithful
statement must specify an expanded language (normally including order and congruence/divisibility
predicates), the standard natural-number structure or a theory, parameters, and whether the claim
is semantic existence or correctness of Ackermann's elimination procedure. These choices require
an inspected primary source rather than invention at intake.

Pinned mathlib contains the Presburger language, formula semantics, quantifier-free predicate, and
the theorem that Presburger-definable sets over `Nat` are semilinear. `IntakeProbe.lean` validates
those interfaces. Mathlib's own Presburger module records quantifier elimination as TODO, and no
terminal quantifier-elimination declaration was found by the bounded intake search. This is API
discovery only, not a substitute theorem or proof credit.

Lifecycle remains `planned` at `[H2, M4, R4]`. Primary-source pinpointing, exact statement
selection, Lean elaboration, anchor audit, obligation registry, proof, and all release gates remain
open. No accepted proof state, audit completion, or theorem completion is claimed.
