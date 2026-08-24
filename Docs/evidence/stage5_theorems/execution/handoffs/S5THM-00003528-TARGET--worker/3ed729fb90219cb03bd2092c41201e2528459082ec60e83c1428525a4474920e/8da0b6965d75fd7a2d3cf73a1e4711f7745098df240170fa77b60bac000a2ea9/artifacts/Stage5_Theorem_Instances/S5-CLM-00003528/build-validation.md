# Build validation

## BV-command

Worker validation uses only the immutable claim command
`check_stage5_theorem_item.py --claim-card <current claim> --work-root <current work> --no-lean`.

## BV-boundary

No Lean, Lake, Elan, clone, fetch, network access, canonical checkout access,
or other task root is used.  A successful worker preflight means the package
meets the task-local semantic/evidence contract; it does not claim canonical
compilation.

## BV-master

The canonical Master must compile `Statement.lean`, `Proof.lean`, and
`Audit.lean` at trust zero, recompute the exact root and transitive environment,
verify source hashes, perform a cold offline replay, run semantic-substitution
mutations, and issue the only authoritative release decision.
