# THM-M-0740 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "monotone
circuit lower bounds". The originating mathematics inventory says only "lower bounds for monotone
circuits" and attributes the topic to Alexander Razborov in 1985. That wording denotes a family of
results, not one quantified proposition.

A second repository inventory gives a useful but non-authoritative clue: its "Razborov lower
bound" row says "monotone circuit lower bound for CLIQUE". Even that does not fix the graph
encoding, clique-parameter regime, circuit basis, fan-in, size measure, uniformity convention, or
asymptotic lower-bound function. Those choices materially change the theorem, so this intake does
not silently select them.

The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib exposes finite simple
graphs, clique predicates, and the generic order-theoretic `Monotone` predicate. The bounded search
did not locate a Boolean-circuit complexity API. The probe is encoding reconnaissance only, not a
canonical statement or proof. Exact commands and results are recorded in `validation.md`.
