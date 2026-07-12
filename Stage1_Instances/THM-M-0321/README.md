# THM-M-0321 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the Markov-Kakutani fixed-point
theorem. It freezes the intended human claim as the common-fixed-point theorem for a commuting
family of continuous affine self-maps of a nonempty compact convex set in a locally convex real
topological vector space.

The exact Lean target is frozen in `Statement.lean`. It uses ambient functions with invariance,
continuity on `K`, preservation of convex combinations on `K`, and pairwise commutation on `K`;
this faithfully states self-maps without inventing an affine-space instance on the subtype. The
`EqOn` alternate encoding, four structural mutations, and empty-index boundary elaborate in the
pinned Lean environment. Exact evidence is recorded in `statement-validation.md`.

The immutable formal-anchor inventory is recorded in `anchor-audit.json` and explained in
`anchor-audit.md`. No exact pinned mathlib or immutable external Lean 4 candidate was located; the
near hits are statement mismatches or the unrelated Riesz-Markov-Kakutani representation theorem.
The provisional root vector therefore remains `[H2, M3, R4]`. The human primary-source theorem/page
and errata crosswalk remains open. No proof, accepted state, audit completion, or theorem completion
is claimed.
