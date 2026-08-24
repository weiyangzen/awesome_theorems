# Build validation

Worker validation command: `check_stage5_theorem_item.py --no-lean`.

The local gate checks exact identity, sealed semantic environment, pinned
provider bytes, placeholder/shadow rejection, M0 machine closure, R0 readable
coverage, strict dominance over THM-M-0387, and empty H/M/R cut sets.  Lean,
Lake, and Elan are intentionally not invoked in this task-local generation.
