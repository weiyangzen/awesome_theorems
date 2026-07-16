# THM-M-0108: Chow's theorem

This directory contains the rev-5.6 intake dossier and the provisional worker
output for `S56-M-0108-STATEMENT`. The statement phase selects and elaborates
the intake-permitted reduced carrier formulation; it does not prove it.

## Status boundary

- Lifecycle: `planned` (`L0 / rework_required`).
- Human status: `H1`; a primary publication is identified, but its exact
  theorem locator, hypotheses, terminology, and errata are not yet audited.
- Machine status: `M3`; `Statement.lean` gives an exact native proposition and
  elaborates in the pinned environment, but no proof body has been supplied.
- Readability status: `R4`; no reviewed proof reconstruction exists.
- Audit complete: no. Theorem complete: no.

`statement.json` records the selected target and expression fingerprint;
`statement-receipt.json` and `check_statement.py` record the provisional
statement self-test. `scope.md` freezes the boundary, while
`source_statement_crosswalk.md` keeps source-fidelity debt visible. Historical
blocker and recheck files remain immutable records of earlier attempts. The
historical metadata label `已验证` supplies no rev-5.6 proof credit.

## Open task DAG

1. `S56-M-0108-STATEMENT`: worker-self-tested target pending integration and
   dependency-ordered master acceptance.
2. `S56-M-0108-ANCHOR_AUDIT`: audit mathlib, external Lean, and primary sources.
3. `S56-M-0108-OBLIGATION_TREE`: freeze typed obligation and provenance graphs.
4. `S56-M-0108-PROOF`: provide genuine proof bodies or pinned imports.
5. `S56-M-0108-VALIDATION`: run kernel, trust, provenance, and replay gates.
6. `S56-M-0108-RELEASE`: reconcile accepted evidence and decide completion.

Validation results are recorded in `validation.md`.
