# THM-M-0733 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `自然证明`
(Natural Proofs). The repository attributes the item to Alexander Razborov and Steven Rudich and
describes it only as an obstacle to proving complexity lower bounds.

That description points toward the Natural Proofs barrier, but it does not select a proposition.
The Razborov-Rudich framework has separate definitions for largeness, constructivity, usefulness,
circuit classes, and pseudorandomness, and its barrier conclusions depend on the chosen parameters
and cryptographic hypothesis. An unconditional statement that all lower-bound methods fail would be
false and is not a permissible replacement.

The intake therefore freezes the ambiguity rather than manufacturing a theorem. The root is
`[H5, M4, R4]`: the supplied wording is not yet a stable proposition, no exact formal artifact is
identified, and no readable proof reconstruction exists. `IntakeProbe.lean` checks only that pinned
mathlib offers finite Boolean-function and polynomial-time Turing-machine vocabulary that could be
used after source selection. It is not a target statement or proof.

