# THM-M-0108: Chow's theorem

This is the rev-5.6 planned intake dossier for `S56-M-0108-INTAKE`. It
freezes the intended mathematical scope but claims neither an exact Lean
statement nor a proof.

## Status boundary

- Lifecycle: `planned` (`L0 / rework_required`).
- Human status: `H1`; a primary publication is identified, but its exact
  theorem locator, hypotheses, terminology, and errata are not yet audited.
- Machine status: `M3`; a legacy statement-shaped artifact exists, but its
  analytic and algebraic predicates are explicitly placeholders.
- Readability status: `R4`; no reviewed proof reconstruction exists.
- Audit complete: no. Theorem complete: no.

The structured intake authority is `intake.json`. `scope.md` freezes the
boundary, and `source_statement_crosswalk.md` records the unresolved fidelity
work. The historical metadata label `已验证` supplies no rev-5.6 proof credit.

## Open task DAG

1. `S56-M-0108-STATEMENT`: elaborate a native Lean target and test its scope.
2. `S56-M-0108-ANCHOR_AUDIT`: audit mathlib, external Lean, and primary sources.
3. `S56-M-0108-OBLIGATION_TREE`: freeze typed obligation and provenance graphs.
4. `S56-M-0108-PROOF`: provide genuine proof bodies or pinned imports.
5. `S56-M-0108-VALIDATION`: run kernel, trust, provenance, and replay gates.
6. `S56-M-0108-RELEASE`: reconcile accepted evidence and decide completion.

Validation results are recorded in `validation.md`.
