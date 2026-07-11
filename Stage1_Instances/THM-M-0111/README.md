# THM-M-0111: Kodaira embedding theorem

This is the rev-5.6 **planned intake dossier** for `S56-M-0111-INTAKE`. It
freezes the intended mathematical scope but claims neither an exact Lean
statement nor a proof.

## Status boundary

- Lifecycle: `planned` (`L0 / rework_required`).
- Human source status: `H4`; a primary publication is identified, but its exact
  theorem locator, assumptions, normalization, and errata have not been audited.
- Machine status: `M4`; the legacy `StatementShape` uses abstract `Prop` fields
  and is only a discovery hint, not the exact Kodaira theorem.
- Readability status: `R4`; no independently reviewed reconstruction exists.
- Audit complete: no. Theorem complete: no.

The authoritative intake fields are in `intake.json`. `scope.md` records the
formal boundary and `source_statement_crosswalk.md` records source fidelity
debt. Later nodes must not silently broaden the conclusion from holomorphic
embedding into complex projective space to an unrelated scheme-theoretic
projectivity predicate.

## Open task DAG

1. `S56-M-0111-STATEMENT`: choose native complex-manifold, Kahler-form,
   integral-cohomology, and projective-space APIs; elaborate the exact target.
2. `S56-M-0111-ANCHOR_AUDIT`: audit mathlib and external Lean 4 candidates at
   immutable revisions, and complete the primary-source locator audit.
3. `S56-M-0111-OBLIGATION_TREE`: freeze typed obligation and provenance graphs.
4. `S56-M-0111-PROOF`: supply genuine terminal proof bodies or pinned imports.
5. `S56-M-0111-VALIDATION`: perform kernel, trust, provenance, and replay gates.
6. `S56-M-0111-RELEASE`: reconcile evidence without inheriting legacy credit.

## Intake validation

See `validation.md`. Structural repository checks and JSON parsing pass at base
revision `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.
