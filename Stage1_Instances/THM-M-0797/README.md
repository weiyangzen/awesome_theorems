# THM-M-0797 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "diamond
principle". The source inventory supplies only the gloss "combinatorial set-theory principle",
an attribution to Ronald Jensen, the year 1972, and an untrusted `verified` label. It does not state
a proposition.

Standard diamond principles are a parameterized family rather than one theorem. The usual
`Diamond` on the first uncountable ordinal asserts the existence of a sequence whose `alpha`th
entry is a subset of `alpha` and which correctly guesses every subset of `omega_1` on a stationary
set. Variants change the cardinal, restrict the stationary set, guess functions instead of subsets,
or assert Jensen's theorem that the constructible universe satisfies diamond. The bare principle is
not a ZFC theorem, while the relative theorem about `L` has additional model-theoretic content.

Selecting any one of those claims from the title would silently broaden or substitute the source.
This intake therefore freezes the ambiguity and exclusion boundary rather than inventing a Lean
target. The root remains `[H3, M4, R4]`. A pinned Lean probe checks only nearby ordinal, first
uncountable ordinal, closed-set, and unbounded-set APIs. It is not a diamond definition, statement,
or proof. Exact commands and results are recorded in `validation.md`.
