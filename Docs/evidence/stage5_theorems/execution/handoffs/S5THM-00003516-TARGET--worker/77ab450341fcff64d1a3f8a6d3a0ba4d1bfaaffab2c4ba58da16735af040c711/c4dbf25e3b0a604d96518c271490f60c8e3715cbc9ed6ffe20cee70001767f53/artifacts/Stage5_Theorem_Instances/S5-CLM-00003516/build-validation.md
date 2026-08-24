# Build validation — S5-CLM-00003516

Tracked toolchain: Lean 4.29.0 through the canonical Lake project.

Required command: frozen claim command `complete-target-semantic-proof-debt`.
The command validates the exact 18 owned paths, sealed crosswalk/machine/readable/
release records, source-provider pins, forbidden Lean constructs, trust-zero
elaboration of `Statement.lean`, `Proof.lean`, and `Audit.lean`, semantic
substitution constraints, strict dominance, and empty cut sets.

The current validation receipt records timestamps and exact stdout/stderr hashes.
Cold replay does not use a target-owned stale olean. Final acceptance remains a
canonical-Master action outside this worker.
