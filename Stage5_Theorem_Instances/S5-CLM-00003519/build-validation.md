# Build validation — worker preflight

Validation route: the sole command frozen in `claim.json`, invoking
`_baseline/check_stage5_theorem_item.py` with this claim card, this work root,
and `--no-lean`.

The no-Lean mode authenticates frozen identity/source bindings, exact routed
imports and declaration references, absence of placeholders and semantic
shadowing, the sealed semantic-environment record, exact M0/R0 shape, empty
cut sets, and strict dominance over the pinned incomplete THM-M-0387 fixture.

The final exit code, times, and stream digests are recorded in
`receipts/current-validation.json` and `_outbox/result.json`. Provider-native
trust-zero compilation is deliberately not run by this worker and remains the
canonical Master's independent post-harvest gate.
