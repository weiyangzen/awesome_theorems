# Build validation

Worker gate: `complete-target-semantic-proof-debt` using the exact immutable
claim command and `--no-lean`.  The captured UTC interval and complete stdout,
stderr, argv, and trace hashes are in `receipts/current-validation.json` and
the generation result.

Master gate: cold offline compilation of all three Lean surfaces at trust zero
against the canonical pinned toolchain.  That gate is intentionally not run by
this generation and remains mandatory before acceptance.
