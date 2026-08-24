# Build validation

The only worker gate is:

`python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean`

It checks frozen identity, provider and source bindings, active imports and qualified-declaration
references, placeholder absence, bidirectional transport, the M0/R0 records, empty cut sets, and
strict dominance. It intentionally does not invoke Lean, Lake, or Elan and cannot substitute for
Master's provider-native trust-zero replay.

The prior Master replay showed that a tactic-local unlimited heartbeat setting did not cover the
declaration's final `whnf` check. `Proof.lean` and `Audit.lean` therefore scope the same reduction
limits over the whole file, while retaining the local settings at the closed decision itself.
