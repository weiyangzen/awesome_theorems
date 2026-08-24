# Build validation

Worker command: `_baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean`.

The worker is forbidden to invoke Lean, Lake, or Elan. Accordingly this document records only the task-local semantic/evidence preflight. Canonical Master must compile `Statement.lean`, `Proof.lean`, and `Audit.lean` from the integrated canonical Lake environment, at trust 0, and must replace every worker-asserted elaboration/environment digest with independently recomputed evidence before acceptance.

The provenance-only FormalConjectures import is deliberately inside a comment; each executable import is `Mathlib`. This prevents the source declaration body from entering the proof dependency closure.
