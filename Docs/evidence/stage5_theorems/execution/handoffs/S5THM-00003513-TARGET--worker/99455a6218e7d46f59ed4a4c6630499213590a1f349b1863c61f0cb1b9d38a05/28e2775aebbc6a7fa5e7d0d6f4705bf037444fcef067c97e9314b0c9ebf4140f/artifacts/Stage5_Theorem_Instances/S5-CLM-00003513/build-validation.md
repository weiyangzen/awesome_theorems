# Build validation

Validation profile: `complete-target-semantic-proof-debt`.

The worker runs exactly the immutable checker named by `claim.json` with
`--no-lean`.  This checks the complete owned artifact set, sealed semantic
crosswalk, provider source binding, absence of forbidden Lean declarations,
M0/R0 evidence shapes, empty cut sets, and strict dominance certificate.

No Lean, Lake, or Elan command is run in this generation.  After harvest, the
canonical Master must perform the clean cold offline build, trust-zero
elaboration, per-declaration axiom/body/dependency audit, semantic substitution
mutations, stale-object mutation, and receipt-tamper checks against integrated
bytes.  `receipts/current-validation.json` binds the local command outcome;
`receipts/release-decision.json` remains `master_accepted = false`.
