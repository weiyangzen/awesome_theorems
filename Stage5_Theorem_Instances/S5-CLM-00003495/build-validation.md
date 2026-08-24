# Build validation

Worker gate: the immutable `complete-target-semantic-proof-debt` command is run with `--no-lean`; this is the only executable validation authorized inside the generation.

Master gate: after harvest, compile `Statement.lean`, `Proof.lean`, and `Audit.lean` cold from source with the repository-pinned Lean toolchain at trust zero. Independently recompute the elaborated root, declaration bodies and types, dependencies, axioms, semantic source environment, and mutation outcomes. Worker evidence cannot replace this gate.
