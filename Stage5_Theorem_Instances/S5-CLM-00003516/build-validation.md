# Build validation

Worker gate: the immutable claim's `complete-target-semantic-proof-debt`
command, executed with `--no-lean`. It verifies exact artifact membership,
strict/sealed JSON, frozen provider bindings, no semantic shadowing, exact M0
and R0 evidence shape, and strict dominance over the pinned negative fixture.

Lean compilation is intentionally absent: the claim forbids the worker from
invoking Lean, Lake, or Elan. The canonical Master alone performs cold offline
trust-zero compilation after harvest.
