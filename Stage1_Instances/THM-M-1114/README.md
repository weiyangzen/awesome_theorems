# THM-M-1114 rev-5.6 intake

This directory is the `planned` intake for the giant-component theorem in the
Erdos-Renyi random graph. The repository phrase "the appearance of a giant component in a random
graph" identifies the classical phase-transition family, but it does not specify a unique theorem:
the random-graph model, parameterization, probability mode, subcritical/supercritical regimes, and
component-size bounds are all absent from the source metadata.

The intake therefore freezes the intended scope without inventing an exact proposition. The
statement phase must select and inspect a pinpoint primary theorem and decide whether the root is
the supercritical existence/uniqueness result alone or the paired threshold theorem for
`G(n, c/n)`. No Lean expression or proof receives credit at intake. The provisional root vector is
`[H1, M4, R4]`; audit completion and theorem completion are both false.

`scope-map.md` records the mathematical decisions still required,
`source-statement-crosswalk.md` maps every available source phrase to those decisions, and
`task-dag.json` leaves all downstream rev-5.6 phases open. Exact self-test commands and boundaries
are recorded in `validation.md`.
