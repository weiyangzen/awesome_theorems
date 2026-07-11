# THM-M-0122: Faltings' theorem

This directory is the rev-5.6 planned intake dossier for
`S56-M-0122-INTAKE`. It freezes the intended Mordell-conjecture consequence of
Faltings' work. It does not claim an exact Lean statement or a proof.

## Status boundary

- Lifecycle: `planned` (`L0 / rework_required`).
- Human status: `H4`; the primary paper is identified, but its exact internal
  locator, conventions, assumptions, and errata have not been independently
  audited.
- Machine status: `M4`; the legacy module contains a useful statement shape,
  but its natural-number genus slot is not a native geometric genus invariant.
- Readability status: `R4`; no independently reviewed proof reconstruction
  exists.
- Audit complete: no. Theorem complete: no.

The canonical human claim, scope, and debt are recorded in `intake.json`.
`scope-map.md` prevents common broadenings, and
`source-statement-crosswalk.md` records the unresolved source fidelity work.

## Open task DAG

1. `S56-M-0122-STATEMENT`: select native curve and genus APIs and elaborate the
   exact theorem, including checked rational-point encodings.
2. `S56-M-0122-ANCHOR_AUDIT`: audit mathlib and external Lean 4 candidates at
   immutable revisions and finish the primary-source locator audit.
3. `S56-M-0122-OBLIGATION_TREE`: freeze typed proof, provenance, trust,
   evidence, documentation, and workflow graphs.
4. `S56-M-0122-PROOF`: provide genuine terminal proof bodies or pinned imports.
5. `S56-M-0122-VALIDATION`: run exact-type, kernel, trust, provenance,
   composition, and replay checks.
6. `S56-M-0122-RELEASE`: reconcile accepted evidence and decide completion.

Validation commands and their results are recorded in `validation.md`.
