# Build validation

Validation command: `complete-target-semantic-proof-debt`, exactly as frozen in the claim card.

The three claim-owned Lean files are compiled separately with the repository-pinned toolchain, `lake env lean --trust=0`, and `LAKE_NO_CACHE=1`. The final frozen validator repeats those invocations after checking the pinned workset member, source bytes, semantic environment, no-shadow policy, exact M0 closure, total R0 mapping, and release certificate.

The authoritative timestamps and stdout/stderr digests for the final run are recorded in `receipts/current-validation.json` and `_outbox/result.json`. The generated `changes.patch` is content-addressed after all 18 writable artifacts are finalized.
