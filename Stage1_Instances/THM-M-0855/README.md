# THM-M-0855 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Chvatal-Erdos theorem. The
repository gives the recognizable gloss "a connectivity and independence-number condition for
the existence of a Hamiltonian cycle," attributes it to Vaclav Chvatal and Paul Erdos in 1972,
and labels it verified. The label is untrusted metadata and supplies no source or machine credit.

The institutional Erdos archive scan of Chvatal and Erdos, *A note on Hamiltonian circuits*,
identifies the intended root as Theorem 1 on printed page 111: a graph on at least three vertices
that is `s`-connected and has no independent set larger than `s` has a Hamiltonian circuit. This is an
exact proposition-level primary-source lead, but it is not yet `H0`. In particular, the paper does
not define `s`-connected locally; its proof cites Dirac's generalized Menger theorem. The source's
incorporated vertex-connectivity convention, the parameter domain, graph conventions, correction
history, preservation, and independent review remain open.

The intake freezes that human theorem family while leaving the exact Lean target null for the
dependent statement phase. Pinned mathlib has Hamiltonicity, independent-set and independence-
number predicates, vertex deletion, and ordinary connectedness. The bounded search found neither
a vertex `s`-connectivity interface nor the Chvatal-Erdos theorem. Edge connectivity is a different
notion and is explicitly excluded. `IntakeProbe.lean` checks only the adjacent APIs.

The provisional vector is `[H1, M4, R4]`: a pinpoint primary statement and proof passage are known
but not source-fidelity accepted; no source-identical usable formal artifact is credited; and no
reviewed proof reconstruction exists. The source's distinct Theorems 2 and 3, concerning a
Hamiltonian path and Hamiltonian-connectedness, are outside this root. All six downstream tasks
remain open. No exact Lean statement, H0, M0, R0, accepted execution state, audit completion,
theorem completion, accepted receipt, or master acceptance is claimed.
