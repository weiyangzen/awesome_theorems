# THM-M-0794 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `适当力迫`
(proper forcing). The source inventory supplies only the gloss `保持基数的力迫` ("forcing that
preserves cardinals"), an attribution to Saharon Shelah, and the year 1982. It does not state a
theorem or define properness.

That gloss is not an exact definition: properness is normally formulated through countable
elementary submodels and generic conditions, while its standard preservation consequence concerns
`ω₁`; arbitrary cardinal preservation is a different and stronger-looking phrase. Possible targets
include the definition of a proper forcing notion, preservation of `ω₁`, preservation under a
specified iteration, or a result for a particular forcing. Choosing among them would substitute
mathematics not fixed by the repository source.

The intake therefore freezes this ambiguity and its exclusions rather than inventing a proposition.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms only nearby order, ideal/cofinal, and
cardinal APIs; it is neither a forcing definition nor theorem evidence. Exact validation commands
and results are recorded in `validation.md`.
