# Build validation — S5-CLM-00003536

Required command ID: `complete-target-semantic-proof-debt`.

The worker runs the immutable task-local validator with the immutable claim
card and this generation's work root.  That validator performs semantic seal
checks, shadow/substitution checks, machine/readability/release checks, and
trust-zero Lean elaboration.  Exact start/end times and stdout/stderr digests
are recorded in `receipts/current-validation.json` and the worker result.

The final command outcome is valid only when the exit code is zero.  Canonical
acceptance remains a distinct Master action after integration.
