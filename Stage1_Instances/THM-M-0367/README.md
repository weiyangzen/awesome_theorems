# THM-M-0367 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"L^p boundedness theorem". The only supplied gloss is "L^p boundedness of various operators".
That describes a property shared by many unrelated operator theorems, not one mathematical
proposition: it names neither an operator nor its domain, measure spaces, exponent range,
hypotheses, or bound.

Selecting the Hardy-Littlewood maximal operator, a Calderon-Zygmund singular integral, the Fourier
transform, or any other familiar operator would therefore substitute invented mathematics for the
source record. The intake freezes this ambiguity and the required decisions rather than choosing a
convenient theorem. The root remains `[H5, M4, R4]`; `H5` records that the current wording is not a
stable proposition, not that every possible Lp-boundedness theorem is false or open.

A narrow pinned Lean probe confirms that mathlib provides `MemLp`, `Lp`, `eLpNorm`, and continuous
linear maps as possible encoding ingredients. It is not a canonical statement, formal candidate,
or proof. Exact commands and results are recorded in `validation.md`.
