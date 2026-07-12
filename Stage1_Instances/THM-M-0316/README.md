# THM-M-0316 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Riesz-Schauder theory. The manifest supplies
only the Chinese name and the source wording "spectral theory of compact operators". That wording
denotes a theorem family, not a uniquely quantified proposition. This intake therefore preserves
the ambiguity rather than silently selecting a convenient formal theorem.

## Scope map

| Surface | Provisional scope | Intake boundary |
|---|---|---|
| Exact root | Classical Riesz-Schauder spectral theory for a compact endomorphism of a complex Banach space | The source audit must select the precise conjunction before Lean elaboration |
| Nonzero spectrum | Every nonzero spectral point is an eigenvalue | A pinned mathlib candidate exists, but intake grants it no proof credit |
| Multiplicity | Every nonzero eigenspace is finite-dimensional | General Banach-space candidate and exact multiplicity convention remain to be audited |
| Accumulation | Zero is the only possible accumulation point of the spectrum | Must choose an exact topological or finite-outside-disks encoding |
| Fredholm relation | For nonzero `lambda`, `T - lambda I` is invertible unless `lambda` is an eigenvalue | Related theorem; inclusion in the root is unresolved |
| Boundaries | `lambda = 0`, zero operator, finite-dimensional `X`, and `0` absent from the spectrum | Must be explicit mutation and boundary fixtures |
| Exclusions | Hilbert/self-adjoint specializations, compactness of the spectrum alone | These are not substitutes for the Banach-space theorem family |

The planned architecture uses stable discovery labels `RS-ROOT`, `RS-SPEC`, `RS-FDIM`, `RS-ACC`,
`RS-FRED`, and `RS-BOUND`. They are scope labels, not yet a frozen obligation registry.

## Current boundary

The root vector is conservatively `[H1, M3, R3]`. `H1` records a classical published theorem whose
exact source-to-root mapping is unfinished. `M3` records statement/interface-level formal discovery
only. No exact Lean target, expression fingerprint, checked transport, proof body, source acceptance,
or theorem completion is claimed. The dependent statement phase is blocked until the exact root
clauses are selected from a page-level primary-source audit.

The structured intake is in `intake.json`, the source and formal-candidate mapping is in
`source_statement_crosswalk.md`, the open phase graph is in `task-dag.json`, and exact intake checks
are recorded in `validation.md`.
