# Build validation

The only worker-authorized command is the exact `complete-target-semantic-proof-debt` command from `../claim.json`, including `--no-lean`. Its stdout, stderr, timestamps, exit status, and argv digest are frozen in `receipts/current-validation.json` after all owned artifact bytes are final.

Static checks also scan active Lean code for placeholders and semantic shadowing, verify the exact frozen member and provider source digests, validate sealed semantic/machine/readability/release records, and enforce the complete 18-file writable path set.

No local Lean/Lake/Elan command is run. Canonical compilation must use the sealed provider-native route and exact import, elaborate each standalone claim-owned file at trust 0, verify `#print axioms` for `maximalLength_le_audit`, recompute the exact elaborated expression and transitive non-foundation constant environment, and run semantic-substitution mutations. Only the Master may convert this worker candidate into canonical acceptance.
