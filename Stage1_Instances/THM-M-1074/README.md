# THM-M-1074 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "compound
Poisson process." The repository source says only that it is a generalization of the Poisson
process; that is a topic description, not an exact proposition. The dossier therefore freezes the
intended theorem family as the construction and distributional characterization of a compound
Poisson process, while leaving the exact source theorem and conventions to the statement phase.

The intended process has the form `X_t = sum_{k=1}^{N_t} Y_k`, where `N` is a Poisson process and
the marks `Y_k` are iid and independent of `N`. The selected source must determine which substantive
conclusion is canonical: stationary independent increments, the compound-Poisson marginal law and
characteristic-function formula, or a source theorem containing both. No convenient subset may
later be substituted for that choice.

No canonical Lean expression or proof is claimed. The provisional root vector is `[H1, M4, R4]`;
audit and theorem completion are false. The scope map, source crosswalk, and open task DAG preserve
the unresolved choices. Intake validation is recorded in `validation.md`.
