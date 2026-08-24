# Build validation

Worker preflight: PASS (`check_stage5_theorem_item.py --no-lean`).

The preflight checks exact workset membership, sealed semantic environment,
pinned provider bytes, placeholder-free Lean surfaces, M0 machine closure,
R0 readability, empty H/M/R cut sets, and strict dominance over the pinned
THM-M-0387 incomplete fixture.  The canonical build remains a separate
post-harvest trust-zero operation owned by Master.
