# Build validation

Worker command: `check_stage5_theorem_item.py --claim-card <task>/claim.json --work-root <task>/work --no-lean`.

The worker preflight validates identity, source bytes, semantic-environment seals, absence of forbidden Lean constructs and shadowing, exact M0 evidence shape, total injective R0 mapping, and strict dominance over THM-M-0387. It deliberately does not execute Lean/Lake/Elan. Master must compile all three Lean artifacts from source at trust zero after integration.

Current validation trace: `06156917bf5c50951aac8efbdc43356365c9372103f40fd695c3d51baf190d08`.
