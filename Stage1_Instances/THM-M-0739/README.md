# THM-M-0739 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"depth-bounded circuits" and its gloss "lower bounds on circuit depth". The record names a broad
research topic rather than one mathematical proposition.

Several inequivalent claims fit those words: `PARITY` lower bounds for polynomial-size `AC^0`
families, depth lower bounds for bounded-fan-in circuits, size-depth tradeoffs, and lower bounds for
restricted gate bases or particular function families. The source record fixes none of the circuit
syntax, gate basis, fan-in, uniformity, size allowance, input function, quantifier order, or bound.
Choosing one of these results would substitute invented mathematics for the assigned target.

The intake therefore freezes that ambiguity and its exclusion boundary. The root remains
`[H3, M4, R4]`. A narrow pinned Lean probe confirms only generic finite Boolean-function ingredients
that could support a later encoding; it is not a circuit definition, theorem statement, or proof.
Exact commands and results are recorded in `validation.md`.
