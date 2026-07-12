# THM-M-0734 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "algebraic
complexity". The source inventory supplies only the topic gloss "algebraic computational
complexity", attributes it to Leslie Valiant, and gives the year 1979. It does not state a theorem.

The label can refer to arithmetic circuit size or depth, algebraic complexity classes such as VP
and VNP, completeness results, lower bounds for restricted circuit models, or complexity of a
specific polynomial family. These are not interchangeable propositions. In particular, choosing
VP versus VNP would collide with the adjacent repository item `THM-M-0735`, which explicitly records
that open problem.

The intake therefore freezes the ambiguity and exclusion boundary rather than inventing a theorem.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib supplies multivariate
polynomials and basic evaluation/degree interfaces that could support a later encoding. It is not
an arithmetic-circuit definition, theorem statement, or proof. Exact commands and results are in
`validation.md`.
