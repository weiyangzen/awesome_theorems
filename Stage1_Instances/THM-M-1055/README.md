# THM-M-1055 rev-5.6 intake

This directory is the `planned` intake for the Birkhoff pointwise ergodic theorem. It freezes the
intended human claim as almost-everywhere convergence of time averages of an integrable observable
under an ergodic probability-preserving transformation to its space mean.

The statement phase now freezes and kernel-elaborates the direct almost-everywhere convergence
target in `Statement.lean`, with minimal pinned mathlib imports and structural mutation checks. The
legacy Lean module remains discovery input only: its `StatementShape` packages the desired limit
and does not supply a proof. The provisional root vector remains fail-closed and no proof, audit
completion, or theorem completion is claimed. The scope map, source crosswalk, statement record,
and open task DAG define the downstream work.
