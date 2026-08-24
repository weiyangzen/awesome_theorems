# Build validation — S5-CLM-00003643

Worker validation uses exactly the immutable claim command `complete-target-semantic-proof-debt` with `--no-lean`. It checks the complete 18-file target surface, exact workset identity, sealed semantic environment, pinned provider-source digests, forbidden Lean constructs and substitutions, M0/R0 evidence shape, empty cut sets, current trace shape, and strict dominance over `THM-M-0387`.

The worker boundary forbids Lean, Lake, and Elan, so this document does not present a worker compilation as evidence. After harvest the canonical Master must compile each Lean file at trust zero from the canonical pinned environment, recompute the elaborated root and transitive declaration/type/body/source/revision census, and rerun cold offline and substitution-mutation checks. `receipts/current-validation.json` records only the permitted local preflight.
