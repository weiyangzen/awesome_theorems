# THM-M-0528 release decision

## Exact verdict

`S56-M-0528-RELEASE` is **blocked**. The lifecycle remains `planned`, the
accepted root vector remains `[H3, M3, R4]`, and both `audit_complete` and
`theorem_complete` remain false. No receipt is accepted and no theorem
completion or release is claimed.

The first node gate failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`: validation is
only provisional worker evidence and has not been accepted by the master. The
first release-protocol failure is section 10.6's cold empty-cache hermetic
replay.

## Reconciliation

The exact statement, local wrapper, and a separately implemented local probe
kernel-replay against pinned Lean 4.29.0 and mathlib. This is useful provisional
evidence, but the frozen typed graph predates proof execution and still records
`root_closed=false` with `M0528-X-ANCHOR` open. A release worker cannot rewrite
that authoritative state or accept the validation dependency.

The release packet also lacks accepted H0 primary-source review and R0 readable
review, full transitive declaration and TCB provenance, an immutable clean
input, empty-cache network-denied build and offline restoration, SBOM/license
closure, distinct independently provisioned signed runners, an independently
implemented minimal receipt verifier, required adversarial CI fixtures, and a
deterministic evidence bundle. The same-checkout validation probe does not
satisfy independent release verification.

## Validation

Run from repository root without `lake update`, `lake build`, clone, fetch, or
dependency mutation:

```text
python3 Stage1_Instances/THM-M-0528/check_release.py
  exit 0
  release-decision: ok (blocked; dependency unaccepted; H3/M3/R4 unchanged)
  validation replay: ok (exact root provisional; authoritative graph stale)
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
```

The checker replays the recorded narrow validation recipe, verifies reconciled
input hashes, manifest membership, dependency support state, graph freshness
failure, unchanged authoritative state, terminal booleans, and the complete
release cut set. Only the integration lane may accept the dependency and
reconcile state; a separately provisioned release lane must close the remaining
assurance gates.
