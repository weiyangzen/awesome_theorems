# Build validation

Validation command: the frozen `complete-target-semantic-proof-debt` command
from the immutable claim card.  It checks exact artifact ownership, semantic
crosswalk identity, provider-source hashes, no-shadowing rules, M0 closure,
R0 reconstruction, release strict dominance, and then cold Lean elaboration of
all three surfaces.

Expected result: exit code 0 with trust-zero replay.
