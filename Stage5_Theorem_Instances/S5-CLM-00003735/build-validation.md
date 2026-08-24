# Build validation — S5-CLM-00003735

The worker command is the task-local semantic/evidence preflight:

```text
/usr/bin/python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean
```

It checks exact frozen identity, canonical JSON seals, source-byte pins,
semantic transport shape, shadowing/import-substitution guards, M0/R0/release
evidence shape, and strict dominance over the pinned THM-M-0387 negative
fixture.  Lean, Lake, and Elan are intentionally outside this worker gate;
the canonical Master performs the cold trust-zero build after harvest.
