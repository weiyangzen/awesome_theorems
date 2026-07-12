# THM-M-0540 release decision

Item `S56-M-0540-RELEASE` is **blocked**. The prerequisite worker validation receipt is internally
consistent and supports provisional exact-root kernel replay against the pinned warm cache. It is
explicitly non-release evidence and cannot support either terminal decision.

`AUDIT-Z` is the first failed gate: primary-source pinpoint and errata review (`H0`), a uniquely
anchored readable reconstruction (`R0`), and independent review are open. Consequently
`audit_complete=false`. The later release gates also fail closed: there is no immutable clean input,
cold empty-cache build, disconnected offline restoration, complete TCB/SBOM/license archive,
deterministic evidence bundle, second independently provisioned clean runner, independently
implemented minimal verifier, or master acceptance.

The exact verdict is therefore:

```text
verdict: blocked
lifecycle: planned -> planned
root vector: [H1, M3, R4] -> [H1, M3, R4]
audit_complete: false
theorem_complete: false
accepted_receipt_ids: none
```

`release-decision.json` content-addresses the reconciled inputs and records the full root cut set.
This negative decision does not promote `M0`, `AUDIT-Z`, `THEOREM-Z`, release, or authoritative item
state. Retry requires accepted audit evidence and all hermetic, supply-chain, deterministic-bundle,
independent-verification, and master-acceptance receipts over one immutable digest set.
