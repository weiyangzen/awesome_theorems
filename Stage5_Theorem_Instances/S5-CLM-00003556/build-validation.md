# Build validation

The frozen command `complete-target-semantic-proof-debt` validates the exact 18-path package, recomputes all authority seals used by its semantic gates, rejects source-symbol substitution, and elaborates `Statement.lean`, `Proof.lean`, and `Audit.lean` independently with the pinned Lean toolchain under trust zero and cold-cache settings.

The command outcome and timestamps are recorded in `receipts/current-validation.json`. Canonical Master must rerun the same checks against integrated bytes.
