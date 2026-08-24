# Build validation

Validation uses the immutable claim command `complete-target-semantic-proof-debt`. The command runs the frozen target validator against this task-local work root, verifies exact ownership and semantic seals, scans all three Lean files for forbidden or shadowing declarations, and elaborates them independently with the pinned Lean toolchain at trust zero and with the Lake cache disabled.

The current validation receipt records start/finish timestamps, command identity, stdout/stderr digests, exact semantic-environment digest, cold-from-source status, semantic-substitution mutation outcomes, and artifact hashes. This worker declares only a provisional release candidate; a successful local command cannot set `master_accepted`.
