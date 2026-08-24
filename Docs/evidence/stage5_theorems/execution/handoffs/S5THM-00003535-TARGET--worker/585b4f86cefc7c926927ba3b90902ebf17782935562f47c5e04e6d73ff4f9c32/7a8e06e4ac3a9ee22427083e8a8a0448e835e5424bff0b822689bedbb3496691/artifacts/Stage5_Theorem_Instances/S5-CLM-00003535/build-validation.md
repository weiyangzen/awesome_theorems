# Build validation — S5-CLM-00003535

Worker validation is intentionally semantic and offline.  The exact command
from the immutable claim is:

```text
/usr/bin/python3 <generation>/work/_baseline/check_stage5_theorem_item.py \
  --claim-card <generation>/claim.json \
  --work-root <generation>/work --no-lean
```

The command checks strict JSON, authority seals, exact artifact ownership,
source/provider bindings, no-shadowing rules, M0 closure evidence, R0 reverse
coverage, and strict dominance over the THM-M-0387 fixture.  Lean/Lake/Elan
are not invoked by this worker.  The canonical Master must independently run
its trust-zero cold replay after harvest.
