# Build validation

The frozen command `complete-target-semantic-proof-debt` checks the exact
workset member, sealed semantic environment, exact provider import, absence of
local semantic shadowing and forbidden Lean placeholders, M0 machine closure,
total injective R0 reconstruction, strict dominance, and independent trust-zero
elaboration of `Statement.lean`, `Proof.lean`, and `Audit.lean`.

The machine-readable command timestamps and output digests are stored in
`receipts/current-validation.json`; the final worker result repeats the same
outcome and binds every delivered byte plus the task-local patch.
