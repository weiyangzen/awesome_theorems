# THM-M-0988 rev-5.6 intake

This directory is the `planned` intake for the one-dimensional Lindeberg-Levy central limit
theorem. It freezes the human claim as convergence in distribution of centered, square-root
normalized partial sums of iid real random variables with finite variance to the corresponding
centered Gaussian law.

The legacy Lean module is discovery input only. Although it contains a wrapper around a pinned
mathlib theorem, rev-5.6 requires the later statement, anchor-audit, obligation, proof, validation,
and release nodes to re-establish every claim. The provisional root vector is `[H2, M3, R4]`; this
intake claims neither kernel closure nor theorem completion.

The scope map, source crosswalk, and open task DAG record the exact downstream decisions. Intake
validation and its limits are recorded in `validation.md`.
