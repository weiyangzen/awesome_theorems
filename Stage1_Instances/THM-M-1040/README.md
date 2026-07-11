# THM-M-1040 rev-5.6 intake

This directory is the `planned` intake for the Feller-process theorem. It freezes the intended
human claim at the level supported by the repository description: a suitable Feller transition
semigroup on a locally compact state space admits a Markov-process realization with that
semigroup. The exact state-space hypotheses, initial laws, canonical path space, and path
regularity must be selected from an inspected primary source during the statement phase.

The legacy Lean module is discovery input only. It supplies a useful candidate object model, but
its realization structure contains the terminal transition-law and Markov properties as fields;
its `StatementShape` therefore receives no statement or proof credit. The provisional root vector
is `[H2, M4, R4]`. No exact Lean target, audit completion, or theorem completion is claimed.

The scope map, source crosswalk, and open task DAG define the downstream work. Intake validation
commands and exact results are recorded in `validation.md`.
