# THM-M-0187 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "Aleksandrov
uniqueness theorem". The supplied gloss is "uniqueness of closed surfaces of constant Gaussian
curvature", while the supplied attribution and year are Aleksandr Aleksandrov and 1942. Those data
do not identify one theorem: the gloss resembles Liebmann's rigidity theorem, whereas commonly
named Aleksandrov uniqueness results concern different hypotheses and conclusions.

The intake therefore preserves the three plausible theorem families rather than silently replacing
the record with the most convenient one. An exact primary-source proposition must be selected before
the Lean statement can be frozen. The provisional root vector is `[H4, M4, R4]`; there is no
canonical Lean expression, source acceptance, proof credit, audit completion, or theorem completion.

`scope-map.md` records the proposition-changing choices, `source-statement-crosswalk.md` records the
metadata conflict and candidate families, and `task-dag.json` leaves downstream execution open.
Validation performed for this intake is recorded in `validation.md`.
