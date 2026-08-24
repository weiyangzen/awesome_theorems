# Build validation

Pinned toolchain: `leanprover/lean4:v4.29.0` (from the canonical `lean-toolchain`).

Validation uses `lake env lean --trust=0` separately on `Statement.lean`, `Proof.lean`, and `Audit.lean`, with `LAKE_NO_CACHE=1` for the frozen validator replay. All three commands exit zero. Static scans reject placeholder/oracle declarations and semantic redefinitions. The frozen complete-target validator then checks the sealed semantic environment, M0 closure, R0 reconstruction, release conjunction, and repeats all three trust-zero elaborations.

The replay is offline and source-oriented: claim-owned Lean inputs are explicit, the provider file is content-addressed, and no stale target olean is accepted as evidence.
