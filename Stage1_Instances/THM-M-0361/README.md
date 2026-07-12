# THM-M-0361 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"Fefferman-Stein theorem". The inventory gives only the gloss "a real-variable characterization
of H^p spaces", the names Charles Fefferman and Elias Stein, and the year 1972. It does not state a
single theorem.

That wording can denote non-interchangeable characterizations by radial or nontangential maximal
functions, grand maximal functions, Lusin area functions, or Littlewood-Paley functions, in
different Hardy-space models and exponent ranges. It can also be confused with the distinct
Fefferman-Stein sharp-function or vector-valued maximal inequalities. Choosing any of these without
a pinpoint source would substitute a familiar theorem for the repository target.

This intake therefore freezes the ambiguity and exclusion boundary rather than inventing a
proposition. The root remains `[H3, M4, R4]`. A pinned Lean probe confirms only nearby analytic
infrastructure: `Lp`/`MemLp`, convolution, Fourier transform, and Schwartz functions. Those APIs
are encoding ingredients, not a Hardy-space definition, an exact characterization, or a proof.
Exact commands and results are recorded in `validation.md`.
