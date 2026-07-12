# THM-M-0156 release decision

Item `S56-M-0156-RELEASE` has the exact verdict **blocked**. The lifecycle remains
`planned`, the accepted root vector remains `[H1, M3, R4]`, and both `AUDIT-Z` and
`THEOREM-Z` are blocked. `theorem_complete` remains false and no receipt is accepted.
This is a tested negative release decision, not theorem completion or master acceptance.

## Evidence reconciliation

The validation receipt provides provisional evidence that the exact frozen rectangular-box
divergence target elaborates through the pinned mathlib proof body and local adapter. A separately
written same-workspace reconstruction reaches the same target, the scoped placeholder and unsafe
checks pass, and Lean reports only `propext`, `Classical.choice`, and `Quot.sound`. This supports a
provisional `M0-W` observation but cannot change accepted state.

The first failed node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation receipt is worker
evidence, not a master-accepted prerequisite. The next failure is structured-state freshness:
`typed-graphs.json` predates proof closure and records `root_closed=false` with
`M0156-B-CANDIDATE` as its open cut. The planned instance's `[H1, M3, R4]` vector therefore remains
authoritative until master reconciliation.

`AUDIT-Z` also fails because independently accepted H0 source fidelity, R0 reconstruction, and
complete inventory/source-boundary reconciliation are absent. Release lacks complete transitive
provenance and TCB closure, an immutable empty-cache network-denied cold build, offline archive
restoration, SBOM/licenses, protected CI and mutation gates, two qualifying signed attestations,
an independent minimal verifier, and a deterministic content-addressed bundle. The same-checkout
reconstruction and shared pinned cache do not satisfy independent verification.

## Validation

Run from base revision `d41c33c7ad196cf30c996231fabd214f4d9f5248` with no dependency update,
build, fetch, clone, network access, or `.lake` mutation:

```text
python3 Stage1_Instances/THM-M-0156/check_release.py
  exit 0
  release-decision: ok (blocked; dependency unaccepted; H1/M3/R4 unchanged)
  validation replay: ok (exact root provisional; authoritative graph stale)
  AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false; accepted receipts=[]
```

The release checker binds the reconciled inputs by SHA-256, checks the negative terminal decision
and complete release cut set, and reruns the narrow validation recipe using the existing pinned
Lean environment. The pre-existing untracked `.lake` symlink remains nonrelease evidence.

## Retry boundary

The integration lane must master-accept the validation dependency and reconcile fresh structured
state. A release lane must then close H0/R0 review, provenance and TCB, hermetic supply-chain replay,
independent verification, deterministic bundle, and master terminal-decision gates.
