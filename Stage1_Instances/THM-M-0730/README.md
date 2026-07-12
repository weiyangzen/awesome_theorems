# THM-M-0730 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "stronger form
of the PCP theorem" and its gloss "a combinatorial proof of PCP". Those phrases point toward Irit
Dinur's gap-amplification proof, but they do not identify one mathematical proposition. A proof
method is not itself a theorem statement, and "stronger form" could refer to the gap-amplification
engine, the bounded-degree constraint-graph formulation, or a PCP consequence with particular
completeness, soundness, randomness, and query bounds.

The intake therefore freezes that ambiguity and forbids silently substituting the ordinary PCP
theorem. The root remains `[H3, M4, R4]`. A pinned Lean probe checks only general finite graph,
finite-set, and rational-number APIs that could support a later constraint-graph encoding; it is
not a target or proof. Exact commands and results are in `validation.md`.

