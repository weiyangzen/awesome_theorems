# THM-M-0313 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "spectral
theorem" in functional analysis. The only target-specific source wording is "spectral decomposition
of normal operators". It does not say whether operators are bounded or unbounded, fix the complex
Hilbert-space assumptions, or define the promised decomposition.

Several standard theorems fit that wording but are not interchangeable: representation by a
projection-valued measure and an operator integral, unitary equivalence to a multiplication
operator, and the continuous functional calculus for a normal element. A finite-dimensional
unitary diagonalization would also be a strict specialization and overlaps the separate matrix
target `THM-M-0043`. Choosing one without a pinpoint source would substitute invented mathematics.

The intake freezes this ambiguity and its exclusion boundary rather than manufacturing a formal
proposition. The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib exposes
adjoints, `IsStarNormal`, and continuous-functional-calculus interfaces relevant to candidate
bounded-operator encodings; it is not the target statement or a proof. Exact validation commands
and results are recorded in `validation.md`.
