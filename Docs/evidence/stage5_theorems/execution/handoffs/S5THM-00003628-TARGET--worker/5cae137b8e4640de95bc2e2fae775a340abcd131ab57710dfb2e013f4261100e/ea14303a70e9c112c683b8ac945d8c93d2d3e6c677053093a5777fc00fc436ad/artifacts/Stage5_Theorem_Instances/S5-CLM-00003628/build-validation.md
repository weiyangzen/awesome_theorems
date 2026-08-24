# Build validation receipt

Worker scope is the semantic, offline `--no-lean` preflight mandated by the
claim.  It checks exact identity, seals, source bytes, semantic environment,
placeholder absence, M0/R0 shape, and release dominance.  The canonical
Master, after harvest, performs the trust-zero Lean compilation and cold
from-source replay.

Command identity: `complete-target-semantic-proof-debt`.

Expected result: all task-local gates pass; no canonical files are modified.
