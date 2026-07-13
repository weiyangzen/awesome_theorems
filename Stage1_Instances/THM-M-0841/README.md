# THM-M-0841: Erdos-Stone theorem

This directory is the rev-5.6 `planned` intake for `S56-M-0841-INTAKE`. The repository catalog
provides only the name, attribution, year, and gloss "a fundamental theorem of extremal graph
theory". That gloss does not choose one exact proposition.

The inspected 1946 primary paper proves a finite complete-equipartite containment theorem in
complementary form. A common modern formulation instead computes the asymptotic extremal density
of a fixed graph from its chromatic number. Their equivalence has not been source-audited or
formalized here, so the canonical human statement and canonical Lean target remain open.

Pinned mathlib supplies `extremalNumber`, `turanDensity`, containment above Turan density, complete
equipartite graphs, and related interfaces. It does not contain an Erdos-Stone declaration or the
needed density computation at the pinned revision. The Lean file in this directory only checks
those interfaces; it adds no theorem or proof body.

Current boundary: `[H1, M3, R4]`. This is a self-testable intake proposal, not an accepted state,
exact statement, source-fidelity closure, proof, audit completion, or theorem completion. All six
downstream tasks remain open, and only the integration lane may accept the provisional receipt.

## Artifacts

- `instance.json`: planned intake authority and fail-closed target record.
- `scope-map.md`: included theorem family, unresolved choices, and exclusions.
- `source-statement-crosswalk.md`: repository-to-primary-source-to-Lean component map.
- `task-dag.json`: six open downstream tasks.
- `IntakeProbe.lean`: API-only pinned Lean probe.
- `check_intake.py`: scoped structural and hash validator.
- `validation.md`: exact command ledger and known failures.
- `intake-receipt.json`: provisional node receipt awaiting master acceptance.
