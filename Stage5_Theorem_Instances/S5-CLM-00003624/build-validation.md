# Build validation

Frozen gate: `complete-target-semantic-proof-debt`.

The gate checks all 18 claim-owned artifacts, recomputes every authority seal used by its semantic contract, verifies the exact provider registry/source binding, rejects semantic shadowing and forbidden Lean declarations, validates exact M0-P and total injective R0 evidence, checks strict dominance over the incomplete `THM-M-0387` fixture, and elaborates `Statement.lean`, `Proof.lean`, and `Audit.lean` with the pinned toolchain at `--trust=0` and `LAKE_NO_CACHE=1`.

The final command outcome and exact stdout/stderr digests are recorded in the task handoff result after this document is generated. Canonical integration and Master acceptance remain out of worker scope.
