# Build validation

Worker command `complete-target-semantic-proof-debt` runs the immutable
claim-local validator with `--no-lean`. This is the mandated semantic/evidence
preflight: it checks the exact owned artifact set, frozen workset binding,
authority seals, semantic environment, import/provenance guards, forbidden
Lean constructs, M0/R0 cut sets, and strict-dominance certificate.

Lean, Lake, and Elan are intentionally not invoked in this generation.
Canonical Master must compile `Statement.lean`, `Proof.lean`, and `Audit.lean`
from the integrated tree at trust zero. A worker-side pass is therefore
necessary for harvest but not sufficient for canonical theorem completion.

The exact command, output digests, UTC interval, and exit status are recorded
in `receipts/current-validation.json` and repeated in the generation result.
