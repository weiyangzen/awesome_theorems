# THM-M-0772 rev-5.6 intake

This directory is the fail-closed `planned` intake for Hausdorff's maximal principle. The repository
claim is: every partially ordered set has a maximal chain. Here "maximal" means inclusion-maximal
among chains, not a chain of greatest cardinality and not the existence of a maximal element of the
underlying order.

The intended human claim is frozen, but the exact Lean declaration remains a statement-phase task.
Pinned mathlib contains the closely matching and more general declaration `maxChain_spec`, for an
arbitrary binary relation. `IntakeProbe.lean` only confirms that candidate's name and current type;
it does not yet establish exact source identity, a checked specialization, or proof credit.

The provisional root vector is `[H1, M4, R4]`. The source edition/locator, independent source
review, canonical Lean expression, obligation registry, and all completion gates remain open. No
audit completion or theorem completion is claimed.
