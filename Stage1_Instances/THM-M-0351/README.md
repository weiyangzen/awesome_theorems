# THM-M-0351 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"Littlewood-Paley theory". The source inventory gives only the gloss "frequency decomposition of
functions", the names John Littlewood and Raymond Paley, and the year 1931. It does not state a
single theorem.

The label can refer to several non-interchangeable claims: the periodic Littlewood-Paley
inequality, a Euclidean dyadic square-function norm equivalence, an `L^2` orthogonal decomposition,
or a homogeneous/inhomogeneous reconstruction theorem. These choices have different domains,
cutoffs, endpoint restrictions, convergence modes, and conclusions. Selecting one without a
pinpoint source would substitute invented mathematics for the repository target.

The intake therefore freezes the ambiguity and the scope boundary rather than a proposition. The
root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib supplies Fourier transforms
on `L^2`, the circle Fourier basis and series convergence, Fourier multipliers on tempered
distributions, and `L^p` predicates. Those APIs are encoding ingredients, not an exact
Littlewood-Paley statement or proof. Exact commands and results are recorded in `validation.md`.

