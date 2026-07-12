# THM-M-1117 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the repository label "small-world
networks". The source wording, "small-world phenomenon", is not yet an exact proposition. The
intake therefore freezes the ambiguity and the permitted claim family rather than inventing a
theorem.

The scope map is in `scope-map.md`, and the source boundary is in
`source-statement-crosswalk.md`. `instance.json` is the planned-instance record, while
`task-dag.json` records the dependent open phases. `IntakeProbe.lean` checks only that the pinned
Lean environment contains graph connectivity, distance, diameter, and neighborhood vocabulary
needed by plausible later encodings. It is not a canonical target and proves no small-world
result.

## Status boundary

Lifecycle is `planned`. No exact source theorem, canonical Lean expression, source review, formal
candidate, proof body, obligation closure, audit completion, or theorem completion is claimed. The
first downstream blocker is statement identity: an authorized statement phase must select a
truth-valued, source-faithful result and distinguish analytic probability claims from the 1998
paper's simulation and empirical-network observations.
