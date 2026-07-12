# THM-M-0321 rev-5.6 statement

This directory is the fail-closed `planned` intake dossier for the Markov-Kakutani fixed-point
theorem. It freezes the intended human claim as the common-fixed-point theorem for a commuting
family of continuous affine self-maps of a nonempty compact convex set in a locally convex real
topological vector space.

The exact Lean target is frozen in `Statement.lean`. It uses ambient functions with invariance,
continuity on `K`, preservation of convex combinations on `K`, and pairwise commutation on `K`;
this faithfully states self-maps without inventing an affine-space instance on the subtype. The
`EqOn` alternate encoding, four structural mutations, and empty-index boundary elaborate in the
pinned Lean environment. Exact evidence is recorded in `statement-validation.md`.

The provisional root vector is `[H2, M3, R4]`. The primary-source theorem/page and errata crosswalk
remains open for the anchor-audit phase. No proof, accepted state, audit completion, or theorem
completion is claimed.
