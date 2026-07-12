# THM-M-0700 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Herbrand's theorem. The two
repository sources give different short glosses: "quantifier elimination and Skolemization" and
"the Herbrand model of first-order logic". Neither supplies a quantified statement, a source
edition and pinpoint, or the conventions needed to identify one proposition.

"Herbrand's theorem" commonly names several equivalent only after substantial setup: a theorem
about existential formulas and finite disjunctions of ground instances, an unsatisfiability
criterion for universal clauses, or existence of a Herbrand model. Equality, empty Herbrand
universes, normal forms, and the chosen proof calculus materially affect those statements. Picking
one silently would broaden or substitute the source record.

This intake therefore freezes that ambiguity and an explicit scope boundary. The root remains
`[H1, M4, R4]`. A pinned Lean probe confirms that mathlib supplies first-order languages, terms,
sentences, realization, satisfiability, and a one-step Skolem-language construction. Those APIs are
encoding ingredients, not a Herbrand theorem or proof. Exact commands and results are recorded in
`validation.md`.
