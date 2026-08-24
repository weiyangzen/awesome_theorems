# Build validation — S5-CLM-00003579

The worker gate is the prescribed task-local semantic preflight:

```text
/usr/bin/python3 _baseline/check_stage5_theorem_item.py \
  --claim-card ../claim.json \
  --work-root . \
  --no-lean
```

This generation is forbidden from invoking Lean, Lake, or Elan.  The command
checks strict JSON, authority seals, frozen source binding, exact imports and
qualified provenance references, forbidden declaration patterns, M0 evidence,
R0 coverage, and the strict-dominance release certificate.  Canonical Master
validation must subsequently perform trust-zero cold compilation of all three
Lean files from the authoritative repository.

The recorded command outcome and output digests are in
`receipts/current-validation.json`.
