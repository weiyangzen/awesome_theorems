# THM-M-0721 rev-5.6 intake

This directory is the `planned` intake for the existence of an NP-complete decision problem. The
human-level claim is frozen as an existential statement about languages over a fixed finite
alphabet, with membership in NP and hardness under polynomial-time many-one reductions. A Boolean
satisfiability language is the intended witness, but the later statement phase must select an exact
encoding and cannot replace this target with the stronger, separately catalogued Cook-Levin
theorem.

The repository source gives only the phrase "existence of NP-complete problems." It does not fix
machine models, encodings, reductions, or a primary theorem anchor. The statement phase now freezes
these choices as binary strings, verifier-based NP, and polynomial-time many-one reductions using
mathlib's bundled TM2 interface. The provisional root vector is `[H1, M3, R4]`: the exact statement
has been elaborated, but its source mapping and proof remain open and no readable reconstruction has
been reviewed.

The scope map, source crosswalk, and open task DAG define the downstream work. Intake validation and
its deliberately limited claim boundary are recorded in `validation.md`. No audit completion or
theorem completion is claimed.

## Statement phase handoff

`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage` in `Statement.lean` is the proposed exact
target. `statement.json` freezes its expression and environment fingerprints, encodings, binders,
mutation tests, and boundary policy. `statement-validation.md` records the real Lean commands. This
is statement-only evidence pending master acceptance; it contains no Cook-Levin or existence proof.
