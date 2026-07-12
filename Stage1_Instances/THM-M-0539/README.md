# THM-M-0539 rev-5.6 intake

This directory is the `planned` intake for the cellular homology theorem. The repository record says
only "computation of the homology of a CW complex". The intake freezes the standard theorem family:
the cellular chain complex obtained from the skeletal filtration computes the singular homology of
the CW complex, with chain groups identified with the relative homology of consecutive skeleta.

The source wording does not fix coefficients, reduced versus unreduced homology, the precise CW
complex hypotheses, naturality, or whether the cell-basis description and boundary-degree formula
belong to the root. Those choices remain hard gates for the statement phase. The pinned mathlib
snapshot contains CW-complex and singular-homology APIs, but the intake probe proves only that these
two interfaces elaborate together; it is not the cellular homology theorem.

The provisional root vector is `[H2, M4, R4]`. No exact Lean target, obligation denominator, proof,
audit completion, or theorem completion is claimed. The scope map, source crosswalk, and open task
DAG record the downstream decisions.
