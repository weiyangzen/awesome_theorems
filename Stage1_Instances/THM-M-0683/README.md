# THM-M-0683 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Goedel's
incompleteness theorem". The only supplied claim is "a consistent system containing arithmetic is
incomplete". That sentence omits conditions essential to a theorem: which incompleteness theorem,
the formal language and proof calculus, the represented arithmetic, effective axiomatizability,
and the exact meanings of consistency and incompleteness.

Read literally as applying to every consistent theory containing arithmetic, the sentence is
false: the complete theory of the standard natural numbers is consistent (assuming the standard
model) and contains arithmetic, but is not effectively axiomatizable. Standard first
incompleteness and Rosser formulations repair this in different ways and are not interchangeable.
The intake therefore freezes the ambiguity and the counterexample boundary rather than silently
adding hypotheses.

The root remains `[H5, M4, R4]`. A pinned Lean probe confirms that mathlib supplies first-order
syntax encodings and Goedel's beta-function lemma, which its own module describes as a step toward
an eventual first-incompleteness proof. This is API evidence only, not the target statement or a
proof. Exact commands and results are recorded in `validation.md`.
