# THM-M-1038 rev-5.6 intake

This directory is the `planned` intake for the Yamada-Watanabe theorem. The intended claim is the
classical implication from weak existence and pathwise uniqueness for a stochastic differential
equation to existence of a strong solution (with uniqueness in law as the customary companion
consequence). The exact source formulation, solution concept, coefficient assumptions, time
horizon, and the relationship between the two conclusions remain statement-phase obligations.

The legacy Lean module is discovery input only. It supplies a local abstract SDE interface, and
several hypotheses in that interface are proposition-valued fields. It therefore gives no
rev-5.6 statement or proof credit. The provisional root vector is `[H2, M4, R4]`; no canonical Lean
target, audit completion, or theorem completion is claimed.

The scope map, source crosswalk, and open task DAG delimit subsequent work. Intake validation and
its exact commands are recorded in `validation.md`.
