# THM-M-0732 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"circuit complexity" and its gloss "Boolean-circuit lower bounds". Those phrases name a research
area and a family of results, not one mathematical proposition.

The repository's own circuit-complexity table lists several inequivalent possible targets:
Shannon's counting lower bound, `PARITY` lower bounds for `AC^0`, monotone lower bounds for
`CLIQUE`, and lower bounds for modular or majority functions over restricted circuit classes. The
target record chooses none of them and fixes neither a circuit model nor a size/depth bound.
Selecting one would substitute invented mathematics for the assigned target.

This intake therefore freezes the ambiguity and the exclusion boundary. The root remains
`[H3, M4, R4]`. A pinned Lean probe checks only finite Boolean-function ingredients that any later
encoding may use; it is neither a circuit definition nor a theorem statement or proof. Exact
commands and results are recorded in `validation.md`.
