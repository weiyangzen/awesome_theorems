# Build validation

Worker semantic preflight command: `check_stage5_theorem_item.py --no-lean`.
It checks the exact target artifact set, frozen source identity, sealed
crosswalk, M0 closure, R0 reconstruction, and provisional strict-dominance
release certificate. Lean/Lake/Elan compilation is reserved for the canonical
Master after harvest.
