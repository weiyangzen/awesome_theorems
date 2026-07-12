# THM-M-0691 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Haken
theorem". The repository gloss says only "a lower bound on the proof length of the pigeonhole
principle". That identifies the proof-complexity result usually associated with Armin Haken's 1985
paper *The intractability of resolution*, but it does not state an exact proposition.

A formal target must fix the pigeonhole CNF family, the resolution calculus and admissible rules,
the proof-size measure, and a quantified numerical lower bound. In particular, "exponential" and
"lower bound" are not Lean propositions without constants and a range of parameters. Choosing
these data from memory would risk substituting a nearby formulation for the source theorem.

The intake therefore freezes this ambiguity and its exclusions. The root remains `[H1, M4, R4]`.
A pinned Lean probe checks only generic finite syntax and cardinality APIs that can support a future
encoding; it is neither Haken's statement nor a proof. Exact commands and results are recorded in
`validation.md`.
