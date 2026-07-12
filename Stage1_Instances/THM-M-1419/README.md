# THM-M-1419 rev-5.6 intake

This directory contains the fail-closed intake, exact statement freeze, and anchor audit for Oseledets'
multiplicative ergodic theorem. `OseledetsStatement.lean` kernel-elaborates the selected
finite-dimensional real, invertible, ergodic, two-sided splitting proposition with minimal direct
imports. `statement.md` records its binders, boundary decisions, mutations, and environment.

The proposition is exact at the Lean statement boundary. `anchor-audit.json` freezes the complete
pinned-mathlib search and a substantive external Lean 4 splitting candidate at an immutable commit.
That candidate uses different interfaces, a newer Lean/mathlib closure, and has no checked exact
transport here. The root vector is `[H2, M3, R3]`: source-audited external discovery is not
repo-local kernel closure. No `H0`, `M0`, audit completion, or theorem completion is claimed.

The historical `THM-M-1056` Lean file is discovery input for a separately owned target only. It
cannot supply statement or proof credit here. The scope map, source crosswalk, and task DAG record
the downstream choices and boundaries. Exact commands and results are recorded in `validation.md`
and `anchor-audit.md`.
