# Build validation — S5-CLM-00003625

Validation is pinned to claim command
`complete-target-semantic-proof-debt`.  It runs offline from the generation's
task-local work root and invokes the immutable
`_baseline/check_stage5_theorem_item.py` with the immutable claim card.

The gate checks all eighteen artifacts, recomputes authority seals, checks the
frozen workset identity, resolves every transitive semantic source against the
pinned provider tree, rejects local Lean semantic substitutions, compiles the
three parameterized transport modules at trust zero, and checks M0, R0, empty
H/M/R cut sets, cold replay metadata, and strict dominance over
`THM-M-0387`.  Exact provider-backed root recomputation remains a Master
obligation because the canonical Lake search path lacks the provider module.

The current validation receipt records the exact argv digest, output digests,
timestamps, exit code, and semantic-environment digest.  The canonical Master
must rerun the validation against integrated bytes; this worker receipt cannot
set `master_accepted`.
