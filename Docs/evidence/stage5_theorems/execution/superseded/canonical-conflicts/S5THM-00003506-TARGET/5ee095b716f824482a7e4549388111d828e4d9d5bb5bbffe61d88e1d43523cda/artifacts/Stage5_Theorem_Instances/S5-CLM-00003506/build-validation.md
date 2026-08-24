# Build validation

Pinned toolchain: `leanprover/lean4:v4.29.0`.

Each of `Statement.lean`, `Proof.lean` and `Audit.lean` was elaborated from
source with `lake env lean --trust=0`.  All three commands exited zero.  The
validator command is `complete-target-semantic-proof-debt`; its result is
recorded in `receipts/current-validation.json`.
