# Build validation — S5-CLM-00003496

Worker validation uses exactly the immutable claim command:

```text
/usr/bin/python3 WORK/_baseline/check_stage5_theorem_item.py \
  --claim-card TASK/claim.json --work-root WORK --no-lean
```

`WORK` and `TASK` expand to the absolute generation-local paths recorded in
`receipts/current-validation.json`. Network access is denied. No Lean, Lake, or
Elan command is run by the worker.

The preflight checks all 18 owned artifacts, exact source/member binding,
semantic-environment shape, frozen provider source hashes, absence of Lean
placeholders and local semantic substitutions, bidirectional transports,
machine/readability/release seals, empty cut sets, and strict dominance over
the negative fixture. A zero exit code is necessary for handoff but insufficient
for canonical acceptance. Master must compile the three integrated Lean files
from source at trust zero and recompute the semantic and declaration evidence.

The exact final stdout, stderr, timestamps, command hash, artifact digests, and
trace seal are written only after the last successful validation run.
