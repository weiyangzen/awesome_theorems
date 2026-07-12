# THM-M-0501 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"Siegel-Walfisz theorem". The repository supplies only the gloss "estimates for zeros of
L-functions" and the attribution Carl Siegel/Arnold Walfisz (1936). That gloss does not state the
usual theorem and is insufficient to select a unique proposition.

The standard theorem is a uniform prime-number theorem in reduced residue classes, commonly
expressed using `pi(x; q, a)`, `psi(x; q, a)`, or `theta(x; q, a)`, with a logarithmic restriction on
`q` and an ineffective error constant. These forms are related but not definitionally identical,
and sources vary in their quantifiers, normalization, range, and error term. The dossier therefore
freezes this ambiguity and its exclusions rather than inventing an exact statement.

The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib contains Dirichlet
characters, von Mangoldt functions, and the qualitative Dirichlet theorem on primes in arithmetic
progressions. It does not establish the quantitative Siegel-Walfisz estimate. Exact commands and
results are recorded in `validation.md`.
