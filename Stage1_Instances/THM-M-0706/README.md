# THM-M-0706 rev-5.6 intake

This directory is the `planned` intake for the Church-Turing thesis. The repository does not give
one stable theorem statement: its mathematics inventory says only "equivalent definitions of
computability", while its computer-science inventory states the broader thesis that every
intuitively computable function is Turing-computable. The latter contains an intentionally
informal predicate and is not itself a theorem of a fixed formal system.

The intake freezes that ambiguity rather than replacing the thesis with an easier equivalence
between two formal machine models. The statement phase must select a primary-source-backed formal
equivalence theorem, or classify the philosophical thesis as outside the exact Lean theorem gate;
it must preserve the distinction between those outcomes. The provisional root vector is
`[H3, M4, R4]`. No canonical Lean expression, accepted proof state, audit completion, or theorem
completion is claimed. Exact checks are recorded in `validation.md`.
