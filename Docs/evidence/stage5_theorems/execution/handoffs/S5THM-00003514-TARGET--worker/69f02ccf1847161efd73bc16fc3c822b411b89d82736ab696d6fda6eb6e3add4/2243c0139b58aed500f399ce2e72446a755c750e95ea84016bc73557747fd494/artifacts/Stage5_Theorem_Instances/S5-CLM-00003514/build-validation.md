# Build validation

Required worker command:

```text
/usr/bin/python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean
```

The final receipt records the exact absolute argv, start/end times, exit code,
and stdout/stderr digests.  The `--no-lean` flag is mandatory in this generation:
the immutable claim forbids Lean, Lake, and Elan.  A passing worker result proves
only the semantic/evidence preflight.  The canonical Master must independently
compile all three Lean files from the integrated bytes at trust zero.
