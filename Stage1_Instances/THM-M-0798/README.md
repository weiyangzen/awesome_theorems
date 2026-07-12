# THM-M-0798 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "square
principle" (`方框原理`). The source inventory supplies only the gloss "combinatorial set-theory
principle", an attribution to Ronald Jensen, the year 1972, and an untrusted `verified` label. It
does not state a proposition.

Several materially different principles are called square: successor-cardinal `square_kappa`,
`square(kappa)` at a specified limit cardinal, weak square, indexed square, and global square. Their
indexing ordinals, club order-type bounds, coherence clauses, width, and no-thread requirements are
not interchangeable. Nor does the title say whether the intended claim asserts the principle in
the constructible universe, derives a consequence, or discusses consistency or independence.

This intake freezes that ambiguity rather than choosing a convenient variant. The root remains
`[H3, M4, R4]`. A pinned Lean probe confirms only that ordinal, cardinal-cofinality, set, and
pairwise-relation APIs needed for a later encoding are available; it is not a square-principle
statement or proof. Exact checks and the downstream boundary are recorded in `validation.md`.
