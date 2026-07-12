# THM-M-0721 rev-5.6 intake

This directory is the `planned` intake for the existence of an NP-complete decision problem. The
human-level claim is frozen as an existential statement about languages over a fixed finite
alphabet, with membership in NP and hardness under polynomial-time many-one reductions. A Boolean
satisfiability language is the intended witness, but the later statement phase must select an exact
encoding and cannot replace this target with the stronger, separately catalogued Cook-Levin
theorem.

The repository source gives only the phrase "existence of NP-complete problems." It does not fix
machine models, encodings, reductions, or a primary theorem anchor. Those choices remain explicit
statement-phase obligations. The provisional root vector is `[H1, M4, R4]`: the classical result is
published, but its exact source-to-statement mapping has not been accepted, no canonical Lean target
has been elaborated, and no readable proof reconstruction has been reviewed.

The scope map, source crosswalk, and open task DAG define the downstream work. Intake validation and
its deliberately limited claim boundary are recorded in `validation.md`. No audit completion or
theorem completion is claimed.
