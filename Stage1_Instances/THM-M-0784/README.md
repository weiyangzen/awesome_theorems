# THM-M-0784 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Proper
Forcing Axiom" (PFA). The source inventory supplies only `PFA and its consequences`, attributes
the entry to Saharon Shelah, and gives the year 1982. It does not identify a particular formulation
of PFA or name one of its many consequences.

PFA itself is normally an additional set-theoretic principle, not an unconditional theorem of ZFC.
A familiar formulation quantifies over proper partial orders and families of at most `aleph_1`
dense subsets and asserts the existence of a filter meeting each member. Even that gloss leaves
order orientation, properness, the dense-family bound, the ambient set theory, and the filter
encoding to be fixed. The phrase "and its consequences" additionally fails to select a conclusion.
Treating a chosen consequence, a relative-consistency theorem, or an assumed-PFA projection as the
target would substitute a different proposition.

The intake therefore freezes the ambiguity and exclusion boundary rather than inventing a theorem.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms only that mathlib exposes partial
orders, filters, dense sets, cardinality, and `aleph_1` ingredients. It is neither a PFA definition
nor proof. Exact commands and results are recorded in `validation.md`.
