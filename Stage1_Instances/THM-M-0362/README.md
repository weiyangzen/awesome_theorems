# THM-M-0362 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "atomic
decomposition theorem". The source inventory gives only the gloss "atomic decomposition of the
H^1 space", an attribution to Charles Fefferman and Elias Stein, and the year 1972. It does not
identify a source, define `H^1` or an atom, or state the decomposition and norm estimates.

Several non-interchangeable results fit that gloss: real Hardy `H^1(R^n)` defined by maximal
functions, boundary Hardy spaces, analytic Hardy spaces, and Hardy spaces on more general measure
spaces. Even for `R^n`, atomic conventions differ in support shape, cancellation, size norm, and
whether the result asserts only representation or also equivalence of norms. Choosing among these
without an inspected source would substitute invented mathematics for the repository target.

The intake therefore freezes this ambiguity and the exclusion boundary rather than a proposition.
The root remains `[H1, M4, R4]`. A pinned Lean probe confirms that mathlib exposes `Lp`, `MemLp`,
Bochner integration, Haar volume, convergence, and summability ingredients. It is not an `H^1`
definition, atom definition, theorem statement, or proof. Exact commands and results are recorded
in `validation.md`.

