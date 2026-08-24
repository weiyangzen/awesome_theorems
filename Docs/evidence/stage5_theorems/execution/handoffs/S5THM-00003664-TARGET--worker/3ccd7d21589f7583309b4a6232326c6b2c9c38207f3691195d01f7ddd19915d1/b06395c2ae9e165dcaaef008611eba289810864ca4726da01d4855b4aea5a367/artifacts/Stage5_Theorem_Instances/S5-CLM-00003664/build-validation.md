# Build validation — S5-CLM-00003664

Worker validation is intentionally limited to the immutable claim's command
`complete-target-semantic-proof-debt` with `--no-lean`. The task-local checker
validates exact ownership, all eighteen required artifacts, frozen statement
identity, source pins, no executable semantic substitution or local shadowing,
sealed M0/R0/release records, empty cut sets, and strict-dominance evidence.

Lean, Lake, and Elan were not invoked. A green worker preflight is not a
canonical trust-zero build. The harvested bytes require Master's clean offline
from-source compilation, expression/environment recomputation, axiom census,
semantic-substitution mutations, and current trace before acceptance.
