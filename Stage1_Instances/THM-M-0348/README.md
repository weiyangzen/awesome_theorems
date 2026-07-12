# THM-M-0348 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"Riesz-Fejer theorem". The only source gloss says "convergence of Fourier series" and supplies
the names Marcel Riesz and Lipot Fejer and the year 1923. That wording does not identify a unique
theorem: it omits the summation method, function space, topology or mode of convergence, and the
precise hypotheses.

The label is additionally close to the non-interchangeable Fejer-Riesz factorization theorem for
nonnegative trigonometric polynomials. Reversing the names is not enough evidence to choose either
the convergence family or the factorization theorem. Selecting a convenient member of either
family would substitute mathematics for the repository record.

This intake therefore freezes the ambiguity and its exclusion boundary rather than inventing a
canonical proposition. The root remains `[H3, M4, R4]`. A pinned Lean probe checks that mathlib
provides Fourier-series, Cesaro-limit, and Laurent-polynomial vocabulary that could encode candidate
readings; it proves none of them. Exact commands and results are recorded in `validation.md`.
