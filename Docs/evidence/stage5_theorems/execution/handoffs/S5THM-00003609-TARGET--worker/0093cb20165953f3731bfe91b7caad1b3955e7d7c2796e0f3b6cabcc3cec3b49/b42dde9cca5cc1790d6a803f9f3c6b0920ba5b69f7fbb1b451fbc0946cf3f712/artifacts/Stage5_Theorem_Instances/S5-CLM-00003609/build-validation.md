# Build validation

## Command

`/usr/bin/python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean`

## Worker boundary

This generation performs semantic/evidence preflight only. Lean, Lake and
Elan are intentionally not invoked here; canonical Master performs the cold
trust-zero compilation after harvest.

## Replay ledger

The three claim-owned Lean surfaces each contain the frozen provider module
path and qualified declaration in a provenance comment, import `Mathlib`, and
prove a direct hypothesis transport without a placeholder, unsafe injection,
claim-specific axiom or bodyless oracle. The final command outcome and output
digests are bound in `receipts/current-validation.json` and the worker result.
