# Build validation

The three owned Lean files were each replayed from the canonical pinned Lake
environment with Lean 4.29.0 and `--trust=0`; all returned exit code 0.

The frozen target validator command is:

```text
/usr/bin/python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root .
```

Its final stdout/stderr hashes, timestamps, and exit code are recorded in
`receipts/current-validation.json` and `_outbox/result.json`. Network access is
not used. Canonical files, Lake configuration, and immutable bootstrap inputs
remain unchanged.
