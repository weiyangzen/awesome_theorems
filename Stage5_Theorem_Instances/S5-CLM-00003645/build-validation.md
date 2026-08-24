# Build validation

Worker validation command: `check_stage5_theorem_item.py --no-lean`.

The task-local gate checks strict JSON, authority seals, exact source/provider
identity, equal source/target elaborated-expression digests, pinned transitive
constant source bytes, no local shadowing, M0 machine evidence, total injective
R0 reconstruction, and strict dominance over `THM-M-0387`. Lean/Lake/Elan are
intentionally not invoked in this generation. Canonical Master must perform
the trust-zero cold replay after harvest.
