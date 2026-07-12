# THM-M-0358 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Fourier
multiplier theorem". The inventory supplies only the gloss "L^p boundedness of Fourier
multipliers", attributes it to Lars Hormander, and dates it to 1960. That information does not
identify a unique proposition.

Several non-equivalent results fit the label: the Hormander integral/Sobolev multiplier theorem,
the Hormander-Mihlin derivative criterion, an `L^2` bounded-symbol result, or periodic multiplier
variants. They differ in ambient group, symbol regularity, scale-uniform hypotheses, exponent
range, endpoint behavior, and operator construction. Choosing one without a pinpoint source would
broaden or substitute the target.

The intake therefore freezes this ambiguity and the source boundary rather than inventing an exact
statement. The root remains `[H3, M4, R4]`. A narrow pinned Lean probe confirms that mathlib has
Fourier multiplier operators on Schwartz functions and tempered distributions, the `L^2` Fourier
isometry, and `L^p` predicates/norms. These are encoding ingredients, not the claimed general
`L^p` boundedness theorem. Commands and results are recorded in `validation.md`.

