# Build validation — S5-CLM-00003651

The prescribed worker command is:

```text
/usr/bin/python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean
```

This is a task-local semantic/evidence preflight. It verifies the exact owned artifact set, sealed crosswalk, pinned provider source digest, source/target expression lock, no-local-shadowing guard, M0 candidate record, R0 reconstruction record, and strict-dominance candidate. It intentionally does not invoke Lean, Lake, or Elan.

Canonical Master compilation is deliberately outside this generation. The Master must compile the integrated bytes from source at trust zero and independently validate the root declaration, declarations, dependencies, axioms, cold replay, and semantic-substitution mutations before changing `master_accepted`.
