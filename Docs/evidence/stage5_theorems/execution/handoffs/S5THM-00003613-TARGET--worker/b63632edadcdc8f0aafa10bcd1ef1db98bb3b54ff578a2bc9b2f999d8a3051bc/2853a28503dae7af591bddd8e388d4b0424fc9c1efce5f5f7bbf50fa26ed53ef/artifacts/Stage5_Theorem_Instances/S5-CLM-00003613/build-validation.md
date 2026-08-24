# Build validation

Worker gate: `check_stage5_theorem_item.py --claim-card ../claim.json --work-root . --no-lean`. This generation intentionally performs the semantic/evidence preflight only. Lean, Lake, and Elan are reserved for canonical Master trust-zero validation after harvest.

Expected result: valid target-local package with semantic environment, M0-P machine closure, R0 readable reconstruction, empty cut sets, and provisional release candidate.
