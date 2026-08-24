# Build validation

Pinned toolchain: `leanprover/lean4:v4.29.0`.

The three claim-owned Lean files were each invoked from the pinned canonical
Lean project using `lake env lean --trust=0` with `LAKE_NO_CACHE=1`; all exited
zero with empty standard output and standard error. The frozen command
`complete-target-semantic-proof-debt` was then invoked with the immutable claim
card and this generation's work root. Exact timestamps and channel digests are
recorded in `receipts/current-validation.json` and the final worker result.

Cold replay means no generated target `.olean` is relied upon: the validator
passes the absolute source file directly to Lean and disables Lake caching.
The Master must repeat the command against the integrated content-addressed
snapshot before acceptance.
