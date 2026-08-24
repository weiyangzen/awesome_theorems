# Build validation

The frozen command `complete-target-semantic-proof-debt` is the authoritative
validator.  Before handoff, Statement.lean, Proof.lean and Audit.lean are each
compiled with the pinned Lean toolchain and `--trust=0`; the final receipt below
records the validator outcome and hashes.
