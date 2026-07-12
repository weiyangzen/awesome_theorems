# THM-M-1419 rev-5.6 intake

This directory contains the fail-closed intake and exact statement freeze for Oseledets'
multiplicative ergodic theorem. `OseledetsStatement.lean` kernel-elaborates the selected
finite-dimensional real, invertible, ergodic, two-sided splitting proposition with minimal direct
imports. `statement.md` records its binders, boundary decisions, mutations, and environment.

The proposition is now exact at the Lean statement boundary, but the sparse repository gloss does
not identify a numbered primary-source variant. The root vector remains `[H2, M4, R4]`: statement
elaboration is not source fidelity or proof closure. No `H0`, `M0`, audit completion, or theorem
completion is claimed.

The historical `THM-M-1056` Lean file is discovery input for a separately owned target only. It
cannot supply statement or proof credit here. The scope map, source crosswalk, and open task DAG
record the downstream choices and boundaries. Intake checks are recorded in `validation.md`.
