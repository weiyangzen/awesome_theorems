# THM-M-1309 rev-5.6 intake

This is a `planned` dossier for the Lindblad-Rodnianski global nonlinear stability theorem for
Minkowski spacetime in harmonic (wave) gauge. The Stage0 gloss, "harmonic gauge for the Einstein
equations," names a method rather than a proposition; it is not treated as the theorem statement.

The frozen intake claim is the small-data global stability result described in `intake.json`.
`scope-map.md` fixes its inclusions and exclusions, while `source-statement-crosswalk.md` records the
primary publication and the statement details that still require a page-exact audit.

## Intake verdict

Lifecycle is `planned`, with provisional root vector `[H1, M4, R3]`. The source is identified, but
its exact quantified norm package is not yet transcribed and independently checked. No repo-local
Lean declaration has been identified and no formal target has elaborated. The first failed gate is
therefore the exact-statement gate. The theorem is not complete.

## Open task DAG

`STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Each node remains open and retains the dependencies in the authoritative execution DAG.
