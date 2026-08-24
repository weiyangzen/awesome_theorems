# Build validation

Prescribed worker command:

`python3 _baseline/check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean`

The worker gate checks immutable identity, owned-path completeness, strict JSON
and seals, pinned provider-source binding, no local semantic shadowing or
substitution, exact M0/R0 evidence shapes, empty cut sets, and provisional
strict dominance. It does not invoke Lean, Lake, or Elan.

Canonical acceptance still requires a cold offline trust-zero build of all
three Lean files from integrated bytes, exact semantic-environment
recomputation, semantic-substitution mutations, and an independently issued
Master receipt. This document does not claim that acceptance has occurred.
