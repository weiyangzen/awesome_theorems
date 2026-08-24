# Build validation

Worker preflight command:

`python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean`

The command performs the task-local semantic/evidence validation permitted by
the claim. It does not run Lean, Lake, or Elan. Canonical Master must compile
`Statement.lean`, `Proof.lean`, and `Audit.lean` from source at trust zero after
harvest and must independently recompute the elaborated root, transitive
environment, read trace, and mutation outcomes.
