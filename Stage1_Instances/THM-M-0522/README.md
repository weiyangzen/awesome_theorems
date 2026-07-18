# THM-M-0522: Kolyvagin-Gross-Zagier theorem

This is the retained planned intake dossier for `S56-M-0522-INTAKE`. It
freezes the intended partial BSD result but claims neither an exact Lean
statement nor a proof.

## Status boundary

- Lifecycle: `planned` (`L0 / rework_required`).
- Human status: `H1`; primary papers are identified, but exact result locators,
  hypotheses, normalization, errata, and the combined implication have not
  received a source audit or independent review.
- Machine status: `M3`; no exact Lean proposition has been selected or
  elaborated, and no proof artifact is credited.
- Readability status: `R4`; no anchored, independently reviewed proof
  reconstruction exists.
- Audit complete: no. Theorem complete: no.

The canonical intake authority is `intake.json`. `scope.md` fixes the included
and excluded claims, while `source_statement_crosswalk.md` records the source
fidelity work still required. The historical metadata label `已验证` supplies
no current proof credit.

## Open task DAG

1. `S56-M-0522-STATEMENT`: choose native definitions, elaborate the exact
   rank-at-most-one target, check transports, and run statement mutations.
2. `S56-M-0522-ANCHOR_AUDIT`: audit primary sources, mathlib, and immutable
   external Lean 4 candidates.
3. `S56-M-0522-OBLIGATION_TREE`: freeze the proof, provenance, trust,
   documentation, evidence, refinement, and workflow graphs.
4. `S56-M-0522-PROOF`: integrate and replay an admitted exact machine proof
   without placeholders; new root work requires an active reviewed frontier exception.
5. `S56-M-0522-VALIDATION`: run kernel, trust, provenance, and replay gates.
6. `S56-M-0522-RELEASE`: reconcile accepted evidence and decide completion.

The intake self-checks and their exact results are recorded in `validation.md`.
