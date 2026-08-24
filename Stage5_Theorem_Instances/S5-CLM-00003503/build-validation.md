# Build validation — S5-CLM-00003503

Worker validation is intentionally the claim-mandated semantic preflight:

```text
/usr/bin/python3 _baseline/check_stage5_theorem_item.py \
  --claim-card ../claim.json --work-root . --no-lean
```

The worker does not invoke Lean, Lake, or Elan.  Canonical Master owns the
trust-zero compilation of `Statement.lean`, `Proof.lean`, and `Audit.lean`
after this handoff is harvested.  The three surfaces contain the frozen
provider import as provenance text and use `import Mathlib` as their only
compilable import.

The package is accepted here only as a provisional release candidate; the
machine closure, semantic environment, and current trace remain subject to
independent Master recomputation.
